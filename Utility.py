import datetime
import zipfile
import shutil
import os
import json
import argparse
import sys
import time
import csv


#load config
def load_config(config):
	conf = json.load(open(config))
	return conf

# ---------- File & OS -----------------
# make a dir if not exists & clear content if exists
def makeDir(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder,777)

# delete folder and its content
def rmDir(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)

# get all file names in the folder
def getFileList(folder):
    filenames = []
    for filename in os.listdir(folder):
        filenames.append(filename)
    return filenames

# write to file, append if file exists
def writeToFile(filename, content):
	if not os.path.exists(filename):
		with open(filename, 'w+') as f:
			f.write(content)
	else:
		with open(filename, 'a') as f:
			f.write(content)

def createFolderStructure(dir):
	if not os.path.exists(dir):
		os.makedirs(dir)

def readFile(filename):
	content = ""
	with open(filename, 'r') as f:
		content = f.read()
	return content

# ------------ Json -----------------------
# open json file
def openFile(name,folder):
    path = os.path.join(folder+"/",name)
    f = open(path, "rb")
    data = json.loads(f.read())
    return data

# write string data into json file and store as name.json
# requires: data is string type
def writeToJson(data,name):
    data = json.loads(data)
    with open( name + '.json', 'w') as outfile:
        json.dump(data, outfile)

# store input data as name.json in folder
# requires: data is json
def createJsonFile(data,name,folder):
    path = os.path.join(folder+"/",name)
    with open( path, 'w') as outfile:
        json.dump(data, outfile)

# convert to string
def convertToStr(data):
	return json.dumps(data)

# convert to json
def convertToJson(data):
	return json.loads(data)

# return current timestamp
def getTimeStamp():
    time = '{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
    return time

def getTimeFormatted():
	time = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
	return time

def getTime():
	timestamp = datetime.datetime.now()
	currentday = timestamp.strftime('%Y%m%d')
	currenttime = timestamp.strftime('%Y%m%d%H%M%S')
	return currentday,currenttime

def execCmd(command):
	os.system(command)

def deleteFile(name):
	if os.path.exists(name):
		os.remove(name)

def clean_up():
	deleteFile("token.txt")   # auth token
	deleteFile("result.csv")  # query result

def script_exit(success):
	clean_up()
	if success:
		exit(0)
	exit(-1)
