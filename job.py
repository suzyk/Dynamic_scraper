class Job:
  def __init__(self, title, company, url, region = "No Region Info", salary = "No Salary Info", position = "No Position Info"):
    self.title = title 
    self.company = company
    self.url = url
    self.region = region
    self.salary = salary
    self.position = position

  def get_parameters():
     return ["Title","Company","Url","Position","Region","Salary"]
  
  def get_values(self):
     return [self.title, self.company, self.url, self.position, self.region, self.salary]
  
  def __str__(self):
    return f"Title: {self.title}\nCompany: {self.company}\nPosition: {self.position}\nRegion: {self.region}\nSalary: {self.salary}\nURL: {self.url}\n"
