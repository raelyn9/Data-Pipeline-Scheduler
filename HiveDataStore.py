import Utility as util
from Modules import Logger
import csv


class Record():
    def __init__(self, pipelineID, time, user, version):
        self.pipelineID = pipelineID
        self.time = time
        self.user = user
        self.version = version

class ConfigRecord(Record):
    def __init__(self, pipelineID, name, label, param, value, time, user, version):
        Record.__init__(self, pipelineID, time, user, version)
        self.name = name
        self.label = label
        self.param = param
        self.value = value

class JobRecord(Record):
    def __init__(self, pipelineID, jobID, time, user, version, action):
        Record.__init__(self, pipelineID, time, user, version)
        self.jobID = jobID
        self.action = action


class HiveDataStore():

    def __init__(self):
        pass

    def setLogger(self, logger):
        self.logger = logger
    
    def setDb(self, db):
        self.db = db


    # query table
    def queryConfByName(self, table, name):
        hive_query = "SELECT * FROM ( SELECT pipelineid, param, value, row_number() OVER ( PARTITION BY param ORDER BY time DESC ) AS row_num FROM "+self.db+"."+table+" WHERE name = '"+name+"') temp_tbl WHERE row_num = 1 LIMIT 1;"
        return hive_query

    def queryJob(self, table, pipelineID):
        hive_query = "SELECT * FROM "+self.db+"."+table+" WHERE PipelineID = '"+pipelineID+"' AND action = 'created' ORDER BY time DESC LIMIT 1;"
        return hive_query
   

    # parse 
    def parseConfigQueryResult(self, table):
        records = []
        result_file = "result.csv"
        table = "temp_tbl"
        result = csv.DictReader(open(result_file))
        for row in result:
            record = ConfigRecord(row['pipelineid'],"","",row['param'], row['value'],"","","")
            records.append(record)
        return records

    def parseJobQueryResult(self, table):
        record = JobRecord("","","","","","") # empty
        result_file = "result.csv"
        result = csv.DictReader(open(result_file))
        for row in result:
            record = JobRecord(row['pipelineid'], row['jobid'], row['time'], row['createdby'], row['version'], row['action'])
        return record


    def writeToLog(self, content):
        self.logger.writeToLog(content)