from bs4 import BeautifulSoup
import requests
import csv

class PoemScraper:
    def __init__(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
            'Host': 'poem.tkaraoke.com',
            'Origin': 'https://poem.tkaraoke.com',
            'Referer': 'https://poem.tkaraoke.com/'
        }
        self.url = lambda id: 'https://poem.tkaraoke.com/{}/'.format(str(id))

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

if __name__=='__main__':
    scraper = PoemScraper()

    ids, num_poems = scraper.list_id(start=10000, end=16600)
    print("Total poems: {}".format(num_poems))

    f = open('url_of_user.csv', 'w')
    writer = csv.writer(f)
    for id in ids:
        writer.writerow([scraper.url(id)])



