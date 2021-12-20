import mysql.connector as mysql
import csv


def fix_name(name):
    new_name = ""
    for i in str(name):
        if i != "'":
            new_name += i
    return new_name


# Creates a class which connects to the local MySQL server, database games whene initialised.
# The class creates a connection to the database and a courses in order to work with the database server.
# When the class is closed, the connection is broken as well as the cursor and the stored data in it dismissed.
class DB:
    def __init__(self):
        self._HOST = 'localhost'
        self._DATABASE = 'games'
        self._USER = 'root'
        self._PASSWORD = 'bajsdebelajsS1'
        self.db_connection = None
        self.cursor = None

    def __enter__(self):
        self.db_connection = self._create_connection()
        self.cursor = self.db_connection.cursor()
        self._connect_to_db()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.db_connection is not None:
            self.cursor.close()
            self.db_connection.close()

    def _create_connection(self):
        try:
            return mysql.connect(host=self._HOST,
                                 database='',
                                 user=self._USER,
                                 password=self._PASSWORD)
        except mysql.Error as e:
            print(e)
            exit(1)

    def _connect_to_db(self):
        try:
            self.cursor.execute(
                """USE {}""".format(self._DATABASE)
            )

        except mysql.Error as e:
            print(e)

    # This function saves an entry in the games database, vgsales table. It requires input for all the columns.
    def save_row_vgsales(self, game_rank, game_name, platform, release_year, genre, publisher, na_sales, eu_sales,
                         jp_sales, other_sales, global_sales):
        try:
            self.cursor.execute(
                """
                INSERT INTO vgsales(
                game_rank, game_name, platform, release_year, genre, publisher, na_sales, eu_sales, jp_sales, 
                other_sales, global_sales
                )
                VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')
                """.format(game_rank, game_name, platform, release_year, genre, publisher, na_sales, eu_sales, jp_sales,
                           other_sales, global_sales)
            )
            self.db_connection.commit()

        except mysql.Error as e:
            print(game_rank, game_name, platform, release_year, genre, publisher, na_sales, eu_sales, jp_sales,
                  other_sales, global_sales)
            print(e)

    # This function saves an entry in the games database, console_s table. It requires input for all the columns.
    def save_row_console_sales(self, platform, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13, y14, y15, y16,
                               y17
                               ):
        try:
            self.cursor.execute(
                """
            INSERT INTO console_s(
            platform, `2004`, `2005`, `2006`, `2007`, `2008`, `2009`, `2010`, `2011`, `2012`, `2013`, `2014`, `2015`, 
            `2016`, `2017`, `2018`, `2019`, `2020`
            )
            VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', 
            '{}', '{}')
            """.format(platform, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13, y14, y15, y16, y17)
            )
            self.db_connection.commit()
        except mysql.Error as e:
            print(e)


# This function uses the DB class and the save_row_vgsales fucntion of the DB class to populate the table
# the data for the table comes from the vgsales.csv file.
def save_game_sales():
    with open('vgsales.csv', 'r') as file:
        data = csv.reader(file)
        with DB() as db:
            first = True    # This is to avoid the first row which contains the column headers.
            for row in data:
                print(row[0])
                if not first:
                    db.save_row_vgsales(
                        int(row[0]),
                        str(fix_name(row[1])),  # Uses fix_name() to eliminate "'" which can cause an error in MYSQL.
                        str(row[2]),
                        str(row[3]),
                        str(row[4]),
                        str(row[5]),
                        float(row[6]),
                        float(row[7]),
                        float(row[8]),
                        float(row[9]),
                        float(row[10]),
                    )
                first = False


# This function uses the DB class and the save_row_console_sales function of the DB class to populate the table.
# The data for the table comes from the console_s.csv file.
def save_console_sales():
    with open('console_s.csv', 'r') as file:
        data = csv.reader(file)
        with DB() as db:
            first = True    # This is to avoid the first row which contains the column headers.
            for row in data:
                print(row)
                if not first:
                    db.save_row_console_sales(
                        (row[0]),
                        row[1],
                        row[2],
                        row[3],
                        row[4],
                        row[5],
                        row[6],
                        row[7],
                        row[8],
                        row[9],
                        row[10],
                        row[11],
                        row[12],
                        row[13],
                        row[14],
                        row[15],
                        row[16],
                        row[17]
                    )
                first = False
