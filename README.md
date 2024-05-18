# Board Game Scoring App

A simple Django app to keep scores of boardgames with friends.

## Init DB

1. Run migrations and migrate DB.
```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

2. Create superuser (username `admin`, password `admin`)
```bash
$ bash scripts/create_superuser.bash
```

3. Seed DB
```bash
TBD
```

## Run the dev server

```bash
$ python manage.py runserver $PORT_NUMBER
```
where `$PORT_NUMBER` is optional and the default is `8000`.
