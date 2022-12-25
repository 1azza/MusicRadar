from turtle import down
import requests
from bs4 import BeautifulSoup, SoupStrainer
from pprint import pprint
import json
class Client:
    def __init__(self):
        pass
    
    def get_all_samples(self):
        print("Fetching data . . .")
        url = "https://www.musicradar.com/news/tech/free-music-samples-royalty-free-loops-hits-and-multis-to-download"
        payload = ""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-GB,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.google.com/",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-User": "?1",
            "TE": "trailers"
        }
        response = requests.request("GET", url, data=payload, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        el = soup.find('h2', {"id": '80-818-free-sample-downloads-a-to-z-2'})
        all_links = el.find_all_next('a', href=True)
        self.samples = {}
        print("Fetching download urls . . .")

        for i in all_links:
            if i.text[0].isnumeric():
                response = requests.request("get", i['href'])
                if i.text == '503 free techno samples':
                    pass
                if response.status_code == 404:
                    download_url = None
                else:
                    num_downloads = (len(response.text.split('.zip')))-2
                    # num_downloads = 1
                    x = 1
                    while x  <= num_downloads:
                        download_url = f"{response.text.split('.zip')[x][5:]}.zip".split(
                            'a-url="')[1]
                        self.samples[download_url] = ({
                            "title" : i.text,
                            "url":i['href'],
                        })
                        x += 2

            else:
                all_links = all_links[:all_links.index(i)]
                break

