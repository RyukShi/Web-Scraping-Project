from json import dumps


class JobOffer():

    def __init__(
        self,
        title: str = None,
        description: str = None,
        company_name: str = None,
        company_url: str = None,
        location: str = None,
        criteria: dict = None,
        country: str = None,
        jobboard: str = None
    ):
        self.title = title
        self.description = description
        self.company_name = company_name
        self.company_url = company_url
        self.location = location
        self.criteria = criteria
        self.country = country
        self.jobboard = jobboard

    def to_tuple(self) -> tuple:
        """ Return a tuple of the data to insert in the database """
        return (
            self.title,
            self.description,
            self.company_name,
            self.company_url,
            self.location,
            # convert criteria dict to json string
            dumps(self.criteria),
            self.country,
            self.jobboard
        )

    def __str__(self) -> str:
        return f"title : {self.title} - company : {self.company_name} - location : {self.location}"
