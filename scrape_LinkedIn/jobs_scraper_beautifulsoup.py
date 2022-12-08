from requests import get
from os import getcwd
from bs4 import BeautifulSoup
from random import random
from urllib.parse import urlencode, quote
from json import dumps

# import functions, classes and constant
from utils import chill, join_path, is_valid_file
from my_logger import MyLogger
from constant import COUNTRIES
from my_connector import MyConnector


class JobsScraperBeautifulSoup:

    def __init__(
        self,
        base_url: str = "https://www.linkedin.com/jobs/search?",
        verbose: bool = False
    ):
        self.BASE_URL = base_url
        self.verbose = verbose
        self.keywords = 'Web Development'
        self.COUNTRIES = COUNTRIES
        # get the current working directory
        self.PATH = getcwd()
        self.SAVE_URLS_PATH_FILE = join_path(
            self.PATH, 'data', 'save_urls.txt')

        self.scraped_jobs = []
        self.scraped_urls = []
        self.missed_countries = []

        self.logger = MyLogger(
            log_file=join_path(self.PATH, "logs",
                               "jobs_scraper_BeautifulSoup.log"),
            log_name="JobsScraperBeautifulSoup",
        )

    def run(self):
        """ Run the scraper """
        self.logger.info("Start scraping")

        if (is_valid_file(self.SAVE_URLS_PATH_FILE)):
            self.load_jobs_urls()
            self.logger.info("Jobs url loaded from save_urls.txt file")
        else:
            self.scraping_jobs_url(self.COUNTRIES)
            if self.missed_countries:
                self.logger.info(
                    f"{len(self.missed_countries)} countries missed, try again to get urls")
                # try again to get the missed countries jobs url
                self.scraping_jobs_url(self.missed_countries)
        self.scraping_jobs_data()

        self.logger.info("Scraping done")

    def load_jobs_urls(self):
        with open(self.SAVE_URLS_PATH_FILE, 'r', encoding='utf-8') as txt_file:
            urls = txt_file.readlines()
            for url in urls:
                self.scraped_urls.append(url.strip("\n"))

    def save_jobs_urls(self):
        with open(self.SAVE_URLS_PATH_FILE, 'w', encoding='utf-8') as txt_file:
            for url in self.scraped_urls:
                txt_file.write(url + "\n")

    def get_soup(self, url: str) -> BeautifulSoup:
        """ Get the soup object from url """
        try:
            response = get(url)
            return BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            self.logger.error(f"Error : {e}")
            return None

    def get_jobs_url(self, url: str) -> list:
        """ Gets the first 25 jobs at most from search url """
        # get soup object
        soup = self.get_soup(url)

        if soup == None:
            self.logger.error(f"Failed to get soup object for this url: {url}")
            return None

        results_list = soup.find('ul', class_='jobs-search__results-list')
        if results_list:
            links = []
            a_tags = results_list.find_all(
                'a', class_='base-card__full-link', href=True)
            for a_tag in a_tags:
                links.append(a_tag['href'])
            return links
        else:
            self.logger.error(f"No links found for this url: {url}")
            return None

    def get_jobs_data(self, url: str) -> tuple:
        # get soup object
        soup = self.get_soup(url)

        if soup == None:
            return None
        # if the jobs offer is not found from database
        if soup.find('div', class_='not-found-404'):
            self.logger.info(f"Page not found for this url: {url}")
            return None

        title = soup.find('h1', class_='top-card-layout__title')
        if title != None:
            title = title.get_text(strip=True)

        description = soup.find('div', class_='show-more-less-html__markup')
        if description != None:
            description = description.get_text()
        else:
            self.logger.info(f"No description found for this url: {url}")

        company_name = soup.find(
            'a', class_='topcard__org-name-link', href=True)
        company_url = None
        if company_name != None:
            company_url = company_name['href']
            company_name = company_name.get_text(strip=True)

        location = soup.find(
            'span', class_='topcard__flavor topcard__flavor--bullet')
        if location != None:
            location = location.get_text(strip=True)

        criteria_list = soup.find_all(
            'li', class_='description__job-criteria-item')
        if criteria_list != None:
            criteria = {}
            for c in criteria_list:
                key = c.find('h3')
                value = c.find('span')
                if key and value:
                    criteria[key.get_text(strip=True)] = value.get_text(
                        strip=True)
        return (
            title, description, company_name,
            company_url, location, dumps(criteria), url
        )

    def scraping_jobs_url(self, countries: list):
        if self.verbose:
            count = 1
            length = len(countries)

        # for loop with random shuffle
        for country in sorted(countries, key=lambda _: random()):
            if self.verbose:
                print(f"{count}/{length} : {country}")

            params = {'keywords': self.keywords,
                      'location': country, 'f_TPR': 'r86400'}
            search_url = self.BASE_URL + urlencode(params, quote_via=quote)
            # get jobs's url based on params
            jobs_url = self.get_jobs_url(search_url)

            if jobs_url == None:
                self.missed_countries.append(country)
                count += 1
                continue

            self.logger.info(f"{len(jobs_url)} jobs found for {country}")

            self.scraped_urls.extend(jobs_url)

            count += 1
            chill(3)

    def scraping_jobs_data(self):
        connector = MyConnector()

        # try to connect to the database
        if not connector.connect_to_db():
            self.logger.error("Can't connect to the database")
            # save the jobs url in save_urls.txt file
            self.save_jobs_urls()
            self.logger.info("Scraped urls saved to save_urls.txt file")
            return

        # max number of jobs offers to insert in the table
        MAX_ELEMENTS = 25
        elements = 0

        if self.verbose:
            count = 1
            length = len(self.scraped_urls)

        for url in self.scraped_urls:
            jobs_data = self.get_jobs_data(url)

            if jobs_data == None and self.verbose:
                print(f"{count}/{length} : No data")

            if jobs_data == None:
                count += 1
                continue

            if self.verbose:
                print(f"{count}/{length} : {jobs_data[0]}")

            self.scraped_jobs.append(jobs_data)
            elements += 1
            if elements >= MAX_ELEMENTS:
                # insert the scraped jobs offers in the database
                if connector.insert_many(self.scraped_jobs):
                    self.logger.info(
                        f"Data inserted successfully ({len(self.scraped_jobs)} row(s) affected)")
                    # clear the scraped_jobs list
                    self.scraped_jobs = []
                    # reset the elements counter
                    elements = 0
                else:
                    self.logger.error(
                        "Data inserted failed, try again next iteration")
            count += 1
            chill(2)

        # if scraped_jobs list is not empty
        if self.scraped_jobs:
            # insert the scraped jobs offers in the database
            if connector.insert_many(self.scraped_jobs):
                self.logger.info(
                    f"Data inserted successfully ({len(self.scraped_jobs)} row(s) affected)")
            else:
                self.logger.error("Data inserted failed")

        # close connection
        connector.close()
