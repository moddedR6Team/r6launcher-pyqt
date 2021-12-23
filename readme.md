## Table of contents
* [General info](#general-info)
* [Features](#features)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
R6Launcher is a launcher written in Python made to launch old Siege versions

## Features
- Supports multiple, fully customizable profiles
- Run all Rainbow Six|Siege versions from one launcher
- Shows useful info about each installation, e.g. installation size

## Technologies
- Python3
- PyQt5
- Nuitka

## Setup
> ⚠️ **Warning**: it's strongly recommended to do all of this while being in a virtual environment

- Install all required dependencies by running the following command: `pip install pyqt5 nuitka qdarkstyle`
- Setup the UPX and 7Zip environment variables inside `build_release.bat` if you want to use either of these features (UPX strongly reduces the size of the final program, 7Zip is required to make an archive with the build). Note that neither of these are mandatory, and if you dont correctly setup them they will be just skipped.
- Run the `build_release.bat` (enter the venv first if you use one)
- Build will be in the `r6launcher.dist` folder (`R6Launcher.7z` will appear if you correctly setted up the 7Zip variable)

## Upcoming features
- Settings
- Edit profile
- Downloader directly in the launcher
- Mods/tools marketplace