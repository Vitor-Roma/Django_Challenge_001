install:
	pip3 install -r requirements.txt


build:
	docker exec application pip3 install -r requirements.txt
	docker exec application python3 manage.py migrate

run:
	docker-compose up
