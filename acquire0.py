import numpy as np
import pandas as pd
from datetime import datetime
from requests import get
from bs4 import BeautifulSoup
from time import sleep
import os

def make_soup(url):
    '''
    This helper function takes in a url and uses requests module to
    parse HTML from the page returning a soup object. We can then use
    the soup object to call various methods to get the parts of the page
    that we need like, job title, and links to job postings. UPDATE:
    implemented random string generator to get passed CAPTCHA when scrapping
    '''
    import random
    import string
    
    rand_string = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(10))
    print(f'User: {rand_string}')
    headers = {'User-Agent': rand_string} 
    response = get(url, headers=headers)    
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def get_search_urls():
    '''
    This function scrapes the Indeed search results pages for each of 4 
    job labels for the first 10 pages of each and returns a list of all
    the urls.
    '''
    # create empty list to hold urls
    urls = []
    # create list of job titles to search for
    jobs = ['data scientist', 'data analyst', 
        'data engineer', 'machine learning engineer']
    
    # loop through each job
    for job in jobs:
        count = 0
        # loop through each page until
        for i in range(1,16):
            # each page for most starred repos on GH
            url = f'https://www.indeed.com/jobs?q={job}&l=United+States&start={count}'
            # append the url to the urls list
            urls.append(url)
            # add 10 to the start to get the next set of entries (next page)
            count += 10
    return urls

def get_all_cards(urls):
    '''
    This function scrapes the url from each job card within each page of 
    the search result urls and returns a complete list of urls for each job.
    UPDATE: added random number generator to get past Captcha'''
    # create empty list
    job_urls = []
    n = 0
    # loop through each url in urls list
    for url in urls:
        # generates a random number between 1 and 8
        # to simulate "human" like activity
        import random
        rand_int = random.randint(1,9)
        print(f'Interval {rand_int}')
        # Make request and soup object using helper function
        soup = make_soup(url)
        # delay 1 second between fetch
        sleep(rand_int)
        n = n + 1
        print(f"Scraping loop number {n}")
        # Create a list of the divider elements that hold the job cards.
        card_list = soup.find_all('div', class_='jobsearch-SerpJobCard')
        # I'm using a set comprehension to return only unique urls.
        card_set = {'https://www.indeed.com' + card.h2.a.get('href') for card in card_list}
        # I'm converting my set to a list of urls.
        card_set = list(card_set)
        # extend the list with a new url as an element
        job_urls.extend(card_set)        
    return job_urls

def get_job_content(urls, i, cached=False):
    '''
    This function takes in a list of Job urls and a parameter
    with default cached == False which scrapes the job_title, and  
    readme text for each url, creates a list of dictionaries with 
    the title and text for each blog, converts list to df, and returns 
    df. If cached == True, the function returns a df from a json file..

    Try and except statements are in place in case a variable isn't indicated.
    We will replace it with an empty string
    '''
    if cached == True:
        df = pd.read_json(f'indeed-data-jobs{i}.json')
        
    # cached == False completes a fresh scrape for df     
    else:
    
        # Create an empty list to hold dictionaries
        records = []
        n = 0
        # Loop through each url in our list of urls
        for url in urls:
        # generates a random number between 1 and 8
        # to simulate "human" like activity            
            import random
            rand_int = random.randint(1,5)
            # Make request and soup object using helper
            soup = make_soup(url)
            sleep(rand_int)
            n = n + 1
            print(f"Loop number: {n}")
            print(f'Interval: {rand_int} seconds \n')
            # access the job title
            try:
                job_title = job_title = soup.find('h1', 'icl-u-xs-mb--xs icl-u-xs-mt--none jobsearch-JobInfoHeader-title').text.strip()
            except AttributeError:
                job_title = ''
            
            # access the company
            try:
                company = soup.find('div', 'icl-u-lg-mr--sm icl-u-xs-mr--xs').text.strip()
            except AttributeError:
                company = ''

            # access the location
            try:
                location = soup.find('div', 'icl-u-xs-mt--xs icl-u-textColor--secondary jobsearch-JobInfoHeader-subtitle jobsearch-DesktopStickyContainer-subtitle').contents[1].text
            except AttributeError:
                location = ''
            
            # is the position remote
            try:
                if soup.find('div', 'icl-u-xs-mt--xs icl-u-textColor--secondary jobsearch-JobInfoHeader-subtitle jobsearch-DesktopStickyContainer-subtitle').contents[2].text != None:
                    remote = 1
            except IndexError:
                remote = 0
            except AttributeError:
                remote = 0

            # access salary
            try:
                salary = soup.find('span', 'icl-u-xs-mr--xs').text
            except AttributeError:
                salary = ''
            
            # access post date from access
            try:
                if (soup.find('div', 'jobsearch-JobMetadataFooter').contents[1].text)[0].isdigit():
                    post_date = soup.find('div', 'jobsearch-JobMetadataFooter').contents[1].text
                elif (soup.find('div', 'jobsearch-JobMetadataFooter').contents[0].text)[0].isdigit():
                    post_date = soup.find('div', 'jobsearch-JobMetadataFooter').contents[0].text
            except AttributeError:
                post_date = ''

            # today's date
            today = datetime.today().strftime('%Y-%m-%d')

            # access full job description text
            try:
                job_description = soup.find('div', {'id':'jobDescriptionText', 'class':'jobsearch-jobDescriptionText'}).text.strip().replace('\n', ' ')
            except AttributeError:
                job_description = ''
                print('^ NO JOB DESC, Check Record. \n')

            # Create a dictionary holding the variables for each job
            job = {'job_title': job_title, 'company': company, 'location': location, 
                'is_remote': remote, 'salary': salary, 'post_date': post_date, 
                'date_accessed': today, 'job_description': job_description}

            # Add each dictionary to the records list of dictionaries
            records.append(job)
            
        # convert our list of dictionaries to a df
        df = pd.DataFrame(records)

        # Write df to a json file for faster access
        # "i" is a number to indicate a file with a different set of records
        df.to_json(f'indeed-data-jobs{i}.json')
    
    return df