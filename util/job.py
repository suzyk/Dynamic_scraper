class Job:
  def __init__(self, title, company, url, region = None, salary = None, position = None):
    self.title = title 
    self.company = company
    self.url = url
    self.region = region if not None else "No Region Info"
    self.salary = salary if not None else "No Salary Info"
    self.position = position if not None else "No Position Info"

  def get_parameters():
     return ["Title","Company","Url","Position","Region","Salary"]

  def get_values(self):
     return [self.title, self.company, self.url, self.position, self.region, self.salary]

  def __str__(self):
    return f"Title: {self.title}\nCompany: {self.company}\nPosition: {self.position}\nRegion: {self.region}\nSalary: {self.salary}\nURL: {self.url}\n"
    