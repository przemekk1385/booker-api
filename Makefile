manage/collectstatic:
	doppler run -- ./manage.py collectstatic

manage/compilemessages:
	doppler run -- ./manage.py compilemessages

manage/createsuperuser:
	doppler run -- ./manage.py createsuperuser

manage/makemessages:
	doppler run -- ./manage.py makemessages

manage/makemigrations:
	doppler run -- ./manage.py makemigrations

manage/migrate:
	doppler run -- ./manage.py migrate

manage/runserver:
	doppler run -- ./manage.py runserver

manage/shell:
	doppler run -- ./manage.py shell

docker/down:
	doppler run -- docker-compose -f docker-compose.dev.yml down

docker/up:
	doppler run -- docker-compose -f docker-compose.dev.yml up -d
