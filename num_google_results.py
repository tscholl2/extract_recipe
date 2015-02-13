import re
import datetime
import requests
from bs4 import BeautifulSoup
import progressbar

REGEX = r'About (.*) results'

def number_of_search_results(key):
    def extract_results_stat(url):
        headers = { 
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/21.0'
        }
        search_results = requests.get(url, headers=headers, allow_redirects=True)
        soup = BeautifulSoup(search_results.text)
        result_stats = soup.find(id='resultStats')
        m = re.match(REGEX, result_stats.text)
        # print m.group(1)
        return int(m.group(1).replace(',',''))

    google_main_url = 'https://www.google.co.in/search?q=' + key
    google_news_url = 'https://www.google.co.in/search?hl=en&gl=in&tbm=nws&authuser=0&q=' + key
    return extract_results_stat(google_main_url)
    
numLines = 0
with open('foods.txt') as f:
  for line in f:
    if len(line)>3:
      numLines = numLines + 1

bar = progressbar.ProgressBar(maxval=numLines,widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    
foods = {}
i = 0
with open('foods.txt') as f:
  for line in f:
    if len(line)>3:
      i = i+1
      bar.update(i)
      foods[line.strip()]=number_of_search_results(line.strip())

d_view = [ (v,k) for k,v in foods.iteritems() ]
d_view.sort(reverse=True) # natively sort tuples by first element
for v,k in d_view:
    print "%s: %d" % (k,v)
