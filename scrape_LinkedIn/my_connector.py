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

    def insert_many(self, obj_data: list) -> bool:
        """ Insert data in specific SQL table """
        if self.connection and obj_data:
            obj_type = type(obj_data[0]).__name__
            if obj_type == 'JobOffer':
                insert_request = """
                INSERT INTO jobs_offers (title, description, company_name,
                                        company_url, location, criteria,
                                        job_offer_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
            # create cursor
            cursor = self.connection.cursor()
            try:
                # insert data
                cursor.executemany(
                    insert_request, [obj.to_tuple() for obj in obj_data])
                # commit the changes
                self.connection.commit()
                print(f"{cursor.rowcount} row(s) inserted")
                return True
            except Error as err:
                print(f"Error : {err}")
                self.connection.rollback()
                return False
            finally:
                cursor.close()

    def execute_query(self, q: str, params=None, fetchone=False):
        if self.connection:
            cursor = self.connection.cursor(buffered=True)
            try:
                cursor.execute(q, params)
                if fetchone:
                    return cursor.fetchone()
                return cursor.fetchall()
            except Error as err:
                print(f"Error : {err}")
            finally:
                cursor.close()

    def update_query(self, q: str, params: tuple):
        if self.connection:
            cursor = self.connection.cursor()
            try:
                cursor.execute(q, params)
                self.connection.commit()
            except Error as err:
                print(f"Error : {err}")
            finally:
                cursor.close()
