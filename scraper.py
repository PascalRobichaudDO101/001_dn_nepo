# -*- coding: utf-8 -*- 

import urllib
from bs4 import BeautifulSoup
from bs4 import NavigableString
import csv


def get_links_list (source_url):
    html = urllib.urlopen(source_url)
    soup = BeautifulSoup(html)
    links = soup.findAll('a', {'title':'View opportunity'})
    return links


def get_tender_soup (link):
    tender_url = base_url + link['href']
    tender_html = urllib.urlopen(tender_url)
    tender_soup = BeautifulSoup(tender_html)
    return tender_soup


def get_tender_id (tender_soup):
    if tender_soup.find('div',{"id":"formTitle"}) == None:
        print "+++++++++++++++  No tender ID - aborting (no formTitle div) ++++++++++++++++++++++++"
        exit()
    else:
        if tender_soup.find('div',{"id":"formTitle"}).findNext('h1') == None:
            print "+++++++++++++++  No tender ID - aborting (No H1 tag) ++++++++++++++++++++++++"
            exit()
        else:
            tender_id = tender_soup.find('div',{"id":"formTitle"}).findNext('h1').contents[0]
    return tender_id


def get_contents (tender_soup, tag, text, next_tag):
    if tender_soup.find(tag,text=text) == None:
        item_name = ''
    else:
        item_name = tender_soup.find(tag,text=text).findNext(next_tag).contents[0]
    return item_name


def get_attr_text (tender_soup, tag, attr_type, attr_name): # where we use a tag's attributes to find previous tage and then use getText on next tag
    if tender_soup.find(tag,{attr_type : attr_name}) == None:
        item_name = ''
    else:
        item_name = tender_soup.find(tag,{attr_type : attr_name}).getText()
    return item_name


def get_categories (tender_soup):
    span = tender_soup.find('div',{"id":"shCat_2"}).findNext('span')
    categories = [c.strip() for c in span.contents if isinstance(c, NavigableString)] # turn it into an array
    return categories


def get_text_text (tender_soup, tag, text, next_tag): # for use where we source the next tag by the text of the previous tag, but use getText() to extract the text
    if tender_soup.find(tag,text) == None:
        item_name = ''
    else: 
        item_name = tender_soup.find(tag,text).findNext(next_tag)
    return


def get_address (tender_soup):
    if tender_soup.find('dt',text="Address:") == None:
        contact_addr = ''
    else:
        contact_addr = tender_soup.find('dt',text="Address:").findNext('dd') # get the dirty tag data (is stored in BS tag form)
        contact_addr = unicode(contact_addr) # turn it into a string
        contact_addr = contact_addr.split("<br>") # split into an array
        for i in range(len(contact_addr)): # loop through the array
            contact_addr[i] = BeautifulSoup(contact_addr[i]).text # then use BeautifulSoup to extract the text and save it back into the array
    return contact_addr


def get_attachments (tender_soup):
    attach_list = []
    if tender_soup.find("table", {"class":"altrows attachmentsTable"}) == None:
        pass
    else:
        rows = tender_soup.find("table", {"class":"altrows attachmentsTable"}).find("tbody").findAll("tr")
        for row in rows:
            att_name = row.findAll('td')[0].getText()
            att_size = row.findAll('td')[1].getText()
            att_date = row.findAll('td')[2].getText()
            att_url = row.findAll('td')[0].a['href']

            attach = [att_url,att_name,att_size,att_date]
            
            attach_list.append(attach)
    return attach_list


if __name__ == '__main__':
    base_url = "https://www.londontenders.org"
    links = get_links_list("https://www.londontenders.org/procontract/supplier.nsf/frm_planner_search_results?OpenForm&contains=&cats=&order_by=DATE&all_opps=&org_id=ALL")

    for link in links:

        tender_soup = get_tender_soup(link); # grabs the html of a tender page and soups it.

        tender_id = get_tender_id(tender_soup); # gets the tender_id, no id? then we exit() in huff
        buyer = get_contents(tender_soup, "dt", "Buyer:", "dd"); 
        title = get_contents(tender_soup, "dt", "Title:", "dd");
        summary = get_attr_text(tender_soup,"dd","class","synopsis");
        categories = get_categories(tender_soup);

        contact_name = get_contents(tender_soup,"dt","Contact:","dd");
        contact_phone = get_contents(tender_soup, "dt","Telephone:","dd");
        contact_email = get_text_text(tender_soup, "dt","Email Address:","dd");
        contact_addr = get_address(tender_soup);

        contract_start = get_contents(tender_soup,"label"," Estimated contract start date:","dd");
        contract_end = get_contents(tender_soup, "label"," Estimated contract end date:","dd");
        eoi_start = get_contents(tender_soup, "label","Expression of interest start date:","dd");
        eoi_end = get_contents(tender_soup, "label","Expression of interest end date:","dd");
        est_value = get_contents(tender_soup, "dt"," Estimated Value (£):","dd");
        contract_duration = get_contents(tender_soup, "label","Contract Period:","dd");
        extension_duration = get_contents(tender_soup, "label"," Anticipated Extension Period:","dd");
        extension_iterations = get_contents(tender_soup, "label","Number of Anticipated Extensions:","dd");

        attach_list = []
        attach_list = get_attachments(tender_soup)


        
        


        # add other fields
        # add data to postgres
        # find a way to gather the data out of a google sheet
