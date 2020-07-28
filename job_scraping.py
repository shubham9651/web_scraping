import requests
from bs4 import BeautifulSoup
import pandas as pd


print('Web scraping of monster website search jobs')
string = '10'
url = 'https://www.monster.com/jobs/search/?q=Software-Developer&stpage=1&page={}'.format(string)
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

job_title = []
job_company = []
job_location = []
job_time = []

results = soup.find(id="ResultsContainer")
python_jobs = results.find_all("h2", string=lambda t: "python" in t.lower())
for p_job in python_jobs:
    link = p_job.find("a")["href"]
    print(p_job.text.strip())
    print(f"Apply here: {link}\n")

for job in soup.find_all('section', class_='card-content'):
    job_titles = job.find('h2', class_='title')
    job_companies = job.find('div', class_='company')
    job_locations = job.find('div', class_='location')
    job_times = job.find('time')
    if(None in (job_titles, job_companies, job_locations)):
        continue
    else:
        job_title.append(job_titles.text.strip())
        job_company.append(job_companies.text.strip())
        job_location.append(job_locations.text.strip())
        job_time.append(job_times.text.strip())


jobs = pd.DataFrame({
    'Title': job_title,
    'Company': job_company,
    'Location': job_location,
    'Time' : job_time
})


file_to_save = 'jobs.csv'
jobs.to_csv(file_to_save,index=False)
print(jobs)
