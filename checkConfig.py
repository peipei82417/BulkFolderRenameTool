#!/usr/local/bin/python3
# coding=utf-8

import os
import json


def printWarningText(s):
    print("\033[93m" + s + "\033[0m")


def main(config, scripts):
    isConfigPass = checkMainConfig(config)
    if not isConfigPass:
        printWarningText('config 未通過檢查')
        exit()
    isScriptsPass = checkScriptsConfig(config, scripts)
    if not isScriptsPass:
        printWarningText('scripts 未通過檢查')
        exit()


def checkScriptPath(config, scripts):
    root = config["rootPath"]
    for script in scripts:
        paths1 = script["oldFolderPaths"]
        paths2 = script["newFolderPaths"]
        for path in paths1:
            if not isExistPaths(root + path):
                printWarningText(
                    script['title'] +
                    "腳本未通過\n" +
                    path + "\n目錄不存在, 請檢查後再繼續"
                )
                return False
        for path in paths2:
            if isExistPaths(root + path):
                printWarningText(
                    script['title'] +
                    "腳本未通過\n" +
                    path + "\n目錄已存在, 請檢查後再繼續"
                )
                return False
    return True


def isExistPaths(path):
    if not os.path.isdir(path):
        return False
    return True


def checkMainConfig(config):
    if not "rootPath" in config:
        printWarningText("rootPath is necessary key")
        return False
    if "rootPath" in config:
        if not isExistPaths(config["rootPath"]):
            printWarningText(config["rootPath"] + "\n目錄不存在, 請檢查後再繼續")
            return False
    return True


def checkScriptsConfig(config, scripts):
    for script in scripts:
        if not isActionsPass(config, script):
            return False

        if not isRenamePathsPass(script):
            return False

        if not isFileContentPass(script):
            return False

    return True


def isActionsPass(config, script):
    actions = script['actions']
    if len(actions) == 0:
        printWarningText("action is necessary key in actions")
        return False
    for action in actions:
        if "subPath" not in action:
            printWarningText("subPath is necessary key in action")
            return False
        else:
            path = config["rootPath"] + action["subPath"]
            if not isExistPaths(path):
                printWarningText(
                    script['title'] +
                    "腳本未通過\n" +
                    path + "\n子目錄不存在, 請檢查後再繼續"
                )
                return False

        if "isLinkMode" not in action:
            printWarningText("isLinkMode is necessary key in action")
            return False

        if "renameFolderGraph" not in action:
            printWarningText("renameFolderGraph is necessary key in action")
            return False

        if "newFolderGraph" in action:
            isSame = isSameStructure(
                action["renameFolderGraph"],
                action["newFolderGraph"]
            )
            if not isSame:
                return False
    return True


def isFileContentPass(script):
    if "oldFileContent" in script and "newFileContent" in script:
        isSame = isSameStructure(
            script["oldFileContent"],
            script["newFileContent"]
        )
        if not isSame:
            printWarningText(script['title'] + " 未通過檢查")
            printWarningText("oldFileContent & newFileContent 結構錯誤")
            return False

    elif "oldFileContent" not in script and "newFileContent" in script:
        printWarningText(script['title'] + " 未通過檢查")
        printWarningText("oldFileContent & newFileContent 必須同時設定")
        return False

    elif "oldFileContent" in script and "newFileContent" not in script:
        printWarningText(script['title'] + " 未通過檢查")
        printWarningText("oldFileContent & newFileContent 必須同時設定")
        return False

    return True


def isRenamePathsPass(script):
    if "oldFolderPaths" in script and "newFolderPaths" in script:
        isSame = isSameStructure(
            script["oldFolderPaths"],
            script["newFolderPaths"]
        )
        if not isSame:
            printWarningText(script['title'] + " 未通過檢查")
            printWarningText("oldFolderPaths & newFolderPaths 結構錯誤")
            return False

    elif "oldFolderPaths" not in script and "newFolderPaths" in script:
        printWarningText(script['title'] + " 未通過檢查")
        printWarningText("oldFolderPaths & newFolderPaths 必須同時設定")
        return False

    elif "oldFolderPaths" in script and "newFolderPaths" not in script:
        printWarningText(script['title'] + " 未通過檢查")
        printWarningText("oldFolderPaths & newFolderPaths 必須同時設定")
        return False

    return True


def isSameStructure(obj1, obj2):
    t1 = type(obj1)
    t2 = type(obj2)
    if t1 != t2:
        return False
    if isinstance(obj1, dict):
        keyList1 = list(obj1.keys())
        keyList2 = list(obj2.keys())
        if len(keyList1) != len(keyList2):
            return False
        valList1 = list(obj1.values())
        valList2 = list(obj2.values())
        if len(valList1) != len(valList2):
            return False
        i = 0
        while i < len(valList1):
            if len(valList1[i]) != len(valList2[i]):
                return False
            i += 1
        return True
    elif isinstance(obj1, list):
        return len(obj1) == len(obj2)
    return True
