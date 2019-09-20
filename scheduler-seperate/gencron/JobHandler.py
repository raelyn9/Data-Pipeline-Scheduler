import Utility as util
from ShellProcess import ShellProcess

class JobHandler():
	def __init__(self,config):
		self.shellProcess = ShellProcess()
		self.config = config
		self.shellProcess.setDb(config)

	def setLogger(self, logger):
		self.shellProcess.setLogger(logger)
		self.shellProcess.execKinit()

	
	def validateTbls(self, confTbl, jobTbl):
		self.shellProcess.invalidateTbl(confTbl)
		self.shellProcess.invalidateTbl(jobTbl)


	def findJobId(self, table, jobtbl, name):
		records = self.shellProcess.queryConfImpala(table, name)
		if len(records) == 0:
			return 0
		pId = records[0].pipelineID
		record = self.shellProcess.queryJobImpala(jobtbl,pId)
		return record.jobID


	def writeToFile(self, filename, records):
		self.shellProcess.writeCronToCsv(filename, records) 