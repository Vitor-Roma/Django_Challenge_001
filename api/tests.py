from django.urls import reverse
from .models import Author, Article
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status


class TestAll(APITestCase):
    register_url = reverse('sign-up')
    login_url = reverse('login')
    articles_url = reverse('Articles-list')
    admin_article_url = reverse('Admin/Articles-list')
    authors_url = reverse('Authors-list')

    data = {
        'email': 'admin@hotmail.com',
        'username': 'admin',
        'password': '123',
    }

    def setUp(self):
        self.user = User.objects.create_user(email='admin@hotmail.com',username='admin', password='123')

        self.login_response = self.client.post(self.login_url, self.data)
        self.token = self.login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        Author.objects.create(name='qualquer nome')
        self.response = self.client.get(self.authors_url)

        self.author_id = self.response.data[0]["id"]
        self.author_detail = reverse('Authors-detail', args=[self.author_id])

        Article.objects.create(author_id=Author.objects.first().id,
                               category='qualquer categoria',
                               title='qualquer titulo',
                               summary='qualquer resumo',
                               firstParagraph='qualquer parágrafo',
                               body='qualquer body aqui, mas precisa ter mais de 50 caracteres senão nao vai dar certo'
                               )

        self.response = self.client.get(self.admin_article_url)
        self.article_id = self.response.data[0]["id"]
        self.article_detail = reverse('Articles-detail', args=[self.article_id])

    def test_author_list(self):
        response = self.client.get(self.authors_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], 'qualquer nome')

    def test_article_list(self):
        response = self.client.get(self.articles_url)
        self.assertEqual(response.data[0]['title'], 'qualquer titulo')

    def test_author_create(self):
        data = {'name': 'o nome que voce quiser'}

        response = self.client.post(self.authors_url, data=data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], data['name'])

    def test_article_create_invalid_body(self):
        data = {'author_id': Author.objects.first().id,
                'category': 'a categoria que voce quiser',
                'title': 'o titulo que voce quiser',
                'summary': 'o resumo que voce quiser',
                'firstParagraph': 'o que voce quiser escrever aqui',
                'body': 'qualquer body com menos de 50 caracteres',
                }
        response = self.client.post(self.admin_article_url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_article_create_valid_body(self):
        data = {'author_id': Author.objects.first().id,
                'category': 'a categoria que voce quiser',
                'title': 'o titulo que voce quiser',
                'summary': 'o resumo que voce quiser',
                'firstParagraph': 'o que voce quiser escrever aqui',
                'body': 'qualquer body com mais de 50 caracteres, pra ver se ta tudo dando certo aqui. aaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
                }

        response = self.client.post(self.admin_article_url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['summary'], data['summary'])

    def test_author_edit(self):
        response2 = self.client.get(self.author_detail)
        self.assertEqual(response2.data['name'], 'qualquer nome')
        data = {'name': 'qualquer outro nome'}
        response = self.client.patch(self.author_detail, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'qualquer outro nome')

    def test_article_edit(self):
        data = {'author_id': Author.objects.first().id,
                'category': 'a categoria que voce quiser',
                'title': 'o titulo que voce quiser',
                'summary': 'o novo resumo',
                'firstParagraph': 'o que voce quiser escrever aqui',
                'body': 'qualquer body com mais de 50 caracteres, pra ver se ta tudo dando certo aqui. aaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
                }
        response = self.client.put(self.article_detail, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['summary'], data['summary'])

    def test_author_delete(self):
        response = self.client.delete(self.author_detail)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, None)

    def test_article_delete(self):
        response = self.client.delete(self.article_detail)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, None)
