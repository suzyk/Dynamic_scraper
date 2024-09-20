from bs4 import BeautifulSoup
import requests
from util.job import Job

search_url = "https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term="
headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}


def get_wwr_jobs(keyword):
  result = []
  r = requests.get(f"{search_url}{keyword}", headers=headers)

  soup = BeautifulSoup(r.content, "html.parser")

  jobs = soup.find_all("section", class_="jobs")
  for job in jobs:
    title = job.find("span", class_="title").text
    #company = job.find("span", class_ = "company").text
    company, position, *region = job.find_all("span", class_="company")

    url = job.find("div", class_="tooltip--flag-logo").next_sibling["href"]
    # this is how to extract attribute
    url = f"https://weworkremotely.com{url}"
    region = region[0].text.strip(
    ) if region else None  #"No Region" if not region else
    result.append(
        Job(title=title,
            company=company.text.strip(),
            url=url,
            region=region,
            position=position.text.strip()))

  return result
