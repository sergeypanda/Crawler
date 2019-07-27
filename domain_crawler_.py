
#Parse the starting page, looking for <a> tags

#Check the link to see if it stays on-site
#if it stays onsite
    #follow link and repeat

# output all the data found to a spreadsheet - csv
    # title, URL

#TODO 
# add query params, any scripts found to csv

from urllib.parse import urlparse
import requests, csv
from bs4 import BeautifulSoup

class DomainCrawler:

    def __init__(self, starting_url, output_file='output.csv', max_pages=25):
            self.starting_url = starting_url
            self.parsed_starting_url = urlparse(starting_url)
            self.visited_urls = []
            self.csv_file = csv.writer(open(output_file, 'w'), delimiter=',')
            self.csv_file.writerow(['Title', 'Href'])
            self.max_pages = max_pages
            self.processed_pages = 0

    def does_url_stay_onsite(self, href):
        url = urlparse(href)
        if  url.netloc == "" or url.netloc == self.parsed_starting_url.netloc:
            return True
        
    
    def process_page(self, href):
        if self.processed_pages > self.max_pages:
            return
        #get the href
        #soupify the contents
        #extract all links

        url = urlparse(href)
        if 'http' not in url.scheme:
            return

        if url.netloc == '' :
            href = self.parsed_starting_url.scheme + '://'+ \
                   self.parsed_starting_url.netloc + \
                   href

        if href not in self.visited_urls:
            self.visited_urls.append(href)
        else:
            return

        print('processing %s' % href)
        self.processed_pages += 1

        try:
            response = requests.get(href)
            soup = BeautifulSoup(response.text)
            # CSV write title, http response code, full url, 
            self.csv_file.writerow([soup.title.string, href])
        except:
            self.csv_file.writerow(['error', href])
            return


        for a in soup.find_all('a'):
            if self.does_url_stay_onsite(a.get('href')):
                self.process_page(a.get('href'))
            

    def start(self):
        self.process_page(self.starting_url)
        print("+Completed+")

if __name__ == '__main__':
    crawler = DomainCrawler('http://www.sometestsite.com')
    crawler.start()