#!/usr/local/bin/python3
# coding=utf-8

import json
import string
import random
import numpy as np
import checkConfig


def main(config, scripts):
    for script in scripts:
        print("正在執行 " + script["title"] + " 腳本初始化")

        actions = script["actions"]
        setNewFolderGraph(actions)
        createDictionary(script)
        setSubstringSets(script)
        print(script)
        print(script["title"] + " 腳本初始化完成")

    isPass = checkConfig.checkScriptPath(config, scripts)
    if not isPass:
        exit()


def setNewFolderGraph(actions):
    maxSize = getMaxSizeAction(actions)
    randomSets = createRandomSets(maxSize)

    for action in actions:
        if "newFolderGraph" in action:
            continue

        newGraph = cloneGraph(
            action["renameFolderGraph"],
            randomSets
        )
        if "isPassGraphRoot" in action and action["isPassGraphRoot"]:
            key = list(action["renameFolderGraph"].keys())[0]
            newGraph.update({key: newGraph.pop(randomSets[0])})
            tups = list(newGraph.items())
            tups.insert(0, tups.pop())
            newGraph = dict(tups)
        action["newFolderGraph"] = newGraph


def getMaxSizeAction(actions):
    maxSize = 0
    i = 0
    while i < len(actions):
        maxSize = max(maxSize, len(actions[i]["renameFolderGraph"]))
        i += 1

    return maxSize


def cloneGraph(graph, newNameSets):
    clone = graph
    c = json.dumps(clone)
    nodeSets = []
    for key in graph:
        nodeSets.append(key)

    i = 0
    while i < len(nodeSets):
        c = c.replace(
            nodeSets[i],
            newNameSets[i]
        )
        i += 1
    return json.loads(c)


def setSubstringSets(script):
    actions = script["actions"]

    oldFolderNameSets = []
    newFolderNameSets = []

    for action in actions:
        oldGraph = action["renameFolderGraph"]
        newGraph = action["newFolderGraph"]

        pathList1 = findAllPathsInGraph(oldGraph, list(oldGraph)[0])
        pathList2 = findAllPathsInGraph(newGraph, list(newGraph)[0])

        destructuringAssignment(oldFolderNameSets, pathList1)
        destructuringAssignment(newFolderNameSets, pathList2)

    setFolderPaths(script, oldFolderNameSets)

    setLinkMode(actions, oldFolderNameSets)
    setLinkMode(actions, newFolderNameSets)

    setFileContent(script, oldFolderNameSets, newFolderNameSets)


def getPairList(strList):
    pairList = []
    pair = []
    i = 0
    while i < len(strList):
        if len(strList[i]) == 0:
            if len(pair) == 0:
                pair.append(i)
            elif len(pair) == 1:
                pair.append(i-1)
                pairList.append(pair)
                pair = [i]
        i += 1
    else:
        pair.append(len(strList)-1)
        pairList.append(pair)
    return pairList


def setLinkMode(actions, strList):
    pairList = getPairList(strList)
    actIdx = 0
    pairIdx = 0
    delIdx = []
    while actIdx < len(actions):
        if actions[actIdx]["isLinkMode"] == False:
            actIdx += 1
            pairIdx += 1
            continue
        else:
            p1 = pairList[pairIdx][0] + 1
            p2 = pairList[pairIdx][1]
            while p1 < p2:
                last1 = strList[p2]
                last2 = strList[p2 - 1]
                lastStr1 = "".join(last1)
                lastStr2 = "".join(last2)
                if lastStr1 in lastStr2:
                    delIdx.append(p2)
                p2 -= 1
        actIdx += 1
        pairIdx += 1
    else:
        delIdx.sort()
        while len(delIdx) > 0:
            pop = delIdx.pop()
            del strList[pop]


