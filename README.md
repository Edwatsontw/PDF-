# PDF 合併工具 / PDF Merger Tool
作者:劉立詳/Edwatson  
https://github.com/Edwatsontw
---

# 🇹🇼 中文說明

# 簡介
PDF 合併工具 是一款輕量化的 Windows 桌面應用程式，提供直覺化的圖形介面，讓使用者能夠輕鬆合併多個 PDF 檔案，並自由設定每個檔案的擷取頁碼範圍。

# 功能特色
- 新增多個 PDF 檔案：支援一次選取多個檔案
- 自訂頁碼範圍：可針對每個 PDF 設定起始頁與結束頁
- 調整順序：自由拖曳或上下移動檔案排列順序
- 移除檔案：從清單中刪除不需要的檔案
- 合併輸出：將所有選定頁面合併為單一 PDF 檔案
- 支援加密 PDF：可讀取受保護的 PDF 文件
- 雙語言介面支援：內建英文與繁中

# 系統需求
| 項目 | 需求 |
|------|------|
| 作業系統 | Windows 10 / 11（64 位元）|
| Python 環境 | `不需要`（已內建）|
| 額外安裝 | `不需要`（單一執行檔）|

# 使用方式
1. 雙擊 `PDF合併工具.exe` 開啟程式
2. 點擊 `新增 PDF` 選取要合併的檔案
3. 若需要，雙擊列表中的檔案以設定頁碼範圍
4. 使用 `⬆ 上移` / `⬇ 下移` 調整合併順序
5. 點擊 `合併輸出`，選擇儲存位置
6. 完成！

# 注意事項
- 本程式為獨立執行檔，`無需安裝 Python`
- 第一次啟動可能需要數秒載入時間（正常現象）
- 若 Windows Defender 出現警告，請點選「仍要執行」

# 技術資訊
- 開發語言：Python 3.11
- GUI 框架：Tkinter / ttk
- PDF 處理：PyPDF2
- 打包工具：PyInstaller 6.x

---

# US English Documentation

# Overview
`PDF Merger Tool` is a lightweight Windows desktop application with an intuitive graphical interface. It allows users to easily merge multiple PDF files and customize the page range for each document.

# Features
- Add Multiple PDFs : Select multiple files at once
- Custom Page Range : Set start and end pages for each PDF
- Reorder Filesb : Move files up or down to adjust merge order
- Remove Files : Delete unwanted files from the list
- Merge & Export : Combine all selected pages into a single PDF
- Encrypted PDF Support : Read and process password-protected PDFs
- Multilingual Support : Built-in support for `English` and `Traditional Chinese`

# System Requirements
| Item | Requirement |
|------|-------------|
| Operating System | Windows 10 / 11 (64-bit) |
| Python Environment | `Not required` (bundled) |
| Additional Installation | `Not required` (standalone executable) |

# How to Use
1. Double-click `PDF合併工具.exe` to launch the application
2. Click `Add PDF` to select files you want to merge
3. Double-click any file in the list to set its page range (optional)
4. Use `⬆ Move Up` / `⬇ Move Down` to reorder files
5. Click  `Merge` and choose a save location
6. Done!

# Notes
- This is a `standalone executable` — no Python installation required
- The first launch may take a few seconds to load (this is normal)
- If Windows Defender shows a warning, click `Run anyway`

# Technical Details
- Language: Python 3.11
- GUI Framework: Tkinter / ttk
- PDF Engine: PyPDF2
- Packager: PyInstaller 6.x

---

This tool is for personal and educational use.
本工具僅供個人及學習用途使用。
