from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv

class Scrapper:
    def __init__(self):
        self.p = sync_playwright().start()
        self.browser = self.p.chromium.launch(headless=False)
    def scrape_page(self, keyword, scroll_count=3, scroll_delay=0.5):
        if isinstance(keyword, list) == False:
            raise Exception("keyword는 배열이여야 합니다.")
        for search_keyword in keyword:
            page = self.browser.new_page()
            page.goto(f"https://www.wanted.co.kr/search?query={search_keyword}&tab=position")

            for i in range(scroll_count):
                page.keyboard.down("End")
                time.sleep(scroll_delay)

            content = page.content()

            page.close()

            soup = BeautifulSoup(content, "html.parser")

            jobs = soup.find_all("div", {"class": "JobCard_container__FqChn"})

            jobs_db = []

            for job in jobs:
                link = f"https://wanted.co.kr{job.find('a')['href']}"
                title = job.find("strong", {"class": "JobCard_title__ddkwM"}).text
                company_name = job.find("span", {"class": "JobCard_companyName__vZMqJ"}).text
                reward = job.find("span", {"class": "JobCard_reward__sdyHn"}).text
                job = {
                    "title": title,
                    "company_name": company_name,
                    "reward": reward,
                    "link": link
                }
                jobs_db.append(job)

            file = open(f"{search_keyword}.csv", "w")
            writer = csv.writer(file)
            writer.writerow(["Title", "Company", "Reward", "Link"])

            for job in jobs_db:
                writer.writerow(job.values())

            file.close()
    def close(self):
        self.p.stop()

scrapper = Scrapper()

scrapper.scrape_page(["python", "react"], 5, 1)

scrapper.close()