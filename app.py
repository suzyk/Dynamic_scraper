from flask import Flask, render_template, request, redirect, send_file
import requests
from bs4 import BeautifulSoup
from scraper.wework_jobs import get_wwr_jobs
from scraper.berlin_jobs import get_berlin_jobs
from scraper.web3_jobs import get_web3_jobs
from util.file import save_to_file

app = Flask(__name__)
db = {} # fake database
"""
Do this when scraping a website to avoid getting blocked.

headers = {
      'User-Agent':
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
      'Accept':
      'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
      'Accept-Language': 'en-US,en;q=0.5',
}

response = requests.get(URL, headers=headers)
"""

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/search")
def search():
  keyword = request.args.get("keyword")
  print(f"search is called with key = {keyword}")
  if keyword == None:
    return redirect("/") #redirect to home
  if keyword in db:
    jobs = db[keyword]
    print("!@#$%^&*(**** printing from db")
  # scrape jobs with this keyword and send the result as an arg below
  else:
    #berlin_jobs = get_berlin_jobs(keyword)
    #wwr_jobs = get_wwr_jobs(keyword) #3
    #web3_jobs = get_web3_jobs(keyword) #8
    #jobs = berlin_jobs + wwr_jobs + web3_jobs #25
    print("********* printing from request")
    jobs = get_web3_jobs(keyword)
    db[keyword] = jobs
    count = len(jobs)
  return render_template("search.html", keyword=keyword, jobs=jobs, count = count)


@app.route("/export")
def export():
  keyword = request.args.get("keyword")
  if keyword == None:
    return redirect("/")
  if keyword not in db:
    return redirect(f"/search?keyword={keyword}")
  save_to_file(keyword, db[keyword])
  return send_file(f"{keyword}_jobs.csv", as_attachment=True) # trigger download


if __name__ == "__main__":
    app.run()
