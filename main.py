import requests
from bs4 import BeautifulSoup

url = "https://weworkremotely.com/categories/remote-full-stack-programming-jobs"

response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")

jobs = soup.find("section", {"class": "jobs"}).find_all("li")

print(jobs)