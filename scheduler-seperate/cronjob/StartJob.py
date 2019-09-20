import argparse
import Utility as util
import SchAPI as sch

# Actual cron task
# Run the job with the given job id using the account specified in the config file

def user_auth(config):
    enter = sch.authStreamsets(config,config["USER"],config["PWD"])
    if enter == True:
        print("Login Failed.  Please enter the correct username and password")
        util.script_exit(False)
    else:
        print("Welcome!")

def readArgs():
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--conf", required=True)
    ap.add_argument("-j", "--job", required=True)
    args = vars(ap.parse_args())
    jobId = args["job"]
    conf = args["conf"]
    config = util.load_config(conf)
    return jobId, config


if __name__ == '__main__':

    jobId, config = readArgs()
    try:
        # log into streamsets
        user_auth(config)
        # start job
        sch.startJob(config, jobId)
        

    except Exception as e:
        print(str(e))
        print("Exception happened.  Exit.")   
        util.script_exit(False)     

    util.script_exit(True)
