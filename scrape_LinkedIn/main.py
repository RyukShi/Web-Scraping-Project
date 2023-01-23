from jobs_scraper_beautifulsoup import JobsScraperBeautifulSoup


def main():
    jobs_scraper_beautifulsoup = JobsScraperBeautifulSoup(verbose=True)
    jobs_scraper_beautifulsoup.run()


if __name__ == '__main__':
    main()
