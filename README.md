PyWebInspect
========================

* Version  : 1.0-(Beta) 
* Language : Python (compiled for 2.7)
* Type     : Module


Description
-----------

A python-based interface with a remote instance of WebInspect. Connecting to the REST API of HP WebInspect you can gather multiple metrics and trigger actions remotely and automated:
* Get all scans;
* Get scan information (status, issues, details,...);
* (...)

You can see the full list of features on the official documentation for the HP Web Inspect REST API.

Warning: Some of the available features in the documentation might not be avaiable in this version.


---------------


Pre-requirements
---------------

* Python 2.7 installed;
* Connectivity to the WebInspect instance;
* Have REST API Enable on WebInspect (HP Fortify Monitor);
* and you are ready to go.


Setup 
---------------

1º - pip install -r requirements.txt;
2º - Setup configuration file (etc/config.json) you can copy the config_template.json and change it;
2º - Import module into your project.

You can change the flags in the configuration file:
* DEBUG: enable/disable stdout messages
* breakOnException: During the flow of the application exceptions might happen and you can choose either if you want them to break the flow at first exception or not (the exception message will be added to the Array errorLog).

And you can start using the features available.

e.g:
```
tmp = ApiWInspect()
#Get scans for a give project: pjName
pj = tmp.executeCall("getScans", None, {"Status":"Complete", "Name":"pjName"})

scanId = pj["response"][0]["ID"]

# Get status of the scan
scanStatus = tmp.executeCall("getScan",scanId)
print scanStatus

# Get Issues of the scans
scanIssues = tmp.executeCall("getScanIssue",scanId)
print scanIssues

```


---------------


TO-DO List
---------------

* Support Authentication (BasicAuth) 
* Get last scans (per project*)
* Logging
* Support Reporting and CRONJOBS
* Launch Scans


If you have any suggestions of improvements or features feel free to comment or contact: duarteetraud@gmail.com.