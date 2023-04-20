from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.http import JsonResponse

from rest_framework import generics
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from .models import Ad, Category, Selection
from .permissions import IfOwner, IfStaff
from .serializers import AdSerializer, CategorySerializer, SelectionSerializer, SelectionCreateSerializer, \
    SelectionListSerializer, SelectionDetailSerializer


class AdListView(ListAPIView):
    serializer_class = AdSerializer

    def get_queryset(self):
        queryset = Ad.objects.select_related('author')

        # Шаг 1: Фильтрация по категориям
        category_ids = self.request.GET.getlist("cat")
        if category_ids:
            queryset = queryset.filter(category_id__in=category_ids)

        # Шаг 2: Поиск по словам в названии
        search_text = self.request.GET.get('text', None)
        if search_text:
            queryset = queryset.filter(name__icontains=search_text)

        # Шаг 3: Фильтрация по местоположению
        location = self.request.GET.get('location', None)
        if location:
            queryset = queryset.filter(author__locations__name__icontains=location)

        # Шаг 4: Фильтрация по диапазону цен
        price_from = self.request.GET.get('price_from', None)
        price_to = self.request.GET.get('price_to', None)
        if price_from and price_to:
            queryset = queryset.filter(price__range=(price_from, price_to))
        elif price_from:
            queryset = queryset.filter(price__gte=price_from)
        elif price_to:
            queryset = queryset.filter(price__lte=price_to)

        return queryset.order_by("-price")


class AdDetailView(generics.RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated]


class AdCreateView(CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated]


class AdUpdateView(generics.UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated, IfOwner | IfStaff]


class AdDeleteView(DestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated, IfOwner | IfStaff]


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer


class CategoryDeleteView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@method_decorator(csrf_exempt, name="dispatch")
class AdImageView(UpdateView):
    model = Ad
    fields = ["name", "image"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES.get("image")
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "image": self.object.image.url if self.object.image else None
        })


class SelectionViewSet(ModelViewSet):
    serializer_class = SelectionSerializer
    queryset = Selection.objects.all()

    default_permission = [AllowAny]
    permissions = {
        "create": [IsAuthenticated],
        "update": [IsAuthenticated, IfOwner],
        'partial_update': [IsAuthenticated, IfOwner],
        "destroy": [IsAuthenticated, IfOwner]
    }

    default_serializer = SelectionSerializer
    serializers = {
        "create": SelectionCreateSerializer,
        "list": SelectionListSerializer,
        "retrieve": SelectionDetailSerializer,
        }

    def get_permissions(self):
        return [permission() for permission in self.permissions.get(self.action, self.default_permission)]

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer)



