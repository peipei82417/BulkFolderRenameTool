#!/usr/local/bin/python3
# coding=utf-8

import os
import shutil
from pathlib import Path


def main(config, scripts):
    for script in scripts:
        print("正在執行 " + script["title"] + " 修改文件內容")

        traverseAndReplaceFile(config["rootPath"], script)

        print(script["title"] + " 修改文件內容完成")

    for script in scripts:
        print("正在執行 " + script["title"] + " 重新命名資料夾")

        renameFolder(config["rootPath"], script)

        print(script["title"] + " 重新命名資料夾完成")


def renameFolder(root, script):
    oldFolderPaths = script["oldFolderPaths"]
    newFolderPaths = script["newFolderPaths"]

    idx = 0
    while idx < len(oldFolderPaths):
        src = root + oldFolderPaths[idx]
        dst = root + newFolderPaths[idx]

        moveToNewFolder(src, dst)
        deleteOldFolder(src)

        idx += 1


def delete_gap_dir(dir):
    for root, dirs, files in os.walk(dir):
        if not os.listdir(root):
            os.rmdir(root)


def traverseAndReplaceFile(rootPath, script):
    oldNameSets = script["oldFileContent"]
    newNameSets = script["newFileContent"]
    extensions = script["filenameExtension"]
    for file in traverseAllFile(rootPath, extensions):
        replaceFileContext(
            file,
            oldNameSets,
            newNameSets
        )


def traverseAllFile(base, extensions):
    for root, ds, fs in os.walk(base):
        idx = 0
        while idx < len(extensions):
            for f in fs:
                if f.endswith(extensions[idx]):

                    fullPath = os.path.join(root, f)
                    yield fullPath
            idx += 1


def replaceFileContext(file, oldNameSets, newNameSets):
    idx = len(oldNameSets) - 1
    while idx >= 0:
        old_str = oldNameSets[idx]
        new_str = newNameSets[idx]
        if old_str == new_str:
            idx -= 1
            continue
        file_data = ""
        with open(file, "r") as f:
            for line in f:
                if old_str in line:
                    line = line.replace(old_str, new_str)
                file_data += line
        with open(file, "w") as f:
            f.write(file_data)
        idx -= 1


def createFolder(dst):
    os.mkdir(dst)


def moveToNewFolder(src, dst):
    shutil.copytree(src, dst)


def deleteOldFolder(src):
    shutil.rmtree(src)
