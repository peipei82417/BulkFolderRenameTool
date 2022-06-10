#!/usr/local/bin/python3
# coding=utf-8

import os
import json


def printWarningText(s):
    print("\033[93m" + s + "\033[0m")


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
