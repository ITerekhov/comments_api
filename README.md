# comments_api
## Тестовое задание: реализация системы комментариев с использованием Django + Postgresql
### Установка и запуск
Для развёртывания приложения будем использовать возможности docker-compose. Перед началом убедитесь что у вас установлен docker:
```
$ docker --version
```
И docker-compose:
```
$ docker-compose --version
```
Если не установлен, можете воспользоваться [официальным гайдом](https://docs.docker.com/compose/install/).
Для загрузки чувствительных данных понадобится файл *.env*. Скопируйте его в *comments_api/*, или если его у вас нет, создайте и заполните по примеру:
```
POSTGRES_NAME=your value
POSTGRES_USER=your value
POSTGRES_PASSWORD=your value
POSTGRES_DB=your value
DEBUG=False
```
По умолчанию приложение будет работать только локально. Если хотите запустить его для удалённого доступа, добавьте в *.env* строку:
```
ALLOWED_HOSTS=your hostname or ip address
```
Далее введите в консоли команду:
```
$ docker-compose up -d --build
```
Если запускаете приложение в первый раз, необходимо выполнить миграции:
```
$ docker-compose exec web python manage.py migrate --noinput
```
На этом этапе приложение бдует работать на указанном вами хосте, или на localhost по умолчанию. Для проверки можете выполнить
```
docker-compose top
```
