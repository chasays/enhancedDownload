# coding: utf-8

import requests
from  time import sleep

serverIP = 'http://127.0.0.1:26339/api/'
buildurl = serverIP + 'buildTask'
gettask = serverIP + 'getTask?id='
starttask = serverIP + 'startTask'
headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': ''}


def fastDownload(url, thread=56, output=r'D:\\Music1', timeout=100):
    taskid = ''
    try:
        buildtask = requests.post(buildurl,
                                  json={'url': url},
                                  headers=headers)
        taskid = buildtask.json().get('data')
        getReq = requests.get(gettask + taskid, headers=headers)
        startJson = getReq.json().get('data').get('task')
        if startJson:
            startJson['filePath'] = output
            startJson['unzip'] = False
            startJson['connections'] = thread

        start = requests.post(starttask, headers=headers, json=startJson)
    except Exception as e:
        print e.message
    else:
        print "Downloading"
        hasCompleted(taskid, timeout)
        return taskid


def hasCompleted(taskID, timeout=100):
    for index in range(timeout):
        getJson = {}
        try:
            getReq = requests.get(gettask + taskID, headers=headers)
            getJson = getReq.json().get('data').get('task')
        except Exception as e:
            print e.message
        else:
            print "Finished: {:.1f} MB".format(getJson.get('downSize') / 1024 / 1024.0)
            sleep(1)
            if getJson.get('totalSize') == getJson.get('downSize'):
                break
if __name__=='__main__':
    fastDownload('http://res.smzdm.com/android/SMZDM_V9.2.1/smzdm-9.2.1-smzdm_i.apk')
