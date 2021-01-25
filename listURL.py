# Import dependencies
from bs4 import BeautifulSoup
import requests
from urllib.parse import quote
from pprint import pprint
import csv

class GoogleSpider(object):
    def __init__(self):
        """Crawl Google search results

        This class is used to crawl Google's search results using requests and BeautifulSoup.
        """
        super().__init__()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:79.0) Gecko/20100101 Firefox/79.0',
            'Host': 'www.google.com',
            'Referer': 'https://www.google.com/'
        }

    def __get_source(self, url: str) -> requests.Response:
        """Get the web page's source code

        Args:
            url (str): The URL to crawl

        Returns:
            requests.Response: The response from URL
        """
        return requests.get(url, headers=self.headers, )

    def search(self, query, start = 0):
        """Search Google

        Args:
            query (str): The query to search for

        Returns:
            list: The search results
        """
        # Get response
        response = self.__get_source('https://www.google.com/search?q={}&start={}'.format(quote(query), str(start*10)))
        # Initialize BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        # Get the result containers
        result_containers = soup.findAll('div', class_='g')
        # Final results list
        results = []
        # Loop through every container
        for container in result_containers:
            # Result title
            try:
                title = container.find('h3').text
            except Exception as e:
                title = ""
                print(e)
            # Result URL
            try:
                url = container.find('a')['href']
            except Exception as e:
                url = ""
                print(e)
            # Result description
            try:
                des = container.find('span', class_='st')
            except Exception as e:
                des= ""
                print(e)
            results.append({
                'title': title,
                'url': url,
                'des': des
            })
        return results


if __name__ == '__main__':
    f = open('./mua_xuan.csv', 'a+')
    urls= list()
    writer = csv.DictWriter(f, fieldnames=['url'])


    for query in ['thơ về mùa xuân', 'những bài thơ mùa xuân', 'thơ hay về mùa xuân','thơ chúc tết']:
        for page in range(0, 9):
            print("query:", query)
            print(page)
            result = GoogleSpider().search(query , start=page)
            print(result)
            for dictionary in result:
                url = dictionary['url']
                if url not in urls:
                    urls.append(url)
                    print(url)

    for url in urls:
        writer.writerow({'url': url})

    f.close()
