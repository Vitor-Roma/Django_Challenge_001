install:
	pip3 install -r requirements.txt

build:
	python3 manage.py makemigrations
	python3 manage.py migrate

run:
	docker-compose up --build -d
	python3 manage.py runserver
