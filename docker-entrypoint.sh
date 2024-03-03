python manage.py makemigrations game_data
python manage.py migrate game_data

daphne -b 0.0.0.0 -p 8000 config.asgi:application