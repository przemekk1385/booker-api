createsuperuser:
	doppler run -- ./manage.py createsuperuser

makemigrations:
	doppler run -- ./manage.py makemigrations

migrate:
	doppler run -- ./manage.py migrate

runserver:
	doppler run -- ./manage.py runserver

shell:
	doppler run -- ./manage.py shell

up_db:
	doppler run -- docker-compose -f docker-compose.dev.yml up -d db

down:
	doppler run -- docker-compose -f docker-compose.dev.yml down

requirements:
	poetry export -f requirements.txt --output requirements.txt
