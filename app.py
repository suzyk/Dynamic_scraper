from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv

keywords = ["flutter", "golang", "python"]
jobs_db = []

def scrap_jobs():
    # scroll down the page
    for x in range(3):
        page.keyboard.down("End")
        time.sleep(2)
    content = page.content()
    soup = BeautifulSoup(content, "html.parser")
    jobs = soup.find_all("div", class_="JobCard_container__REty8")
    print("---------getting jobs\n")
    for job in jobs:
        url = f"https://www.wanted.co.kr{job.find('a')['href']}"
        title = job.find("strong", class_="JobCard_title__HBpZf").text
        company = job.find("span", class_="JobCard_companyName__N1YrF").text

        job = {
            "title": title,
            "company": company,
            "url": url
        }
        jobs_db.append(job)

p = sync_playwright().start()

browser = p.chromium.launch(headless=False) # using arguments (opposite of positional arguments)
page = browser.new_page()
for key in keywords:
    page.goto(f"https://www.wanted.co.kr/search?query={key}&tab=position")
    scrap_jobs()
    time.sleep(7)


"""
time.sleep(3)
page.click("button.Aside_searchButton__rajGo") # requires CSS selector
time.sleep(3)
page.get_by_placeholder("검색어를 입력해 주세요.").fill("flutter")
time.sleep(3)
page.keyboard.down("Enter")
time.sleep(4)
page.click("a#search_tab_position")
time.sleep(4)
"""

print(f"# of Jobs ------ {len(jobs_db)}\n")
#print(jobs_db)


p.stop()

# create new csv file for each job
# put all the code in functions
# change structure to OOP
# combine all the scrapers for different websites
file = open("jobs.csv", "w")
writer = csv.writer(file)
writer.writerow(["title","company","url"])
for job in jobs_db:
    writer.writerow(job.values())
file.close()