from mysql.connector import connect, errorcode, Error


class MyConnector:
    def __init__(
        self,
        host: str = 'localhost',
        user: str = 'root',
        password: str = 'password',
        database: str = 'web_scraping_project'
    ):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect_to_db(self) -> bool:
        try:
            self.connection = connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("Connection established")
                return True
        except Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(f"Error : {err}")
            return False

    def close(self):
        if self.connection:
            self.connection.close()
            print("Connection closed")

    def insert_many(self, data: list) -> bool:
        """ Insert many data in jobs table """
        if self.connection:
            insert_request = """
            INSERT INTO jobs_offers (title, description, company_name,
                                    company_url, location, criteria,
                                    jobs_offer_url, posted_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            # create cursor
            cursor = self.connection.cursor()
            try:
                # insert data
                cursor.executemany(insert_request, data)
                # commit the changes
                self.connection.commit()
                return True
            except Error as err:
                print(f"Error : {err}")
                self.connection.rollback()
                return False
            finally:
                cursor.close()
