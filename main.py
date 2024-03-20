import requests
from bs4 import BeautifulSoup

url = "https://weworkremotely.com/remote-full-time-jobs"

all_jobs = []

def get_pages(url):
    response = requests.get(f"{url}?page=1")
    soup = BeautifulSoup(response.content, "html.parser")
    last = soup.find("span", {"class": "last"})
    if last:
        return int(last.find("a")["href"].split("?page=")[1])
    else:
        return False

def scrape_page(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    jobs = soup.find("section", {"class": "jobs"}).find_all("li")[1:-1]


    for job in jobs:
        title = job.find("span", {"class": "title"}).text
        company, position, region = job.find_all("span", {"class": "company"})
        url = job.find("div", {"class": "tooltip--flag-logo"}).next_sibling["href"]
        job_data = {
            "title": title,
            "company": company.text,
            "position": position.text,
            "region": region.text,
            "url": "https://weworkremotely.com" + url
        }
        all_jobs.append(job_data)

total_pages = get_pages(url)

if total_pages:
    if(total_pages>=2):
        total_pages = int(input(f"{total_pages}개의 페이지를 찾았습니다. 몇 페이지까지 추출 하시겠습니까?: "))
    else:
        print(f"{total_pages}개의 페이지를 찾았습니다.")
    for page in range(1, total_pages+1):
        print(f"{page}페이지 요청 중.. ({page}/{total_pages})")
        scrape_page(f"{url}?page={page}")
    print(f"총 {len(all_jobs)}개의 일자리를 찾았습니다.")
else:
    print("1개의 페이지가 있습니다.")
    print("1페이지 요청 중... (1/1)")
    scrape_page(url)
    print(f"총 {len(all_jobs)}개의 일자리를 찾았습니다.")