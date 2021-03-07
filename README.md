# Data Job Resume Booster
## About the Project
### Goals
- Build a dataset of job postings with the field of data science, analytics, etc.
- Create labels for each job posting; for example, data scientist, data engineer, etc.
- Develop a machine learning model to classify a job based on description text
- Identify the most common words and phrases for each label

### Background

>As a Data Scientist seeking a job in-field, I thought it would be fun and useful to practice my skills using NLP to classify jobs based on the posting descriptions from popular sites like LinkedIn. 
>
>Many candidates starting their search may have their resume's sidestepped by recruiters or a company's ATS system. I want to build a list of common words and phrases that each job title uses to hopefully increase candidate's chances by tailoring their individual skills/experience to match the job closer.

### Deliverables
- A script that runs the classification model
- A CSV of the most common words and phrases for each job title

### Acknowledgments
- Data scrapped from [Indeed](https://www.indeed.com)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#kinds-of-objects)
- Project inspired by [Codeup](https://codeup.com/)'s NLP Project
- Getting past [CAPTCHA](https://proxyway.com/guides/how-to-bypass-captcha)'s
- Inspiration for building scrapper: [here](https://github.com/israel-dryer/Indeed-Job-Scraper)

## Data Dictionary
## Initial Thoughts & Hypotheses
### Thoughts
- I'll need to make sure my data is representative by including a variety of industries, balanced data from each label, and locations.
- I need to create the labels for each job posting using regex, manually, or some form of normalization.
- Each observation is a single job posting
- I'll use the BeatifulSoup Library to webscrape and collect my data
- Find n-grams, verbs, and phrases within the exploratory phase
- Normalize, tokenize, stem or lemmatize words, and remove stop words
- Features to include:
  - Job Title (original) 
  - Job label - target
  - Company
  - Location
  - Remote - binary category
  - Seniority level 
  - Industry
  - Job description - word vectors
  - Top skills - word vectors
  - Benefits - word vectors

### Hypotheses

## Project Steps
### Acquire
Created a series of functions to extract the data from indeed using the Beautiful Soup library. The idea was to parse the html of each job posting and reference different elements to obtain each variable.
1. `make_soup`: takes in a url and uses the requests module to parse HTML from the page returning a soup object. We can then use the soup object to call various methods to get the parts of the page that we need like, job title, and job description. I had to implement a random string generator as a user agent to get past CAPTCHA when scrapping (see acknowledgements). This is because a website detects strange activity like scrapping too frequently.
2. `get_search_urls`:  scrapes the Indeed search results pages for each of 4 job titles (data scientist, data analyst, data engineer, and machine learning engineer) for the first 10 pages of each and returns a list of all the urls. I ended up with 60 urls (15 pages for each job title).
3. `get_all_cards`: This function scrapes the url from each job card within each page of the search result urls and returns a complete list of urls for each job. I had to implement random number generator to use a delay timer to get past CAPTCHA (see acknowledgements). I ended up with 904 unique job postings. I also saved the list of urls locally as a text file so that I have them saved for later use/reproducibility.
4. `get_job_content`: takes in a list of job urls and a parameter with default cached == False which scrapes the job_title, company, location, remote, salary, post_date, access_date, and job_description for each url, creates a list of dictionaries with the features mentioned for each job, converts list to df, and returns df. If cached == True, the function returns a df from a json file. Try and except statements are in place in case a variable isn't indicated. We will replace it with an empty string
5. **Takeaways**: I ran the `get_job_content` function in 5 separate parts to essentially save my progress in case I happened to run into an error with the url's content while scrapping. Finally I used pandas to concatenate them into a single dataframe for preparation and preprocessing.

### Prepare
### Explore
### Model
### Conclusions
## How to Reproduce
### Steps
### Tools & Requirements
Python | Pandas | Requests | Bs4 | Time | Datetime | Sci-Kit Learn
## License
Standard License 
## Creators
Brandon Martinez
