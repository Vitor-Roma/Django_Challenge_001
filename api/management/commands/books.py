from __future__ import absolute_import, unicode_literals
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.core.management.base import BaseCommand
from selenium.webdriver.chrome.options import Options
from api.tasks import web_scrap, set_chrome_options
from challenge.celery import app
from api.models import Author, Article
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        x = 1
        page = f'https://www.goodreads.com/list/show/1.Best_Books_Ever?page={x}'
        link_list = self.get_links(page)
        web_scrap.delay(link_list)

    def get_links(self, page):
        driver = webdriver.Chrome(options=set_chrome_options())
        driver.get(page)
        link_list = []
        x = 1
        while x <= 5:
            page = f'https://www.goodreads.com/list/show/1.Best_Books_Ever?page={x}'
            driver.get(page)
            books = driver.find_elements(By.CLASS_NAME, 'bookTitle')
            x += 1
            for book in books[:20]:
                list = book.get_attribute('href')
                book_list = {'link': list}
                link_list.append(book_list)
        return link_list


# def web_scrap(self, link_list):
#     driver = webdriver.Chrome(options=self.set_chrome_options())
#     for link in link_list:
#         page = link['link']
#         driver.get(page)
#         try:
#             author_name = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.CLASS_NAME, 'authorName')))
#             author_name = author_name.text
#         except:
#             author_name = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.CLASS_NAME, 'ContributorLink__name')))
#             author_name = author_name.text
#         try:
#             title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
#             title = title.text
#         except:
#             title = 'No title available'
#         summary = 'No summary available'
#         # import ipdb; ipdb.set_trace()
#         try:
#             category = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.CLASS_NAME, 'bookPageGenreLink')))
#             category = category.text
#         except:
#             try:
#                 category = WebDriverWait(driver, 10).until(
#                     EC.presence_of_element_located((By.CLASS_NAME, 'BookPageMetadataSection__genre')))
#                 category = category.text
#             except:
#                 category = 'No category available'
#         if category == '':
#             category = 'No category found'
#         try:
#             button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, '...more')))
#             button.click()
#             body = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'descriptionContainer')))
#             body = body.text[:-7]
#         except:
#             try:
#                 body = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'Formatted')))
#                 body = body.text[:-7]
#             except:
#                 body = "body not found, so i'll fill with some text here, that way i can create the article"
#         firstParagraph = body[:50]
#         try:
#             author = Author.objects.get(name=author_name)
#             author_id = author.id
#         except:
#             author = Author.objects.create(name=author_name)
#             author_id = author.id
#         try:
#             Article.objects.get(title=title)
#         except:
#             Article.objects.create(author_id=author.id, category=category, title=title, summary=summary,
#                                    firstParagraph=firstParagraph, body=body)
#         print('Executando...')
