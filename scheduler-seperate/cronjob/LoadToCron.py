from crontab import CronTab
from datetime import datetime
import argparse
import csv

# create cron jobs from input csv file that contains information about the job (jobid, time, frequency)
# take in user to create cron file on that user
# task directory for referencing the task script location

def readArgs():
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-u", "--user", required=True) # cron user
    ap.add_argument("-f", "--file", required=True) # cron info file
    ap.add_argument("-d", "--dir", required=True) # cron task directory:  /home/fvdl_project_rbu/crontask/
    args = vars(ap.parse_args())
    user = args["user"]
    filename = args["file"]
    directory = args["dir"]
    return user, filename, directory


if __name__ == '__main__':

    user, filename, directory = readArgs()
    user_cron = CronTab(user=user)

    
    data = csv.DictReader(open(filename))
    for row in data:
        jobId = row["JobID"]
        freq = row['Frequency'] 
        time = row['Time']
        datetime = datetime.strptime(time, "%Y-%m-%d %H:%M")

        job = user_cron.new(command='python '+directory+'StartJob.py --job '+jobId+' --conf '+directory+'config.json', comment=freq)

        if freq == "one time":
            job.month.on(datetime.month)
            job.day.on(datetime.day)
            job.hour.on(datetime.hour)
            job.minute.on(datetime.minute)
        
        elif freq == "daily":
            job.hour.on(datetime.hour)
            job.minute.on(datetime.minute)

        elif freq == "hourly":
            job.minute.on(datetime.minute)

        user_cron.write()
