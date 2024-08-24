from extractor import *
from flask import Flask, render_template, request

app = Flask("Jobscrapper")

db = {} # fake database
 
# create response for homepage
@app.route("/")  # this is called a decorator
def home():
  return render_template("home.html")

@app.route("/search")
def search():
  keyword = request.args.get("keyword")
  if keyword in db:
    jobs = db[keyword]
  # scrape jobs with this keyword and send the result as an arg below
  else:
    scrape_remoteok_jobs(keyword, True)
    db[keyword] = jobs_db
    jobs = jobs_db
  return render_template("search.html", keyword=keyword, jobs=jobs)

if __name__ == "__main__":
  app.run(debug=True)
