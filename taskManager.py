#!/usr/local/bin/python3
# coding=utf-8

import os
import json
import datetime


def printWarningText(text):
    print("\033[93;40mm" + text + "\033[0m")


def printDict(dic):
    print("\n～～～～TASK LIST～～～～\n")
    for key, val in dic.items():
        print("No." + str(key) + " : " + val)
    print("\n～～～～TASK LIST～～～～\n")


def getTaskName():
    while True:
        taskDict = getTaskDict("tasks/")
        printDict(taskDict)
        taskKey = input("請輸入Task 編號: ")
        if taskKey not in taskDict:
            printWarningText("找不到編號 " + taskKey + " 的Task")
            continue
        else:
            return taskDict[taskKey]


def getTaskDict(path):
    taskDict = {}
    tasksPath = path
    folders = os.listdir(tasksPath)
    idx = 1
    for folder in folders:
        s = str(idx)
        taskDict[s] = folder
        idx += 1
    return taskDict


def getMainConfig(taskName):
    configPath = "tasks/" + taskName + "/config.json"
    with open(configPath) as f:
        return json.load(f)


def getToDoScripts(taskName):
    scriptPath = "tasks/" + taskName + "/scripts/"
    todoScripts = []
    files = os.listdir(scriptPath)
    files.sort(key=lambda x: int(x[0:2]))
    for file in files:
        with open(os.path.join(scriptPath, file)) as f:
            data = json.load(f)
            todoScripts.append(data)

    return todoScripts


def runNextAction():
    while True:
        isNext = input("還要進行後續流程嗎？(y/n)\n")
        if isNext == "n":
            return
        elif isNext != "y" and isNext != "n":
            print("請輸入(y/n)")
            continue

        taskDict = getTaskDict("nextAction/")
        printDict(taskDict)
        taskKey = input("請輸入Task 編號: ")
        if taskKey not in taskDict:
            printWarningText("找不到編號 " + taskKey + " 的Task")
            continue
        taskName = taskDict[taskKey]
        print("正在執行 " + taskName)
        os.chdir("nextAction")
        os.system("chmod u+x *.sh")
        os.system("./" + taskName)
        os.chdir("../")


def printCoverage(taskName, config, scripts):
    if not os.path.isdir("coverage"):
        os.mkdir("coverage")
    if not os.path.isdir("coverage/"+taskName):
        print("自動創建coverage/"+taskName+"資料夾")
        os.mkdir("coverage/"+taskName)
    coverageName = config["title"]
    if coverageName == "":
        coverageName = input("請輸入報告名稱: ")
    today = datetime.date.today()
    now = datetime.datetime.now()
    time = str(today.year) + str(today.month) + str(today.day) + \
        "_" + str(now.hour) + str(now.minute) + str(now.second)
    coverageName = coverageName + "_" + time
    path = "coverage/"+taskName+"/"+coverageName
    print("報告資料夾名稱: " + coverageName)
    os.mkdir(path)
    for script in scripts:
        coverage = {
            "dictionary": script["dictionary"],
            "oldFileContent": script["oldFileContent"],
            "newFileContent": script["newFileContent"],
            "oldFolderPaths": script["oldFolderPaths"],
            "newFolderPaths": script["newFolderPaths"]
        }
        with open(path+"/"+script["title"]+".json", "w") as file:
            json.dump(coverage, file, indent=4)
    os.system("open " + path)
