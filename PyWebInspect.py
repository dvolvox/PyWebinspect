# Python Dependencies
from requests.auth import HTTPBasicAuth
import requests
import json
import pymssql
import xml.etree.ElementTree as ET
import urllib
import random, string
import time
import datetime
from collections import Counter


#Disable Warning for the url3 packages
requests.packages.urllib3.disable_warnings()


class ApiWInspect(object):

  #
  # Init Functioon
  #
  def __init__(self):
    self.errorLog = []
    # Load Settings from config.json file
    self.settings = self.loadConfig()
    #Load the Debug flag
    self.DEBUG = self.settings["debug"]
    # This flag is used to stop the flow at 1rst exception
    self.breakOnException = self.settings["breakOnException"]
    #Ping WebInspect Instance
    self.initPing()


  ################################################################
  #
  # Helpers
  #
  ################################################################

  #
  # Init ping
  #
  def initPing(self):
    if self.settings["initPing"]:
      try:
        self.logMessage("Connecting to Webinspect...")
        tmp = requests.get("http://" + self.settings["con"]["host"] + ":" + self.settings["con"]["port"] +"/webinspect",verify=False)
        if tmp.status_code <  200 or tmp.status_code >= 400:
          self.launchException(0,"Unable to reach WebInspect")
      except Exception as e:
        self.launchException(0,"Unable to reach WebInspect")

  #
  # Load Configuration File
  #
  def loadConfig(self):
    with open('etc/config.json',"r") as outfile:
      tmpSettings = json.load(outfile)
    if tmpSettings["con"]["host"] == "":
      raise Exception("Host cannot be empty on the configuration file (./etc/config.json)")
    if tmpSettings["con"]["port"] == "":
      tmpSettings["con"]["port"] = "8083"
    return tmpSettings

  #
  # Make HTTP Request
  #
  def makeRequest(self, uri, body):
    try:
      tmpUrl = "http://" + self.settings["con"]["host"] + ":" + self.settings["con"]["port"] + uri

      self.logMessage("makeRequest",tmpUrl,body)

      if body != {}:
        tmpUrl += "?" + urllib.urlencode(body)
        tmp = requests.get(tmpUrl, verify=False)
      else:
        tmp = requests.get(tmpUrl, verify=False)
      if tmp.status_code <  200 or tmp.status_code >= 400:
        self.errorLog.append("HTTP Error %s" % tmp.status_code)
        return []
      else:
        return json.loads(tmp.text)
    except Exception as e:
      return self.launchException(1, "makeRequest",e.message,uri,body)

  #
  # Exception Handler
  #
  def launchException(self,chain=False,*args ):
    message = "[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "]"
    message += "[ERROR]"
    for var in args:
      message += '[{:^10}]'.format(var)

    if self.breakOnException or not chain:
      # Launch Exception
      raise Exception(message)
    else:
      # Save to error log
      self.errorLog.append(message)
      return []
  
  #
  # Logging message
  #
  def logMessage(self, *args):
    if self.DEBUG:
      lmsg = "[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "]"
      lmsg += "[DEBUG]"
      for var in args:
        lmsg += '[{:^10}]'.format(var)
      print lmsg


  ################################################################
  #
  # API
  #
  ################################################################

  #
  # ExecuteRest
  # Main route
  #
  def executeCall(self, inputOperation, inputId=None, args={}):
    self.logMessage("executeCall",inputOperation,inputId,args)
    try:   
      # Get All Scans
      if inputOperation == "getScans":
        uri = "/webinspect/scanner/scans/"
      
      # Get Settings
      elif inputOperation == "getSettings":
        uri = "/webinspect/scanner/settings/"
      
      # Get Status of a Scan from ID
      elif inputOperation == "getScan" and inputId != None:
        uri = "/webinspect/scanner/%s" % inputId
      
      # Export to file by scan ID
      elif inputOperation == "getScanDesc" and inputId != None:
        uri = "/webinspect/scanner/%s.scan" % inputId
      
      #Get scan details by ID
      elif inputOperation == "getScanDetails" and inputId != None:
        uri = "/webinspect/scanner/%s.details" % inputId 
      
      #Get issues requests response from scan id
      elif inputOperation == "getScanIssue" and inputId != None:
        uri = "/webinspect/scanner/%s.issue" % inputId             
      else:
        raise Exception("Invalid Key")

      response = self.makeRequest(uri,args)
      return {"response": response,"errorLog": self.errorLog, "len": len(response)}

    except Exception as e:
      self.launchException(0,e.message, inputOperation, inputId, args)
    
    


#
# TESTS
#
#tmp = ApiWInspect()
#print json.dumps(tmp.executeCall("getScans"),indent=2)
#pj = tmp.executeCall("getScans", None, {"Status":"Complete", "Name":"EDS"})
#scanId = pj["response"][0]["ID"]

#scan = tmp.executeCall("getScan",scanId)
#print scan

#scan = tmp.executeCall("getScanIssue",scanId)
#print scan