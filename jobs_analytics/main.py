from jobs_analytics import JobsAnalytics


def main():
    analytics = JobsAnalytics(verbose=True)
    analytics.tech_analysis_process(readjust=False)
    params = {
        "technologies": {
            "JavaScript Frameworks": ["React"],
            "Main tech": ["Ruby", "TypeScript"]
        },
        "country": 'FRANCE'
    }
    job_offers = analytics.search_process(params)
    if job_offers:
        print(job_offers)
    else:
        print("No data found in the database")

    analytics.find_duplicates(True)


if __name__ == '__main__':
    main()
