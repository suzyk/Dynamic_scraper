import requests
from bs4 import BeautifulSoup
from util.job import Job

search_url = "https://berlinstartupjobs.com/skill-areas/"
headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}

def get_berlin_jobs(keyword):
    result = []
    response = requests.get(f"{search_url}{keyword}", headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    jobs = soup.find('ul', class_="jobs-list-items").find_all("li", class_="bjs-jlid")
    # result 8
    for job in jobs:
        title = job.find("h4", class_="bjs-jlid__h").find("a", href=True)
        link = title["href"]
        title = title.text
        company = job.find("a", class_="bjs-jlid__b").text
        #description = job.find("div", class_="bjs-jlid__description").text.strip()
        result.append(Job(title, company, link))
    return result
 