import SchAPI as sch
import Utility as util
from ShellProcess import ShellProcess
import APIBuilder as API

class JobHandler():
	def __init__(self,config):
		self.shellProcess = ShellProcess()
		self.config = config
		self.shellProcess.setDb(config)
		

	def setLogger(self, logger):
		self.shellProcess.setLogger(logger)
		self.shellProcess.execKinit()


	def authStreamsets(self, user, pswd):
		return not(API.setAuthToken(user, pswd, self.config))

	
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


	def startJob(self, jobId):
		sch.startJob(self.config, jobId)