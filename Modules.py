import Utility as util


class Logger():

    def __init__(self):
        pass
    
    def setLogDir(self):
        currentday,currenttime = util.getTime()

        print("!!!! logger  time "+currenttime)

        self.directory = "logs/"+currentday
        self.logfile = self.directory+"/streamsets_"+currenttime+".log"
        self.selectconf = self.directory+"/select_config_"+currenttime+".sql"
        self.selectjob = self.directory+"/select_job_"+currenttime+".sql"

        util.createFolderStructure(self.directory)
    
    def writeToLog(self, content):
        print(content) # print to console
        util.writeToFile(self.logfile,content+'\n')
    
    def writeToSelectConf(self, content):
        util.writeToFile(self.selectconf,content)

    def writeToSelectJob(self, content):
        util.writeToFile(self.selectjob,content)
    
    def writeAPILog(self, url):
        content = '--> Streamsets API url: '+url
        self.writeToLog(content)

    def getLogFile(self):
        return self.logfile