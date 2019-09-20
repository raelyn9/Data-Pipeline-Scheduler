import Utility as util
import APIBuilder as API


def authStreamsets(config, user, pswd):
	return not(API.setAuthToken(user, pswd, config))

def getJobStatus(config, jobId):
    body = [jobId]
    return API.sch_api_post_request(config, '/jobrunner/rest/v1/jobs/status','',body)    

def startJob(config, jobId):
    body = [jobId]
    return API.sch_api_post_request(config, '/jobrunner/rest/v1/jobs/startJobs','',body)

def stopJob(config, jobId):
    body = [jobId]
    return API.sch_api_post_request(config, '/jobrunner/rest/v1/jobs/stopJobs','',body)