def setFileContent(script, oldNameSets, newNameSets):
    if "oldFileContent" in script and "newFileContent" in script:
        return

    oldNameSets = np.array(oldNameSets, dtype=list)
    newNameSets = np.array(newNameSets, dtype=list)

    filted = compareAndFilterDuplicate(oldNameSets, newNameSets)

    oldNameSets = filted[0]
    newNameSets = filted[1]

    oldFileContent = joinPrefix(script['prefix'], oldNameSets)
    newFileContent = joinPrefix(script['prefix'], newNameSets)

    script["oldFileContent"] = oldFileContent
    script["newFileContent"] = newFileContent


def setFolderPaths(script, oldNameSets):
    if "oldFolderPaths" in script and "newFolderPaths" in script:
        return

    newNameSets = createNewNameSetForPaths(
        oldNameSets,
        script["dictionary"]
    )

    oldFolderNamePaths = joinSubPath(script["actions"], oldNameSets)
    newFolderNamePaths = joinSubPath(script["actions"], newNameSets)

    script["oldFolderPaths"] = oldFolderNamePaths
    script["newFolderPaths"] = newFolderNamePaths


def createNewNameSetForPaths(nameSets, dic):
    newList = []
    for nameSet in nameSets:
        li = []
        if len(nameSet) > 0:
            idx = 0
            while idx < len(nameSet):
                if idx == len(nameSet) - 1:
                    s = nameSet[-1]
                    li.append(dic[s])
                else:
                    li.append(nameSet[idx])
                idx += 1
        newList.append(li)
    return newList


def createRandomSets(n):
    length_of_string = 6
    randomSets = []
    i = 0
    while i < n:
        r = ""
        for _ in range(length_of_string):
            r += random.choice(string.ascii_lowercase)
        randomSets.append(r)
        i += 1
    return randomSets


def findAllPathsInGraph(graph, start):
    visitedList = [[]]

    def dfs(graph, currVertex, visited):
        visited.append(currVertex)
        for vertex in graph[currVertex]:
            if vertex not in visited:
                dfs(graph, vertex, visited.copy())
        visitedList.append(visited)

    dfs(graph, start, [])
    return visitedList


def destructuringAssignment(origCombi, newCombi):
    for combi in newCombi:
        origCombi.append(combi)


def compareAndFilterDuplicate(list1, list2):
    newList1 = []
    newList2 = []
    idx = 0
    while idx < len(list1):
        if list1[idx] not in newList1:
            newList1.append(list1[idx])
            newList2.append(list2[idx])
        idx += 1
    return [newList1, newList2]


def joinPrefix(prefix, list2D):
    newList = []
    for pf in prefix:
        for l in list2D:
            newStr = []
            for s in l:
                newStr.append(pf + s)
            if len(l) > 0:
                newList.append("".join(newStr))
    return newList


def joinSubPath(actions, strList):
    newList = []
    actionsIdx = 0
    strListIdx = 1
    while actionsIdx < len(actions) and strListIdx < len(strList):
        subPath = actions[actionsIdx]["subPath"]
        mainPath = subPath
        if len(strList[strListIdx]) == 0:
            if "isPassGraphRoot" in actions[actionsIdx] and actions[actionsIdx]['isPassGraphRoot']:
                newList.pop()
            actionsIdx += 1
            strListIdx += 1
            continue
        for path in strList[strListIdx]:
            mainPath = mainPath + "/" + path

        newList.append(mainPath)
        strListIdx += 1
    else:
        if "isPassGraphRoot" in actions[actionsIdx] and actions[actionsIdx]['isPassGraphRoot']:
            newList.pop()
    return newList


def createDictionary(script):
    actions = script["actions"]
    dic = {}
    for action in actions:
        oldGraph = action["renameFolderGraph"]
        newGraph = action["newFolderGraph"]
        oldName = list(oldGraph.keys())
        newName = list(newGraph.keys())
        i = 0
        while i < len(oldName):
            dic[oldName[i]] = newName[i]
            i += 1
        script["dictionary"] = dic
