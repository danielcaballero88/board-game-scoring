# Board Game Scoring App

A simple Django app to keep scores of boardgames with friends.

## Init DB

1. Run migrations and migrate DB.

```bash
$ python manage.py makemigrations
# <output>>
$ python manage.py migrate
# <output>
```

1. Create superuser (username `admin`, password `admin`)

```bash
$ bash scripts/create_superuser.bash
# super user created
```

1. Seed DB

```bash
$ bash scripts/seed_db.bash
# ...
```

## Run the dev server

```bash
$ python manage.py runserver $PORT_NUMBER
# ...
```

where `$PORT_NUMBER` is optional and the default is `8000`.

## Linters and formatters (and pre-commit hooks)

For the python code the linters in use are:

- `flake8` with configuration given in `setup.cfg`
- `pylint` with configuration given in `.pylintrc`
and the formatters are:
- `black` with default settings
- `isort` with configuration compatible with `black` (set in `setup.cfg`)

For the templates (html files) the linter is `djlint` and formatter `djhtml`.

Pre commit hooks in place using python's `pre-commit` package, check configuration in `.pre-commit-config.yaml`.
