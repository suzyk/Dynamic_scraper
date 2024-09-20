from bs4 import BeautifulSoup
import requests
from util.job import Job

search_url = "https://web3.career/"
headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}


def get_web3_jobs(keyword):
  result = []
  r = requests.get(f"{search_url}{keyword}-jobs", headers=headers)

  soup = BeautifulSoup(r.content, "html.parser")

  jobs = soup.find("tbody", class_="tbody").find_all("tr", class_="table_row")
  for job in jobs:
    if "id" not in job.attrs:
        div = job.find("div", class_="job-title-mobile")
        title = div.find("h2").text.strip()
        #print(f"title = {title}")
        company = job.find("h3").text.strip()
        url = div.find("a", href=True)["href"]
        region = job.find("td", class_="job-location-mobile").find("a", href=True).text
          #26 python -1 sponsor
        url = f"https://web3.career{url}"
        result.append(
            Job(title=title,
                company=company,
                url=url,
                region=region))
    
  return result
