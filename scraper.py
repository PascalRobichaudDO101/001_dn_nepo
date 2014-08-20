
from bs4 import BeautifulSoup
from urllib2 import urlopen

BASE_URL = "https://www.qtegov.com/"


def make_soup(url):
    html = urlopen(url).read()
    return BeautifulSoup(html, "lxml")
    
    
def get_tender_links(source_url):
    soup = make_soup(source_url)
    section = soup.find("div", "plannerSearch")

    cells = soup.findAll('td')
    
    for cell in cells:
        print cell
        
#       link = cell.a['href']
        
#    tender_links = [BASE_URL + td.a["href"] for td in section.findAll("td")]
    return tender_links


def get_tender_details(tender_url):
    soup = make_soup(tender_url)
    buyer = BeautifulSoup(text).find("dt",text="Buyer:").parent.findNextSiblings("dd")
    title = BeautifulSoup(text).find("dt",text="Title:").parent.findNextSiblings("dd")
    summary = BeautifulSoup(text).find("dt",text="Summary:").parent.findNextSiblings("dd")
    return {"buyer": buyer,
            "title": title,
            "tender_url": tender_url,
            "summary": summary}


if __name__ == '__main__':
    source_url = ("https://www.qtegov.com/procontract/supplier.nsf/frm_planner_search_results?OpenForm&contains=&cats=&order_by=DATE&all_opps=CHECK&org_id=ALL")

    tenders = get_tender_links(source_url)
 
    data = [] # a list to store our dictionaries
    for tender in tenders:
        buyer = get_tender_details(tender)
        data.append(tender)
        sleep(1) # be nice
 
    print data

#    runners_up = [h2.string for h2 in soup.findAll("h2", "boc2")]

