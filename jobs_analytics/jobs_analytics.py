from re import search, escape, IGNORECASE
from time import time
from json import dumps

# import constant and classes
from constant import TECHNOLOGIES
from my_connector import MyConnector


class JobsAnalytics():

    def __init__(
        self,
        verbose: bool = False
    ):
        self.connector = MyConnector()
        self.is_connected = self.connector.connect_to_db()
        self.verbose = verbose

    def tech_analysis_process(self, readjust: bool = False):
        if not self.is_connected:
            if self.verbose:
                print(
                    "Unable to run the process cause the database connection has not been established")
            return None
        q1 = """
            SELECT description, job_offer_id 
            FROM jobs_offers 
            WHERE description IS NOT NULL
        """
        if not readjust:
            q1 += " AND technologies IS NULL;"
        else:
            q1 += ";"

        q2 = """
            UPDATE jobs_offers 
            SET technologies = %s 
            WHERE job_offer_id = %s;
        """
        job_offers = self.connector.execute_query(q1)

        if job_offers:
            if self.verbose:
                start_time = time()

            for j in job_offers:
                # get elements of tuple to get job's description and id
                d, id = j
                process_dict = {}
                for category, technologies in TECHNOLOGIES.items():
                    t = [tech for tech in technologies if search(
                        fr"(?!\B\w){escape(tech)}(?<!\w\B)", d, IGNORECASE)]
                    if t:
                        process_dict[category] = t
                params_tuple = (dumps(process_dict), id)
                self.connector.update_query(q2, params_tuple)

            if self.verbose:
                print(
                    f"Process execution time for {len(job_offers)} jobs offers : {(time() - start_time)} s")
        else:
            if self.verbose:
                print(
                    "All job offers have been processed through the web technology search process")

    def search_process(self, params: dict):
        if not self.is_connected:
            if self.verbose:
                print(
                    "Unable to run the process cause the database connection has not been established")
            return None
        q1 = """
            SELECT job_offer_id, location, technologies, company_name, 
            company_url, country 
            FROM jobs_offers 
            WHERE JSON_CONTAINS(technologies, %s)
        """
        if params.__contains__("technologies"):
            params_tuple = (dumps(params["technologies"]),)
            if len(params) > 1:
                if params.__contains__("location"):
                    q1 += " AND location LIKE %s"
                    params_tuple += ("%{0}%".format(params["location"]),)
                if params.__contains__("company_name"):
                    q1 += " AND company_name LIKE %s"
                    params_tuple += ("%{0}%".format(params["company_name"]),)
                if params.__contains__("country"):
                    q1 += " AND country LIKE %s"
                    params_tuple += ("%{0}%".format(params["country"]),)
            q1 += ";"
            return self.connector.execute_query(q1, params_tuple)
        else:
            if self.verbose:
                print("It is mandatory to inform the technologies key in the params")
            return None

    def find_duplicates(self, delete: bool = False):
        if not self.is_connected:
            if self.verbose:
                print(
                    "Unable to run the process cause the database connection has not been established")
            return None
        q1 = """
            SELECT job_offer_id, title, company_name, country, location, technologies, COUNT(*) 
            FROM jobs_offers 
            WHERE JSON_EXTRACT(technologies, "$") != "{}" 
            GROUP BY title, company_name, country, location 
            HAVING COUNT(*) > 1;
        """
        duplicates = self.connector.execute_query(q1)

        if self.verbose:
            print(f"{len(duplicates)} duplicates found")

        if delete:
            while duplicates:
                d = duplicates.pop(0)
                deleteQuery = """
                    DELETE FROM jobs_offers
                    WHERE job_offer_id != %s AND title = %s AND company_name = %s AND country = %s AND
                    location = %s AND JSON_CONTAINS(technologies, %s);
                """
                rowcount = self.connector.update_query(deleteQuery, d[:-1])
                if self.verbose:
                    print(f"{rowcount} row(s) deleted")
