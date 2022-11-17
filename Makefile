compilemessages:
	doppler run -- ./manage.py compilemessages

createsuperuser:
	doppler run -- ./manage.py createsuperuser

makemessages:
	doppler run -- ./manage.py makemessages

makemigrations:
	doppler run -- ./manage.py makemigrations

migrate:
	doppler run -- ./manage.py migrate

runserver:
	doppler run -- ./manage.py runserver

shell:
	doppler run -- ./manage.py shell

up-db:
	doppler run -- docker-compose -f docker-compose.dev.yml up -d db

down:
	doppler run -- docker-compose -f docker-compose.dev.yml down
