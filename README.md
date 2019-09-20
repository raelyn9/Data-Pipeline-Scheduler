# Streamsets Pipeline Scheduler

- Before running the script, make sure that the schedule csv can be read properly by python.  When converting .xlsx to .csv, it happens that the python csv reader module cannot read the first column of the csv file.  In that case, create a new csv file and then copy and paste the content to the new csv.  Read from the new csv file instead.  

### Run:
```
python Scheduler.py --user [cron user] --file [schedule file] 
python RmCron.py --user [cron user]
```

### Overview:
Schedule pipeline jobs by reading from a csv to get job information and generating crontab entries.  Config.json contains database connection parameters, user account info and pipeline environment.

### Steps:
- Parse csv file and read configurations from config.json
- Get pipeline job id from pipeline name by querying hive tables (config_env and job_env).  Environment is specified in the config file
- Add job to cron
- Add job for RmCron.py at the end to remove jobs that are only run one time (if there is an 'End' entry at the end of the csv )OR run RmCron.py manually

### Note:
- All pipelines included in the schedule must also have entries in the config_env file to complete the job id search.  Otherwise the job will not be found or run.
- All pipelines should have distinct names if we search job by pipeline name. 
- Specify configurations (user, pswd, db, env, etc) in config.json.
- File must be in csv and follow the table structure.
- Schedule csv format: Pipeline Name, (Pipeline ID) , Start Time ETC, Start Time UTC, Frequency


# Scheduler-Separate 
- scheduler-separate folder separates the scheduling process. Gencron folder has the code that transforms the schedule csv to croninfo.csv that contains all the information needed for generating cron entries. The script in cronjob folder will add cron entries to the cron file using croninfo.csv (LoadToCron.py).  It also contains the script for running the actual cron task (StartJob.py).  

### Deployment Steps:
- Step 1: Place gencron folder in the environment with Arcadia shell installed, and place cronjob in the data collector environment.  
- Step 2: When deploying a schedule, run the script in gencron first with the input scheduler file
```
python ScheduleProcessor.py --file [schedule csv file] --config [config file]
# e.g.  python ScheduleProcessor.py --file test-schedule.csv --config config.json
```
- Step 3: The script will output a file called croninfo.csv.  Copy croninfo.csv to the data collector environment within the cronjob folder
- Step 4: Run the cronjob script to create cron entries
```
python LoadToCron.py --user [user] --file [croninfo file]  --dir [directory of StartJob.py]
# e.g. python LoadToCron.py --user fvdl_project_rbu --file croninfo.csv --dir /home/fvdl_project_rbu/crontask/
# user - LoadToCron.py will write cron entries to the input user's cron file
```