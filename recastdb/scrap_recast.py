#!/usr/bin/python

import urllib2
from bs4 import BeautifulSoup

'''
   a script to import data from the 

     recast.perimeterinstitute.ca

'''

from database import db

from models import Analysis
from models import ScanRequest
import json

db.create_all()


url_link = "http://recast.perimeterinstitute.ca/?q=analyses-catalog"

def process_analysis_page(s):
    #soup.tbody   # for the tbody tag
    #print s.tbody.tr.a.string
    #to get url of a page do
    # soup.tbody.a['href'] and append the url of web site
    new_url_link = url_link + soup.tbody.a['href']

    str_list_analysis = []
    for i in s.tbody.find_all('a'):

        if i.string == "view":
            continue
        new_url_link = "http://recast.perimeterinstitute.ca/" + i['href']

        node_number = "node-"+new_url_link[-3:]
        #download the page
        page = urllib2.urlopen(new_url_link).read()
        
        #Now lets try to hack things so we can parse all the variables of interest on this page
        good_page = BeautifulSoup(page, 'html.parser')
        
        for i in good_page.find_all('div'):
            try:
                if i['id'] == node_number:
                    #print i.text
                    #str_list_request.append(i.text)
                    str_list_analysis.append(i.text)
            except:
                continue


    return str_list_analysis






def process_request_page(s):
    
    ''' 
    to scrap requests page 
        returns list of requests
    '''
    counter = 0
    str_list_request = []
    for i in s.tbody.find_all('a'):
        if len(i.text) > 10:
            continue
        
        #open the page for the request
        new_url_link = "http://recast.perimeterinstitute.ca/" + i['href']
        
        node_number = "node-"+new_url_link[-3:]
        
        page = urllib2.urlopen(new_url_link).read()

        good_page = BeautifulSoup(page, 'html.parser')
                
        for i in good_page.find_all('div'):
            try:
                if i['id'] == node_number:
                    #print i.text
                    str_list_request.append(i.text)
            except:
                continue

    return str_list_request




def make_request_dict(request_list):
    
    '''
    return dict or request label and the string in the text box
    (Not perfect but will parse necessary info)
    '''    
    request_dict_list = []

    for l in request_list:
        lines = l.split("\n")
        lines = [line for line in lines if line.strip()]          

        for i in range(len(lines)):
            if lines[i].endswith(":"):
                if not lines[i+1].endswith(":"):
                    lines[i] = lines[i] + lines[i+1]
                    lines[i+1] = "\n"

        for i in range(len(lines)):
            try:
                lines.remove("\n")
            except:
                continue
        
        new_dict = {}
    
        for i in range(len(lines)):
            
            if i == 0:
                continue
            if lines[i] == "Request Parameter Points":
                continue
            if lines[i] == "Request Description and Potential":
                continue

            try:
                tup = lines[i].split(":")
                new_dict[tup[0]] = tup[1]
            except:
                continue
    
        request_dict_list.append(new_dict)

    return request_dict_list
        

def make_analysis_dict(analysis_list):
    
    '''
    same as dict for request, but for analysis stuff
    '''
    analysis_dict_list = []
    
    for l in analysis_list:
        lines = l.split("\n")
        lines = [line for line in lines if line.strip()]
        
        for i in range(len(lines)):
            if i < (len(lines)-1):
                if lines[i].endswith(":"):
                    if not lines[i+1].endswith(":"):
                        if lines[i+1].find(":") == -1:
                            if lines[i+1].find("Unclaimed") == -1:
                                lines[i] = lines[i] + lines[i+1]
                                lines[i] = "\n"

        for i in range(len(lines)):
            try:
                lines.remove("\n")
            except:
                continue

        new_dict = {}

        for i in range(len(lines)):

            if lines[i].find("Unclaimed") != -1:
                continue
            if lines[i].find("Run Conditions") != -1:
                break

            try:
                tup = lines[i].split(":")        
                new_dict[tup[0]] = tup[1]
            except:
                continue
        
        analysis_dict_list.append(new_dict)
        
    return analysis_dict_list


#Analysis page
content = urllib2.urlopen(url_link).read()
soup = BeautifulSoup(content, 'html.parser')
print "Fetching analysis page.... "
analysis_list = process_analysis_page(soup)
print "analysis page to dict ... "
analysis_dict_list = make_analysis_dict(analysis_list)

#Request stuff
request_url = "http://recast.perimeterinstitute.ca/?q=requests"
request_content = urllib2.urlopen(request_url).read()
request_soup = BeautifulSoup(request_content, 'html.parser')
print "Fecthing request page.... "
request_list = process_request_page(request_soup)
print "request page to dict... "
request_dict_list = make_request_dict(request_list)


request_jsonarray = []

for i in range(len(request_dict_list)):
    request_jsonarray.append(json.dumps(request_dict_list[i], ensure_ascii=False))

analysis_jsonarray = []

for i in range(len(analysis_dict_list)):
    analysis_jsonarray.append(json.dumps(analysis_dict_list[i], ensure_ascii=False))





'''
print "Adding analysis to db.... "
#Now lets retrieve data and input into the db
analysis = []

for i in range(len(analysis_dict_list)):
    temp_analysis = Analysis()
    for k in analysis_dict_list[i]:

        # this is where we will add fields we want to input into the db
        if k == "Description":
            temp_analysis.description_of_original_analysis=analysis_dict_list[i][k]

    analysis.append(temp_analysis)
    

for a in analysis:
    db.session.add(a)

db.session.commit()
    

print "Adding request to db.... "
#Request case
requests = []
for i in range(len(request_dict_list)):
    temp_request = ScanRequest()    

    for k in request_dict_list[i]:
        
        if k == "Model Name":
            temp_request.description_of_model = request_dict_list[i][k]

    requests.append(temp_request)

for s in requests:
    db.session.add(s)

db.session.commit()

print "DONE.... "
'''
