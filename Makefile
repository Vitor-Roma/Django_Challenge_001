all:
	pip install -r requirements.txt
	docker-compose up
	docker exec application pip3 install -r requirements.txt
	docker exec application python3 manage.py migrate


install:
	pip3 install -r requirements.txt


build:
	docker exec application pip3 install -r requirements.txt
	docker exec application python3 manage.py migrate

run:
	docker-compose up

