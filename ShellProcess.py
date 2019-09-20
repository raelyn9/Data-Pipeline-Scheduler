import Utility as util
from HiveDataStore import HiveDataStore
from Modules import Logger


class ShellProcess():

    def __init__(self):
        self.db = HiveDataStore()

    def setDb(self, conf):
        self.conf = conf
        self.impala_cmd = self.conf['IMPALA_SHELL_CMD']+" -f "
        self.impala_select_cmd = self.conf['IMPALA_SHELL_CMD']+" -B -q "
        self.impala_invalidate_cmd =  self.conf['IMPALA_SHELL_CMD']+" -q \" invalidate metadata "+self.conf["DB"]+"."
        self.db.setDb(self.conf["DB"])
        
    def setLogger(self, logger):
        self.logger = logger
        self.db.setLogger(logger)

    def execCmd(self, cmd):
        util.execCmd(cmd)
        self.logger.writeToLog(cmd)

    def execKinit(self):
        self.execCmd("echo \""+self.conf["KPWD"]+"\" | kinit "+self.conf["KUSER"])

    def execImpalaCmd(self, filename):
        cmd = self.impala_cmd+filename
        self.execCmd(cmd)

    def invalidateTbl(self, table):
        query= self.impala_invalidate_cmd + table +";\""
        self.execCmd(query)
    
    def queryConfImpala(self, table, name):
        query = self.impala_select_cmd + "\""+ self.db.queryConfByName(table,name) + " \" -o result.csv  --print_header \"--output_delimiter=,\";"
        self.execCmd(query)
        records = self.db.parseConfigQueryResult(table)
        return records
    
    def queryJobImpala(self, table, pipelineId):
        query = self.impala_select_cmd +"\""+ self.db.queryJob(table,pipelineId) + " \" -o result.csv  --print_header \"--output_delimiter=,\";"
        self.execCmd(query)
        record = self.db.parseJobQueryResult(table)
        return record

    


