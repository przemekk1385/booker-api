runserver:
	doppler run -- ./manage.py runserver

makemigrations:
	doppler run -- ./manage.py makemigrations

migrate:
	doppler run -- ./manage.py migrate

updb:
	doppler run -- docker-compose -f docker-compose.dev.yml up -d db

down:
	doppler run -- docker-compose -f docker-compose.dev.yml down
