python manage.py makemigrations game_data game_server
python manage.py migrate game_data game_server

daphne -b 0.0.0.0 -p 8000 config.asgi:application