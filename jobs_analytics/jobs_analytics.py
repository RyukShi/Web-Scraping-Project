from re import search, escape, IGNORECASE
from time import time
from json import dumps

# import constant and classes
from constant import TECHNOLOGIES
from my_connector import MyConnector

connector = MyConnector()

# try to connect to the database
if not connector.connect_to_db():
    print("Can't connect to DB")
else:
    q1 = """
        SELECT description, jobs_offer_id FROM jobs_offers
        WHERE description IS NOT NULL
        AND technologies IS NULL;
    """

    q2 = """
        UPDATE jobs_offers 
        SET technologies = %s 
        WHERE jobs_offer_id = %s;
    """

    jobs_offers = connector.execute_query(q1)

    if jobs_offers:
        start_time = time()

        for j in jobs_offers:
            # get elements of tuple to get job's description and id
            d, id = j
            t = [tech for tech in TECHNOLOGIES if search(
                fr"(?!\B\w){escape(tech)}(?<!\w\B)", d, IGNORECASE)]
            params_tuple = (dumps(t), id)
            connector.update_query(q2, params_tuple)

        print(
            f"Process execution time for {len(jobs_offers)} jobs offers : {(time() - start_time)} s")
    else:
        print(
            "All job offers have been processed through the web technology search process")
