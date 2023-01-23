from requests import get
from os import getcwd
from bs4 import BeautifulSoup
from random import random
from urllib.parse import urlencode, quote

# import functions, classes and constant
from utils import chill, join_path, is_valid_file, serialize_data, deserialize_data, get_size
from my_logger import MyLogger
from constant import COUNTRIES
from my_connector import MyConnector
from job_offer import JobOffer


class JobsScraperBeautifulSoup:

    def __init__(
        self,
        base_url: str = "https://www.linkedin.com/jobs/search?",
        verbose: bool = False,
        specific_countries: list = None,
        keywords: str = 'Web Development'
    ):
        self.BASE_URL = base_url
        self.verbose = verbose
        self.keywords = keywords
        if not specific_countries:
            self.COUNTRIES = COUNTRIES
        else:
            self.COUNTRIES = specific_countries
        # get the current working directory
        self.PATH = getcwd()
        self.SAVE_URLS_PATH_FILE = join_path(
            self.PATH, 'data', 'save_urls.json')

        self.scraped_jobs = []
        self.scraped_urls = {}
        self.missed_countries = []
        self.missed_jobs = {}

        self.logger = MyLogger(
            log_file=join_path(self.PATH, "logs",
                               "jobs_scraper_BeautifulSoup.log"),
            log_name="JobsScraperBeautifulSoup",
        )

    def run(self):
        """ Run the scraper """
        self.logger.info("Start scraping")

        if (is_valid_file(self.SAVE_URLS_PATH_FILE)):
            data = deserialize_data(self.SAVE_URLS_PATH_FILE)
            if data != None:
                self.scraped_urls = data
                self.logger.info("Jobs url loaded from save_urls.json file")
        else:
            self.scraping_jobs_url(self.COUNTRIES)
            if self.missed_countries:
                self.logger.info(
                    f"{len(self.missed_countries)} countries missed, try again to get urls")
                # try again to get the missed countries jobs url
                self.scraping_jobs_url(self.missed_countries)
        if self.scraped_urls:
            self.scraping_jobs_data(self.scraped_urls)
            if self.missed_jobs:
                self.logger.info(
                    "There are jobs missed, try again to get jobs data")
                # try again to get the missed jobs data
                self.scraping_jobs_data(self.missed_jobs)
        else:
            self.logger.info("No links found, scraping jobs process aborted")

        self.logger.info("Scraping done")

    def get_soup(self, url: str) -> BeautifulSoup:
        """ Get the soup object from url """
        try:
            response = get(url)
            return BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            self.logger.error(f"Error : {e}")
            return None

    def get_jobs_url(self, country: str) -> list:
        """ Gets the first 25 jobs at most based on country """
        params = {'keywords': self.keywords,
                  'location': country, 'f_TPR': 'r86400'}
        # generate search url based on params
        search_url = self.BASE_URL + urlencode(params, quote_via=quote)
        # get soup object
        soup = self.get_soup(search_url)

        if soup == None:
            self.logger.error(f"Failed to get soup object for {country}")
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
            self.logger.error(f"No links found for {country}")
            return None

    def get_job_data(self, url: str, country: str) -> JobOffer:
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
            # if description is None, the analysis process cannot be done
            return None

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

        if title == description == company_url == company_name == criteria == location:
            # if all the variables are equal, it means that they are all equal to None
            return None

        return JobOffer(
            title=title, description=description, job_offer_url=url,
            company_name=company_name, company_url=company_url,
            criteria=criteria, location=location, country=country
        )

    def scraping_jobs_url(self, countries: list):
        if self.verbose:
            count = 1
            length = len(countries)

        # for loop with random shuffle
        for country in sorted(countries, key=lambda _: random()):
            if self.verbose:
                print(f"{count}/{length} : {country}")

            jobs_url = self.get_jobs_url(country)

            if jobs_url == None:
                self.missed_countries.append(country)
                count += 1
                continue

            self.logger.info(f"{len(jobs_url)} jobs found for {country}")
            # append country urls into scraped_urls
            self.scraped_urls[country] = jobs_url
            count += 1
            chill(2)

    def scraping_jobs_data(self, jobs_url: dict):
        connector = MyConnector()

        # try to connect to the database
        if not connector.connect_to_db():
            self.logger.error("Can't connect to the database")
            # if the file is not empty it has been loaded previously,
            # so it's not necessary to save the urls
            if not get_size(self.SAVE_URLS_PATH_FILE) > 0:
                # save the jobs url in save_urls.json file
                success = serialize_data(
                    self.SAVE_URLS_PATH_FILE, self.scraped_urls)
                if success:
                    self.logger.info(
                        "Scraped urls saved to save_urls.json file")
            return

        for country, urls in jobs_url.items():
            if self.verbose:
                count = 1
                length = len(urls)
                print(f"{length} job offers for {country}")
            missed_jobs_temp = []
            for url in urls:
                job_data = self.get_job_data(url, country)

                if job_data == None:
                    if self.verbose:
                        print(f"{count}/{length} : No data")
                    missed_jobs_temp.append(url)
                    count += 1
                    continue

                if self.verbose:
                    print(f"{count}/{length} : {job_data}")

                self.scraped_jobs.append(job_data)

                count += 1
                chill(2)

            # insert the scraped job offers in the database
            success_insert = connector.insert_many(self.scraped_jobs)
            if success_insert:
                self.logger.info(f"Data inserted successfully for {country}")
            else:
                self.logger.info(f"Data inserted failed for {country}")
            # if missed_jobs_temp is not empty
            if missed_jobs_temp:
                # save the missed jobs for specific country
                self.missed_jobs[country] = missed_jobs_temp
            # clear the scraped_jobs list
            self.scraped_jobs = []

        # close connection
        connector.close()
