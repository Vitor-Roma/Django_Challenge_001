all:
	docker-compose up
	docker exec application pip3 install --upgrade pip
	docker exec application pip3 install -r requirements.txt
	docker exec application python3 manage.py makemigrations
	docker exec application python3 manage.py migrate



install:
	pip3 install -r requirements.txt


build:
	docker exec application pip3 install --upgrade pip
	docker exec application pip3 install -r requirements.txt
	docker exec application python3 manage.py makemigrations
	docker exec application python3 manage.py migrate

test:
	docker exec application python3 manage.py test

run:
	docker-compose up

coverage:
	docker exec application coverage run manage.py test
	docker exec application coverage report
	docker exec application coverage html
