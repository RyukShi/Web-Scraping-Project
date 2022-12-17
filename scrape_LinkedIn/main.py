from jobs_scraper_beautifulsoup import JobsScraperBeautifulSoup


def main():
    countries = ['CHINA', 'ICELAND']
    jobs_scraper_beautifulsoup = JobsScraperBeautifulSoup(verbose=True, specific_countries=countries)
    jobs_scraper_beautifulsoup.run()


if __name__ == '__main__':
    main()
