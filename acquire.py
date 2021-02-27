import numpy as np
import pandas as pd

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