#!/usr/bin/env python
import urllib2
import json
import collections
import mysql.connector
from bs4 import BeautifulSoup


#Construct the URL for the Sunlight Foundation API
apikey = ''
root = 'https://congress.api.sunlightfoundation.com/'
method = 'legislators'
qing = '?per_page=all'
url = root+method+qing+'&apikey='+apikey

#Send the request and process the result
request = urllib2.Request(url)
output = json.load(urllib2.urlopen(request))


#Iterate through the request and build a dictionary of congress_facts (bioguide_id,birthday,oc_email,title,first_name,last_name,state,district,party,phone,twitter_id,facebook_id)
congress_facts = {}
for result in output['results']:
    single_congress_fact = {}
    single_congress_fact['bioguide_id'] = result.get('bioguide_id').decode()
    single_congress_fact['birthday'] = result.get('birthday')
    single_congress_fact['oc_email'] = result.get('oc_email').decode()
    single_congress_fact['title'] = result.get('title')
    single_congress_fact['first_name'] = result.get('first_name')
    single_congress_fact['last_name'] = result.get('last_name')
    single_congress_fact['state'] = result.get('state')
    single_congress_fact['district'] = result.get('district')
    single_congress_fact['party'] = result.get('party')
    single_congress_fact['phone'] = result.get('phone')
    single_congress_fact['twitter_id'] = result.get('twitter_id')
    single_congress_fact['facebook_id'] = result.get('facebook_id')
    congress_facts[result.get('bioguide_id')] = single_congress_fact

#Open MySQL Connector
cnx = mysql.connector.connect(user='', password='', database='congress')
cursor = cnx.cursor()

#Run a query to drop and add the congress_members table
sqla=("""drop table if exists congress_members""")
sqlb=(""" create table congress_members (
    bioguide_id varchar(255),
    birthday date,
    oc_email varchar(255),
    title varchar(255),
    first_name varchar(255),
    last_name varchar(255),
    state varchar(255),
    district int,
    party varchar(255),
    phone varchar(255),
    twitter_id varchar(255),
    facebook_id varchar(255),
    PRIMARY KEY (bioguide_id)
)
""")
cursor.execute(sqla)
cursor.execute(sqlb)

#Add members of congress to the list
def add_congress_member(single_congress_member):
    sqlq = ("""INSERT INTO congress_members (bioguide_id,birthday,oc_email,title,first_name,last_name,state,district,party,phone,twitter_id,facebook_id)
    VALUES(%(bioguide_id)s,%(birthday)s,%(oc_email)s,%(title)s,%(first_name)s,%(last_name)s,%(state)s,%(district)s,%(party)s,%(phone)s,%(twitter_id)s,%(facebook_id)s)""")
    cursor.execute(sqlq, single_congress_member)
    pass

#Loop through and call add_congress_member
for single_congress_member in congress_facts.values():
    add_congress_member(single_congress_member)

sqla = ("""drop table if exists congress_bios""")

sqlb = ("""create table congress_bios (
    bioguide_id varchar(255),
    bio_text blob,
    img_src varchar(255),
    PRIMARY KEY (bioguide_id))""")

cursor.execute(sqla)
cursor.execute(sqlb)

def add_biography(bioguide_id):
    bio_url = "http://bioguide.congress.gov/scripts/biodisplay.pl?index=" + bioguide_id
    data = urllib2.urlopen(bio_url)
    soup = BeautifulSoup(data)
    bio = soup.find_all('p')
    bio_text=str(bio)
    photo_url="//bioguide.congress.gov/bioguide/photo"
    for img_soup in soup.find_all('img'):
        img_src = ""
        img_str = str(img_soup)
        if photo_url in img_str:
            img_src="http:" + img_str[img_str.find('\"')+1:img_str.rfind('\"')]
    cursor.execute("""INSERT INTO congress_bios(
    bioguide_id,bio_text,img_src)
    VALUES(%s, %s, %s)""", (bioguide_id,bio_text,img_src))
    pass

for bioguide_id in congress_facts.keys():
    add_biography(bioguide_id)
