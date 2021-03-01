import numpy as np
import pandas as pd
from datetime import datetime
from requests import get
from bs4 import BeautifulSoup
from time import sleep
import os

def make_soup(url):
    '''
    This helper function takes in a url and parses HTML
    returning a soup object.
    '''
    headers = {'User-Agent': 'brandmarz'} 
    response = get(url, headers=headers)    
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def get_job_urls():
    '''
    This function scrapes the default LinkedIn search page 
    for the first 25 pages and returns a list of urls.
    '''
    # create empty list to hold urls
    urls = []
    # create list of jobs to search for
    jobs = ['data%20scientist', 'data%20analyst', 'data%20engineer', 'machine%20learning%20engineer']
    # loop through the jobs to obtain urls for each one
    for job in jobs:
        # loop through the every 25 entries (1 page) to contiuously get job urls
        count = 0
        for i in range(0,16):
            # each page for each job type
            url = f'https://www.linkedin.com/jobs/search/?f_L=United%20States&geoId=103644278&keywords={job}&location=United%20States&start={count}'
            # append the url to the urls list
            urls.append(url)
            # add 25 to the start to get the next set of entries
            count += 25
    return urls

def get_all_urls(urls):
    '''
    This function scrapes all of the urls from
    the URLS list and returns a complete list of urls.
    '''
    # create empty list
    repo_urls = []
    n=0
    # loop through each url in urls list
    for url in urls:
        # Make request and soup object using helper function
        soup = make_soup(url)
        # delay 1 second between fetch
        sleep(8)
        n = n + 1
        print(f"Scraping loop number {n}")
        # Create a list of the anchor elements that hold the urls.
        urls_list = soup.find_all('a', class_='v-align-middle')
        # I'm using a set comprehension to return only unique urls.
        urls_set = {'https://github.com' + link.get('href') for link in urls_list}
        # I'm converting my set to a list of urls.
        urls_set = list(urls_set)
        # extend the list with a new url as an element
        repo_urls.extend(urls_set)        
    return repo_urls

def get_record(card):
    '''
    Extract job data from a single record
    '''
    # access the 'a' tag that corresponds to the job title
    atag = card.h2.a
    # get the title text as a string
    job_title = atag.get('title')
    # get the url of the job using the root
    job_url = 'https://www.indeed.com' + atag.get('href')
    # get the company name 
    company = card.find('span', class_='company').text.strip()
    # get job location
    job_location = card.find('div' , class_='recJobLoc').get('data-rc-loc')
    # get job summary (need to replace with entire job description)
    job_summary = card.find('div', class_='summary').text.strip().replace('\n', ' ')
    # when the job was posted relative to today
    post_date = card.find('span', class_='date').text
    # today's date
    today = datetime.today().strftime('%Y-%m-%d')
    # get the job salary
    try:
        job_salary = card.find('span', class_='salaryText').text.strip()
    except AttributeError:
        job_salary = ''

    # use tuple to assign each record's data
    record = (job_title, company, job_location, post_date, job_summary, job_salary, job_url)

    return record