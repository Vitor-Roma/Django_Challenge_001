from __future__ import absolute_import, unicode_literals
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from api.models import Author, Article
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from challenge.celery import app


def set_chrome_options() -> Options:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options


@app.task(name="web_scrap_books")
def web_scrap(link_list):
    driver = webdriver.Chrome(options=set_chrome_options())
    for link in link_list:
        page = link['link']
        driver.get(page)
        try:
            author_name = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'authorName')))
            author_name = author_name.text
        except:
            author_name = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'ContributorLink__name')))
            author_name = author_name.text
        try:
            title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
            title = title.text
        except:
            title = 'No title available'
        summary = 'No summary available'
        # import ipdb; ipdb.set_trace()
        try:
            category = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'bookPageGenreLink')))
            category = category.text
        except:
            try:
                category = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'BookPageMetadataSection__genre')))
                category = category.text
            except:
                category = 'No category available'
        if category == '':
            category = 'No category found'
        try:
            button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, '...more')))
            button.click()
            body = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'descriptionContainer')))
            body = body.text[:-7]
        except:
            try:
                body = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'Formatted')))
                body = body.text[:-7]
            except:
                body = "body not found, so i'll fill with some text here, that way i can create the article"
        if len(body) < 50:
            body = "body is too short, so i'll fill with some text here, that way i can create the article"
        firstParagraph = body[:50]
        try:
            author = Author.objects.get(name=author_name)
            author_id = author.id
        except:
            author = Author.objects.create(name=author_name)
            author_id = author.id
        try:
            Article.objects.get(title=title)
        except:
            Article.objects.create(author_id=author.id, category=category, title=title, summary=summary,
                                   firstParagraph=firstParagraph, body=body)
        print('Executando...')
