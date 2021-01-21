from bs4 import BeautifulSoup
import requests
import csv
import psycopg2
import psycopg2
from psycopg2 import Error
from queue import Queue

class PoemScraper:
    def __init__(self, start, end):
        """

        :param start: Bound of user id
        :param end: Bound of user id
        """
        self.header = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
            'Host': 'poem.tkaraoke.com',
            'Origin': 'https://poem.tkaraoke.com',
            'Referer': 'https://poem.tkaraoke.com/'
        }
        self.url = lambda id: 'https://poem.tkaraoke.com/{}/'.format(str(id))

        self.db_infor = {
            'user': 'pvhanh',
            'password': 'pvhanh',
            'host': '118.70.82.134',
            'port': '5432',
            'database': 'poem'
        }

        self.ids = Queue(maxsize=0)

        self.contents = Queue(maxsize=0)


    def get_idxs(self, filename, start, end):
        """
        Read all id of user in range (start, end)
        :param filename: file contain url of all user
        :return: list
        """
        res = []
        with open(filename, 'r') as file:
            for line in file.readlines():
                id = int(line.split("/")[-2])
                if start <= id < end:
                    res.append(id)

        return res


    def fetch(self):
        """
        Fetch all poems of a member.
        """

        id = self.ids.get()
        base_url = self.url(id)

        page = requests.get(base_url, headers=self.header)
        soup = BeautifulSoup(page.text, 'html.parser')

        container = soup.find_all('table', class_='table table-condensed table-fuction table-athor')
        if len(container) != 0:
            information = container[0].find_all('b')
            num_poems = [int(s) for s in str(information[0]).split(" ") if s.isdigit()]

        # Maximum poems of 1 page is 10
        num_pages = int(num_poems/10)

        for i in range(num_pages):
            page_id = "2-{}.html".format(i+1)
            page_url = base_url + page_id

            response = requests.get(url=page_url, headers=self.header)
            soup = BeautifulSoup(response.text, 'html.parser')

            container = soup.find_all('td', class_='td_poem_items')
            for c in container:
                poem_link = self.header['Origin'] + c.find('a', href=True)['href']

                response = requests.get(url=poem_link, header=self.header)
                soup = BeautifulSoup(response.text, 'html.parser')

                content = soup.find('div', class_='col-md-12 wrapper-content-poem')



    def list_id(self, start, end):
        ids = list()
        num_poems = 0

        try:
            for id in range(start, end, 1):
                page = requests.get(self.url(id), headers=self.header)
                soup = BeautifulSoup(page.text, 'html.parser')

                container = soup.find_all('table', class_='table table-condensed table-fuction table-athor')
                if len(container) != 0:
                    ids.append(id)
                    content = container[0].find_all('b')
                    if len(content) != 0:
                        num_poems += [int(s) for s in str(content[0]).split(" ") if s.isdigit()][0]

                print("id: {}, num:{}".format(id, num_poems))

        except  Exception as e:
            print("Id:", id)
            print("Num Poems:", num_poems)
            print(e)
            return ids, num_poems

        return ids, num_poems

if __name__ == '__main__':

    """
    scraper = PoemScraper()

    ids, num_poems = scraper.list_id(start=10000, end=16600)
    print("Total poems: {}".format(num_poems))

    f = open('url_of_user.csv', 'w')
    writer = csv.writer(f)
    for id in ids:
        writer.writerow([scraper.url(id)])
    """


    try:
        # Connect to an existing database
        connection = psycopg2.connect(user="pvhanh",
                                      password="pvhanh",
                                      host="118.70.82.134",
                                      port="5432",
                                      database="poem")

        # Create a cursor to perform database operations
        cursor = connection.cursor()
        # Print PostgreSQL details
        print("PostgreSQL server information")
        print(connection.get_dsn_parameters(), "\n")
        # Executing a SQL query
        cursor.execute("SELECT version();")
        # Fetch result
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


