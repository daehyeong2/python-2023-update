import requests
from bs4 import BeautifulSoup

class Scrapper:
    def __init__(self):
        self.scrapped_keyword = []
        self.all_jobs = []
    def scrape_data(self, url):
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"})
        soup = BeautifulSoup(response.content, "html.parser")
        headers = soup.find_all("a", {"class": "preventLink"})[1::2]
        for header in headers:
            expired = bool(header.findNext("div", {"class": "description"}).find("strong", recursive=False))
            if expired:
                continue
            title = header.find("h2").text.replace("\t", "").replace("\n", "")
            company = header.findNext("h3", {"itemprop": "name"}).text.replace("\t", "").replace("\n", "")
            location = header.findNext("div", {"class": "location"}).text
            salary = header.findNext("div", string=lambda x: x and "💰" in x).text.replace("*", "")
            url = "https://remoteok.com" + header["href"]
            if header["href"] == "/remote-jobs/":
                continue
            job_data = {
                title: title,
                company: company,
                location: location,
                salary: salary,
                url: url
            }
            self.all_jobs.append(job_data)
    def scrape(self, keyword, data_range):
        if data_range > 50: raise Exception("data_range는 50 이하의 숫자만 넣어야 합니다.")
        if isinstance(keyword, list) and len(keyword) > 1:
            print(f"약 {data_range*20*len(keyword)}개의 일자리를 검색하겠습니다. (일자리가 {data_range*20*len(keyword)}개만큼 없어도 최대한 검색합니다.)")
            for search_keyword in keyword:
                if search_keyword in self.scrapped_keyword: continue
                for offset in range(data_range):
                    print(f"{search_keyword}: {offset+1}페이지 요청 중.. ({offset+1}/{data_range})")
                    self.scrape_data(f"https://remoteok.com/?tags={search_keyword}&action=get_jobs&offset={offset*20}")
                self.scrapped_keyword.append(search_keyword)
        else:
            if isinstance(keyword, list): search_keyword = keyword[0]
            else: search_keyword = keyword
            if search_keyword in self.scrapped_keyword: return
            print(f"약 {data_range*20}개의 일자리를 검색하겠습니다. (일자리가 {data_range*20}개만큼 없어도 최대한 검색합니다.)")
            for offset in range(data_range):
                print(f"{search_keyword}: {offset+1}페이지 요청 중.. ({offset+1}/{data_range})")
                self.scrape_data(f"https://remoteok.com/?tags={search_keyword}&action=get_jobs&offset={offset*20}")
            self.scrapped_keyword.append(search_keyword)
        print(f"{len(scrapper.all_jobs)}개의 일자리를 찾았습니다.")

scrapper = Scrapper()

scrapper.scrape(
    keyword=["python", "react"],
    data_range=3
)