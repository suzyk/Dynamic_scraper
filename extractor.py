from playwright.sync_api import sync_playwright
import requests
from job import Job
import time
from bs4 import BeautifulSoup
from file import save_to_file

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

keywords = ["flutter", "golang", "python"]
jobs_db = []

def scrape_wanted_jobs():
  def scrape_jobs(page):

    # scroll down the page
    for x in range(3):
        page.keyboard.down("End")
        time.sleep(2)
    content = page.content()
    soup = BeautifulSoup(content, "html.parser")
    jobs = soup.find_all("div", class_="JobCard_container__REty8")
    
    for job in jobs:
        url = f"https://www.wanted.co.kr{job.find('a')['href']}"
        title = job.find("strong", class_="JobCard_title__HBpZf").text
        company = job.find("span", class_="JobCard_companyName__N1YrF").text

        jobs_db.append(Job(title.strip(), company.strip(), url.strip())) #removes newline character
  
  p = sync_playwright().start()

  browser = p.chromium.launch(headless=False) # using arguments (opposite of positional arguments)
  page = browser.new_page()
  for key in keywords:
    jobs_db.clear() #reset db for each job position
    page.goto(f"https://www.wanted.co.kr/search?query={key}&tab=position")
    scrape_jobs(page)
    time.sleep(7)
    save_to_file(f"wanted_{key}", jobs_db)
  p.stop()


def scrape_weworkremotely(testing=False):

  def parse_html(content):
    soup = BeautifulSoup(content, "html.parser")

    #used to be category-2
    jobs = soup.find("section", class_ = "jobs").find_all("li")[0:-1] # eliminate the first and last item


    for job in jobs:
      title = job.find("span", class_="title").text
      #region = job.find("span", class_="region")
      #region = "No Region" if not region else region.text

      # _ is a valid variable name but we use it to ignore the particular item
      # this syntax put each item in the list to a variable
      # * allows an unspecified number of arguments and it consumes them all.. so it returns a tuple
      company, position, *region = job.find_all("span", class_="company")

      """
      if region :
        region = region.text
      else:
        region = "N/A"   # contract jobs don't have region
        """
      #url = job.find("a")["href"] # this is how to extract attribute
      url = job.find("div", class_="tooltip--flag-logo").next_sibling["href"] 
      url = f"https://weworkremotely.com{url}"
      #position is full-time/contract info
      region = region[0].text if region else None #"No Region" if not region else region[0].text
      jobs_db.append(Job(title = title, 
                         company = company.text.strip(), 
                         url = url, 
                         region = region, 
                         position = position.text.strip()))
      
  def scrape_page(url):
    if not testing:
      r = requests.get(url,
                            headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"})
    
      if r.status_code == 200:
        parse_html(r.content)
      else:
        print(f"request error with {r.content}")
    else:
      f = open(url, encoding="utf8")
      parse_html(f)
      f.close()
    
  def get_pages(url):
    response = requests.get(url,
                            headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"})
    if(response.status_code == 200):
      soup = BeautifulSoup(response.content, "html.parser")
      return len(soup.find("span", class_= "pages-container").find_all("span", class_= "page"))
    else:
       raise print(f"Cannot access the site ({response.status_code})")

  if not testing :
    pages = get_pages("https://weworkremotely.com/remote-full-time-jobs")
    for page in range(pages):
      url = f"https://weworkremotely.com/remote-full-time-jobs?page={page+1}"
      scrape_page(url)
      save_to_file("weworkremotely", jobs_db) 
  else:
      scrape_page("html/weworkremotely.html")
      save_to_file("weworkremotely", jobs_db) 

#scrape_weworkremotely() ## request issues

#scrape_wanted_jobs()
#scrape_remoteok_jobs("python")
#scrape_weworkremotely(True)

