from django.core.management.base import BaseCommand
from selenium.webdriver.chrome.options import Options
from api import tasks


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        tasks.get_movies()

    def set_chrome_options(self) -> None:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_prefs = {}
        chrome_options.experimental_options["prefs"] = chrome_prefs
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        return chrome_options
