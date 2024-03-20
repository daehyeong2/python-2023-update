import requests
from bs4 import BeautifulSoup

base_url = "https://weworkremotely.com"
url = "https://weworkremotely.com/categories/remote-full-stack-programming-jobs"

response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

jobs = soup.find("section", {"class": "jobs"}).find_all("li")[1:-1]

all_jobs = []

for job in jobs:
    title = job.find("span", {"class": "title"}).text
    company, position, region = job.find_all("span", {"class": "company"})
    url = job.find("div", {"class": "tooltip--flag-logo"}).next_sibling["href"]
    job_data = {
        "title": title,
        "company": company.text,
        "position": position.text,
        "region": region.text,
        "url": base_url + url
    }
    all_jobs.append(job_data)

print(all_jobs)