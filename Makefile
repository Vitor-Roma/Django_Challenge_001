all:
	docker-compose up --build
	docker exec application pip3 install --upgrade pip
	docker exec application pip3 install -r requirements.txt
	docker exec application python3 manage.py makemigrations
	docker exec application python3 manage.py migrate

build:
	docker exec application pip3 install --upgrade pip
	docker exec application pip3 install -r requirements.txt
	docker exec application python3 manage.py makemigrations
	docker exec application python3 manage.py migrate

test:
	docker exec application python3 manage.py test

run:
	docker-compose up

scrap-books:
	docker exec application python3 manage.py books

scrap-movies:
	docker exec application python3 manage.py movies

down:
	docker-compose down

coverage:
	docker exec application coverage run manage.py test
	docker exec application coverage report
	docker exec application coverage html

attach:
	docker attach application

search:
	docker exec -it application python3 manage.py search_index --rebuild