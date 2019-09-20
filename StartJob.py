import argparse
from Modules import Logger
from JobHandler import JobHandler
import Utility as util


def user_auth(user,pwd,job):
    enter = job.authStreamsets(user,pwd)
    if enter == True:
        print("Login Failed.  Please enter the correct username and password")
        util.script_exit(False)
    else:
        print("Welcome!")

def readArgs():
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--conf", required=True)
    ap.add_argument("-n", "--name", required=True)
    args = vars(ap.parse_args())
    pName = args["name"]
    conf = args["conf"]
    config = util.load_config(conf)
    return pName, config


if __name__ == '__main__':

    util.writeToFile("result.csv","")
    
    pName, config = readArgs()
    confTbl = "config_"+config["ENV"]
    jobTbl = "job_"+config["ENV"]

    try:
        job = JobHandler(config)

        # log into streamsets
        user_auth(config["USER"],config["PWD"],job)

        # initialize log structure
        logger = Logger()
        logger.setLogDir()
        job.setLogger(logger)

        # invalidate hive table
        job.validateTbls(confTbl, jobTbl)

        # find & create job
        jobId = job.findJobId(confTbl, jobTbl, pName)
        print("job id: "+jobId)
        if jobId == 0:
            print("WARNING: Job can't be found.")
        else:
            job.startJob(jobId)
        

    except Exception as e:
        print(str(e))
        print("Exception happened.  Exit.")   
        util.script_exit(False)     

    util.script_exit(True)
