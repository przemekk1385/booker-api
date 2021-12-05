runserver:
	doppler run -- ./manage.py runserver

makemigrations:
	doppler run -- ./manage.py makemigrations

migrate:
	doppler run -- ./manage.py migrate

shell:
	doppler run -- ./manage.py shell

up_db:
	doppler run -- docker-compose -f docker-compose.dev.yml up -d db

down:
	doppler run -- docker-compose -f docker-compose.dev.yml down
