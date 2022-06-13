#!/usr/local/bin/python3
# coding=utf-8

import taskManager
import checkConfig
import initialScript
import fileOperation


def printSuccessfulText(text):
    print("\033[1m\033[92m" + text + "\033[0m")


def main():
    taskName = taskManager.getTaskName()
    printSuccessfulText("開始執行" + taskName)

    config = taskManager.getMainConfig(taskName)
    scripts = taskManager.getToDoScripts(taskName)
    printSuccessfulText("成功獲取 " + taskName + " 設定檔與腳本")

    checkConfig.main(config, scripts)
    printSuccessfulText(taskName+" 設定檔與腳本通過檢查")

    initialScript.main(config, scripts)
    printSuccessfulText(taskName+" 腳本初始化成功")

    fileOperation.main(config, scripts)
    printSuccessfulText(taskName+" 修改文件及資料夾成功")

    printSuccessfulText("MAIN TASK SUCCESSFUL")

    printSuccessfulText("開始列印" + taskName + "報告")
    taskManager.printCoverage(taskName, config, scripts)
    printSuccessfulText(taskName + "報告列印成功")

    taskManager.runNextAction()
    printSuccessfulText("TASK FINISH")


if __name__ == "__main__":
    main()
