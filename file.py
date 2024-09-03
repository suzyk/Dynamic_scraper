import csv
from job import Job 
from io import StringIO
#BytesIO, TextIOWrapper

def save_to_file(file_name, jobs):
    
    file = open(f"{file_name}_jobs.csv", "w")
    writer = csv.writer(file)
    writer.writerow(Job.get_parameters())
    for job in jobs:
        writer.writerow(job.get_values())
    file.close()
