from flask import Flask, render_template, request, redirect, send_file
from file import *
from scraper.remoteok import scrape_remoteok_jobs

app = Flask("Jobscrapper")

db = {} # fake database
 
# create response for homepage
@app.route("/")  # this is called a decorator
def home():
  return render_template("home.html")

@app.route("/search")
def search():
  keyword = request.args.get("keyword")
  if keyword == None:
    return redirect("/") #redirect to home
  if keyword in db:
    jobs = db[keyword]
  # scrape jobs with this keyword and send the result as an arg below
  else:
    #jobs = wwr+ remote
    jobs = scrape_remoteok_jobs(keyword, True)
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
  app.run(debug=False)
