from datetime import datetime
import argparse
import csv
from Modules import Logger
from JobHandler import JobHandler
from HiveDataStore import CronRecord
import Utility as util


# take in schedule file, get job id from pipeline name/id
# output croninfo.csv containing jobid, time, frequency

def read_input():
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--file", required=True) # schedule file
    ap.add_argument("-c", "--conf", required=True) # config file for scheduler
    ap.add_argument('-n', action='store_true')  # search by pipeline name  optional
    ap.add_argument('-i', action='store_true')  # search by pipeline id    optional
    
    # read args
    flags = ap.parse_args()
    args = vars(ap.parse_args())
    filename = args["file"]
    conf = args["conf"]
    config = util.load_config(conf)

    search_col = "Pipeline Name"  # default
    if flags.i:
        search_col = "Pipeline ID"
    
    return filename, search_col, config


if __name__ == '__main__':
 
    filename, search_col, config = read_input()

    job = JobHandler(config)
    confTbl = "config_"+config["ENV"]
    jobTbl = "job_"+config["ENV"]

    # initialize log structure
    logger = Logger()
    logger.setLogDir()
    job.setLogger(logger)

    # invalidate hive table
    job.validateTbls(confTbl, jobTbl)

    # get cron job info
    data = csv.DictReader(open(filename))
    records = []

    for row in data:
        pName = row[search_col]
        freq = row['Frequency'] 
        time = row['Start Time UTC']
        
        print(pName, time)

        # find & create job
        jobId = job.findJobId(confTbl, jobTbl, pName)
        print("job id: ",jobId)
        if jobId == 0:
            print("WARNING: Job can't be found.")
        else:
            record = CronRecord(jobId, time, freq)
            records.append(record)
        

    filename = "croninfo" 
    job.writeToFile(filename, records)


    util.script_exit(True)

