# 🎩 Alfred Workflow - MacOS App Store Finder

Find MacOS Application with a keyword **"asf"**

*"asf" is short for **A**pp **S**tore **F**inder*

![demo](demo.gif)

## 🔨 Installation
1. Download workflow from [here](https://github.com/DoonDoony/alfred-workflow-app-store-finder/releases/latest/download/appstorefinder.alfredworkflow)
2. Open a downloaded file

## ✨ Features
- Provides App Store search results available in your country
- Only MacOS software search results are provided

## 🙇‍♂️ Built With
- Python 2.7.x
- [Alfred-Workflow](https://github.com/deanishe/alfred-workflow)
- [Poetry](https://python-poetry.org)

## 🎁 How to package 
```bash
$ poetry install --no-root
$ fab build  # Running the command will generate the .alfredworkflow file
```


## ✅ TODO
- [x] Do not download icon if a file already exists
- [x] Make a command "asfc" to delete icon images and caches
- [x] Build script
- [x] Lightweight by packaging only compiled files (.pyc)
