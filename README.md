# Урок 30. Пользователи и роли. Домашнее задание
На этой неделе мы добавим в наше приложение пользователей, добавим к ним ролевую модель и разграничим права. 

# Шаг 1

Перепишите модель пользователя так, чтобы она наследовалась от AbstraсtUser.

# Шаг 2

Добавьте в приложение авторизацию по JWT.

Должно получиться следующее:

```json
Request
POST /user/token/
{
	"username": "user",
	"password": "password",
}

Response
200
{
    "refresh": "JWT_token",
    "access": "JWT_token"
}

400 
{
    "username": [
        "This field is required."
    ],
    "password": [
        "This field is required."
    ]
}

Request
POST /user/token/
{
	"username": "user",
	"password": "password",
	"refresh":  "JWT_token"
}

Response
200
{
    "refresh": "JWT_token",
    "access": "JWT_token"
}

400 
{
    "refresh": [
        "This field is required."
    ],
    "password": [
        "This field is required."
    ]
}
```

# Шаг 3

Скройте возможность просмотра детальной информации объявлений для неавторизованных пользователей. Теперь смотреть карточку объявления могут только те, кто зарегистрировался и вошел в свой аккаунт.  

# Шаг 4

Еще одна бизнес-хотелка: подборки объявлений. 

Авторизованные пользователи способны создавать подборки объявлений: можно сделать название и накидать в подборку несколько разных объявлений. Просматривать эти подборки могут все, а вот создавать, редактировать и удалять — только авторизованные пользователи. Менять, естественно, можно только свою подборку.

Реализуйте эту функцию с помощью GenericAPIView. Спецификация ниже: 

```json
Request
GET /selection/

Response
200
{
    "count": 4,
    "next": null,
    "previous": null,
    "results": [
        {
						"id": 1,
						"name": "Подборка Васи"
				},
				{
						"id": 2,
						"name": "Подборка Пети"
				},
    ]
}
```

```json
Request
GET /selection/1/

Response
200
{
    "id": 1,
    "items": [
        {
            "id": 18,
            "name": "FSDFDS",
            "price": 123,
            "description": "SDFSAF",
            "is_published": false,
            "image": null,
            "author": 4,
            "category": 1
        },
        {
            "id": 19,
            "name": "dadsfa",
            "price": 18,
            "description": "sdfds",
            "is_published": true,
            "image": null,
            "author": 4,
            "category": null
        }
    ],
    "name": "Подборка Васи",
    "owner": 19
}

404
{
	"error": "Not Found"
}

```

```json
Request
POST /selection/create/
{
	"name": "Подборка Васи",
	"owner": 19,
	"items": [18]
}

Response
200
{
  "id": 1,
	"name": "Подборка Васи",
	"owner": 19,
	"items": [18]
}

404 
{
    "detail": "Not found."
}

```

```json
Request
PATCH /selection/3/update/
{
	"name": "Подборка Васи",
	"owner": 19,
	"items": [18, 19]
}

Response
200
{
  "id": 3,
	"name": "Подборка Васи",
	"owner": 19,
	"items": [18, 19]
}

404
{
    "detail": "Not found."
}
```

```json
Request
DELETE /selection/1/

Response
204
```

# Шаг 5

Ну и последнее на сегодня: найдите ручки, которые отвечали за редактирование и удаление объявлений. Эти ручки нужно оставить доступными по следующим условиям: 

- либо это объявление принадлежит текущему пользователю (он его создавал);
- либо пользователь, который пытается поменять или удалить объявление, является модератором или админом.

Опубликуйте вашу работу на GitHub, сдайте ссылку на нее.

**Критерии выполнения:**

- [ ]  Пользователь наследуется от AbstractUser.
- [ ]  Ролевая модель определена через собственное поле role с параметром choices.
- [ ]  Доступы регулируются через Permissions.
- [ ]  permission_classes используются как на уровне класса (атрибутом класса), так и на уровне метода (декоратором).