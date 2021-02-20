<p align="center">
  <img src="/src/mainICO.png" height="200" align="centre">
 </p>
<p align="center">

[![KeepSafe: Passing](https://img.shields.io/badge/KeepSafe-Passing-lightgreen)](https://github.com/imshawan/keepsafe-passwordmanager)
![License: MIT](https://img.shields.io/badge/License-MIT-Green)
![Code Size: 135](https://img.shields.io/badge/Code%20Size-195KB-blue)
![Release: 1.2.1](https://img.shields.io/badge/Release-1.3.1-informational)

</p>

# KeepSafe - Password Manager

KeepSafe is a free Powerful and secure password manager with a elegant design. It lets you manage all your credentials quickly and efficiently for local applications and online services in a single window. KeepSafe stores your credentials in an encrypted form to the database so that no one can access your sensitive information without your permission. Check here for <a href="/src/"> screenshots </a>

## Main Features of KeepSafe - Password Manager

* A simple, flat and minimal UI design
* Add, Modify, Delete records with ease
* All of your passwords are stored encrypted in the database
* Friendly User Account controls

## Requirements
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the modules from requirements.txt
```bash
pip install -r /path/to/requirements.txt
```
## Compiling into executable?
* Use pip to install PyInstaller
```bash
pip install pyinstaller
```
Compile to executable (*.exe) 
```bash
pyinstaller --onefile --noconsole keepsafe.py
```
Or use

```bash
pyinstaller --windowed --noconsole keepsafe.py
```
For advanced usage, if you want to create a windows setup installer
```bash
pyinstaller --noconfirm --windowed --noconsole --icon=<iconImage.ico> --version-file=<versionINFOFile.txt> keepsafe.py
# Replace iconImage.ico with the application icon file
# Replace versionINFOFile.txt with the version information text file
```
  
## Some Notes worth to be kept in mind!

* /resources/config.dat ----------------------> Contains user configurations
* /resources/keepsafe.db --------------------> The main database file

#### Files created under '/resources' folder are not to be played with and any changes made to the files may result in data loss AND I'm not responsible for that

<b>KeepSafe</b> is a Open-Source Password Manager for Windows. Send me your feedbacks, bug-reports and suggestions about KeepSafe to <a href="mailto:imshawan.dev049@gmail.com">imshawan.dev049@gmail.com</a>
