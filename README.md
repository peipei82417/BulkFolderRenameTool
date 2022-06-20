# BulkFolderRenameTool

## 概述
- 使用 Python 所撰寫的批量修改資料夾工具。

## 目的
- 將繁瑣且冗長的批量修改工作改由程式執行，以降低人為操作所產生的疏失及疲倦感。

## 完整介紹

### 進行專案
1. 於 tasks 資料夾內創建專案資料夾，一個專案資料夾須包含以下內容，請參考 "[/tasks/[範例專案]](https://github.com/peipei82417/bulk-folder-rename-tool/tree/main/tasks/%5B%E7%AF%84%E4%BE%8B%E5%B0%88%E6%A1%88%5D)"。
     - config.json - 本次修改文件的基礎設定，
     請參考 "[/tasks/[範例專案]/config.json](https://github.com/peipei82417/bulk-folder-rename-tool/blob/main/tasks/%5B%E7%AF%84%E4%BE%8B%E5%B0%88%E6%A1%88%5D/config.json)". 
     
     - scripts 資料夾 - 存放修改行為的所有腳本，
     請參考 "[/tasks/[範例專案]/scripts/](https://github.com/peipei82417/bulk-folder-rename-tool/tree/main/tasks/%5B%E7%AF%84%E4%BE%8B%E5%B0%88%E6%A1%88%5D/scripts)"  

2. 撰寫 config.json 文件  

     - config.json 內定義了此專案之根目錄，所有的修改行為都會在此根目錄下進行。  

3. 於 scripts/內撰寫{00-99}.json 文件，{00-99}.json 會照順序依次進行，請參考 "[/tasks/[範例專案]/scripts/](https://github.com/peipei82417/bulk-folder-rename-tool/tree/main/tasks/%5B%E7%AF%84%E4%BE%8B%E5%B0%88%E6%A1%88%5D/scripts)"。
4. cd BulkFolderRenameTool  

5. python3 main.py  


### 主流程

當 python3 main.py 後:
1. 輸入專案編號  

2. 系統自動檢查所有設定檔與腳本  
3. 系統根據設定檔與腳本自動生成&組合亂數與路徑
     * ex1.
   "[/tasks/[範例專案]/scripts/01.json](https://github.com/peipei82417/bulk-folder-rename-tool/blob/main/tasks/%5B%E7%AF%84%E4%BE%8B%E5%B0%88%E6%A1%88%5D/scripts/01.json)" 會組合出
   "[/tasks/[範例專案]/demo/01.json](https://github.com/peipei82417/bulk-folder-rename-tool/blob/main/tasks/%5B%E7%AF%84%E4%BE%8B%E5%B0%88%E6%A1%88%5D/demo/01.json)" 的結果。
     * ex2.
   "[/tasks/[範例專案]/scripts/02.json](https://github.com/peipei82417/bulk-folder-rename-tool/blob/main/tasks/%5B%E7%AF%84%E4%BE%8B%E5%B0%88%E6%A1%88%5D/scripts/02.json)" 會組合出
   "[/tasks/[範例專案]/demo/02.json](https://github.com/peipei82417/bulk-folder-rename-tool/blob/main/tasks/%5B%E7%AF%84%E4%BE%8B%E5%B0%88%E6%A1%88%5D/demo/02.json)" 的結果。  
   
4. 系統根據設組合出的結果進行文件修改與資料夾改名。  

### 自定義後續流程

當主流程結束後可選擇是否進行後續流程，
使用者可以在 nextAction 資料夾內部自行撰寫 shell | python 腳本
讓後續流程依序執行。
     - 若要進行後續行為
  輸入 y 後輸入腳本編號即可。
     - 若不要進行後續行為
  輸入 n 即可退出程序。

### scripts/{00-99}.json 腳本詳細介紹

#### {00-99}.json 內"必填"參數介紹:
   1. title: string
      - 此腳本之主題/目的。  
     
   2. actions: Array<action>
      - action 陣列 action 介紹。  
     
   3. prefix: Array<string>
      - 單字組合用前綴詞。  
     
   4. filenameExtension: Array<string>
      - 需修改檔名的後綴詞。
      - 系統只會修改擁有此後綴詞之檔名。  
      
#### action 內參數介紹:  
   1. subPath(必填): string
      - 需改名的資料夾根目錄。  
     
   2. renameFolderGraph(必填): {string: Array<string>}
      - 為樹狀圖形的 key,value pair。  
      - 第 0 項為 start(root)。
      - key 值填寫 subPath 下需改名的所有資料夾。
      - value 值填寫 key 值所能抵達的路徑。  
     
   3. newFolderGraph(選填): {string: Array<string>}
      - 同為樹狀圖形的 key,value pair。
      - key 值填寫 subPath 下需改名的所有資料夾。
      - value 值填寫 key 值所能抵達的路徑。
      - 此選項 默認為 六位小寫英文亂數。
      - 若填寫此參數則需注意與 renameFolderGraph 參數的結構問題，
        這兩者 key,val "結構與路徑" 需完全吻合。  
     
   4. isLinkMode(必填): boolean
      - 系統將透過 renameFolderGraph 與 newFolderGraph 兩個參數自動組合所有路徑與單字。
      - 在 false 的情況下
        系統會組合所有可能的單字。
      - 在 true 的情況下
        系統只組合所有起點至終點的單字。 
     
   5. isPassGraphRoot(選填): boolean
      - 是否繞過圖形起點/根目錄，默認為 false。
      - 在 true 的情況下
        系統不會修改 renameFolderGraph 起點的名稱。  
     
#### {00-99}.json 內"選填"參數介紹:
   以下將以兩兩一組做說明:
     
   1. oldFolderPaths 與 newFolderPaths: Array<string>
      - 更名前後資料夾路徑。  
      - 在未填寫此參數的情況下
        系統會透過 actions 自動生成所有路徑。
      - 在有填寫此參數的情況下
        需注意兩者結構與陣列長度，
        oldFolderPaths 與 newFolderPaths 之間以索引值進行對應。
        (ex. 將 oldFolderPaths[1] 替換成 newFolderPaths[1])
        系統則會根據內容進行變更，並不會自動生成。
      - 若不想修改檔名 只需指派空陣列即可。  
     
   2. oldFileContent 與 newFileContent: Array<string>
      - 更名前檔案內文。  
      - 在未填寫此參數的情況下
        系統會透過 actions 自動生成所有內文。
      - 在有填寫此參數的情況下
        需注意兩者結構與陣列長度，
        oldFileContent 與 newFileContent 之間以索引值進行對應。
        (ex. 將 oldFileContent[1] 替換成 newFileContent[1])
        系統則會根據內容進行變更，並不會自動生成。
      - 若不想修改內文 只需指派空陣列即可。


