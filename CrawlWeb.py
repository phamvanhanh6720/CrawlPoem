from bs4 import BeautifulSoup
import requests
import psycopg2
from psycopg2 import Error
from queue import Queue
import os
from argparse import ArgumentParser
from threading import Thread
import unidecode


class PoemScraper:
    def __init__(self,url_file, start, end):
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
        # Connect to database
        try:
            self.connection = psycopg2.connect(user=self.db_infor['user'], password=self.db_infor['password'],
                                           host=self.db_infor['host'], port=self.db_infor['port'],
                                           database=self.db_infor['database'])
        except (Exception, Error) as error:
            print("Error while connecting to PostGreSql", error)

        self.ids = Queue(maxsize=0)
        # put id to Queue
        for id in self.get_idxs(os.path.join(url_file), start, end):
            self.ids.put(id)

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

    def fetch(self, thread):
        """
        Fetch all poems of a member.
        """
        # get first element in queue
        while not self.ids.empty():

            id = self.ids.get()
            base_url = self.url(id)

            page = requests.get(base_url, headers=self.header)
            soup = BeautifulSoup(page.text, 'html.parser')

            container = soup.find_all('table', class_='table table-condensed table-fuction table-athor')
            if len(container) != 0:
                information = container[0].find_all('b')
                num_poems = [int(s) for s in str(information[0]).split(" ") if s.isdigit()]

            author = soup.find('strong', class_='strong-name-author')
            author = (author.contents[0]).strip()
            author = author.lower()
            author = unidecode.unidecode(author)
            author = author.replace(" ", "_")
            #print(author)

            # Maximum poems of 1 page is 10
            num_pages = int(num_poems[0]/10)

            for i in range(num_pages):
                page_id = "/2-{}.html".format(i+1)
                page_url = base_url + author + page_id

                # print(page_url)

                response = requests.get(url=page_url, headers=self.header)
                soup = BeautifulSoup(response.text, 'html.parser')

                container = soup.find_all('td', class_='td-poem-items')
                count = 1
                for c in container:
                    print("Thread {} process: poem {}, page {}, id {}".format(thread, count, i + 1, id))
                    poem_link = self.header['Origin'] + c.find('a', href=True)['href']

                    response = requests.get(url=poem_link, headers=self.header)
                    soup = BeautifulSoup(response.text, 'html.parser')

                    container = soup.find_all('div', class_='col-md-12')

                    for c in container:
                        if c['class'] == ['col-md-12']:
                            element = BeautifulSoup(str(c), 'html.parser')
                            if element.find_all('br') != []:
                                if c.contents[0] != '\n' or c.contents[-1] != '\n':
                                    self.contents.put([str(c.contents), str(poem_link)])
                                    break

                    count += 1
                    # print("Put done")

            self.ids.task_done()


        print("-----------------Thread {} Done-----------------".format(thread))

    def store_content(self):
        try:
            while True:
                content = self.contents.get(timeout=600)
                cursor = self.connection.cursor()
                query = """INSERT INTO poems2(content, url) VALUES(%s, %s)"""

                # Execute query
                cursor.execute(query, (content[0], content[1]))
                self.connection.commit()

                # Close transaction session
                cursor.close()
                self.contents.task_done()
                print("Store content")

        except Exception as e:
            print(e)
            print("Store Content Of Page Done!!!!!!!")
            self.connection.close()


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

    parser = ArgumentParser()
    parser.add_argument("-num_thread", "--num_thread", default=32, type=int)
    parser.add_argument("-start", "--start", default=10000, type=int)
    parser.add_argument("-end", "--end", default=17000, type=int)

    args = parser.parse_args()

    scraper = PoemScraper('url_of_user.csv', start=args.start, end=args.end)
    num_threads = args.num_thread

    for i in range(num_threads):
        worker = Thread(target=scraper.fetch, args=(i+1, ))
        worker.start()

    store_worker1 = Thread(target=scraper.store_content)
    store_worker1.start()

    store_worker2 = Thread(target=scraper.store_content)
    store_worker2.start()



