from crontab import CronTab
import argparse

def read_input():
    ap = argparse.ArgumentParser()
    ap.add_argument("-u", "--user", required=True)
    args = vars(ap.parse_args())
    user = args["user"]
    return user

if __name__ == '__main__':

    user = read_input()

    my_cron = CronTab(user=user)

    for job in my_cron:
        if job.comment == 'one time':
            my_cron.remove(job)
            my_cron.write()