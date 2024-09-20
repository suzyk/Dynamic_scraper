import requests
from util.job import Job
from bs4 import BeautifulSoup

headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"}
def parse_html(content):
    result = []
    soup = BeautifulSoup(content, "html.parser")
    jobs = soup.find("table", id = "jobsboard").find_all("tr", class_ = "job")

    for job in jobs:
        title = job.find("h2").text
        company = job.find("h3").text

        region_salary = job.find_all("div", class_ = "location")
        region = ""
        salary = ""
    
        if len(region_salary) > 0 :
            all_regions = []
            for i in region_salary:# everything except last item
                if "$" in i.text:
                    salary = i.text
                    break  # do not care after salary info
                else:
                    all_regions.append(i.text)
            region = ", ".join(all_regions)  
        
        region = "No region" if len(region) == 0 else region
        salary = "No salary info" if len(salary) == 0 else salary
    
        #another way
        #url = job.find("a", itemprop="url")["href"]
        url = job.find("a", class_ = "preventLink")["href"]
        result.append(Job(title.strip(), company.strip(), f"https://remoteok.com{url}", region.strip(), salary.strip()))
    return result

def scrape_remoteok_jobs(keyword, testing=False):
    if not testing:
      url = f"https://remoteok.com/remote-{keyword}-jobs"
      r = requests.get(url, headers=headers)

      if (r.status_code == 200):
        return parse_html(r.content)
      else:
        print(f"request error with {r.content}")
        return []
    else: #read local file for test
      url = f"html/remoteok_{keyword}.html"
      f = open(url, encoding="utf8")
      result = parse_html(f)
      f.close()
      return result
