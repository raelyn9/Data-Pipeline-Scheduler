from crontab import CronTab
from datetime import datetime
import argparse
import csv


# set up env and db in config.json

def read_input():
    ap = argparse.ArgumentParser()
    ap.add_argument("-u", "--user", required=True)
    ap.add_argument("-f", "--file", required=True)
    
    args = vars(ap.parse_args())
    user = args["user"]
    filename = args["file"]
    return user, filename


if __name__ == '__main__':
 
    user, filename = read_input()
    my_cron = CronTab(user=user)

    data = csv.DictReader(open(filename))
    for row in data:
        pName = row["Pipeline Name"]
        freq = row['Frequency'] 
        start = row['Start Time UTC']
        print(pName, start)

        if pName == "End":
            # clean up
            job = my_cron.new(command='python /home/ph_cron-fvdlservice/scheduler/RmCron.py --user '+ user, comment="one time")
        else:
            job = my_cron.new(command='python /home/ph_cron-fvdlservice/scheduler/StartJob.py --name '+pName+' --conf /home/ph_cron-fvdlservice/scheduler/config.json', comment=freq)

        datetime = datetime.strptime(start, "%Y-%m-%d %H:%M")
        if freq == "one time":
            job.month.on(datetime.month)
            job.day.on(datetime.day)
            job.hour.on(datetime.hour)
            job.minute.on(datetime.minute)

        if freq == "daily":
            job.hour.on(datetime.hour)
            job.minute.on(datetime.minute)

        elif freq == "hourly":
            job.minute.on(datetime.minute)

        my_cron.write()
