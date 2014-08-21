import urllib
from bs4 import BeautifulSoup

base_url = "https://www.qtegov.com/"
source_url = ("https://www.qtegov.com/procontract/supplier.nsf/frm_planner_search_results?OpenForm&contains=&cats=&order_by=DATE&all_opps=CHECK&org_id=ALL")

# pull down the content from the webpage
html = urllib.urlopen(source_url)
soup = BeautifulSoup(html)

blocks = soup.findAll('a', href=True)


for block in blocks:

    link = base_url + block['href']
    
    print link
