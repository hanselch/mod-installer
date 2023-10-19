# Double checking if you have dependecies shown on top
import tkinter as tk 
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import *
import os, webbrowser, json, importlib.util
import subprocess, sys
import zipfile, shutil, glob

#------------------------------------------------
# Double checking if you have the request library
libraries = ['gdown']
for l in libraries:
    if importlib.util.find_spec(l) is None:
        print(f"\033[32m Installing '{l}'...\033[39m")
        subprocess.check_call([sys.executable, "-m", "pip", "install", l])
    else:
        print(f"\033[32m {l} is found in system.")

import gdown

#------------------------------------------------
# Getting the main Minecraft File
getUser = os.environ.get('USERNAME')
default_dir = f"C:/Users/{getUser}/AppData/Roaming/.minecraft/mods"
# Double checking if user has the directory above
if os.path.exists(default_dir):
    print(f"\033[32m Directory; {default_dir} is found!\033[39m")
else:
    print(f"\033[31m Directory; {default_dir} is not found!\033[39m")
    print("Creating directory...")
    os.mkdir(default_dir)
    print(f"\033[32m Directory; {default_dir} has been created\033[39m")

# Setting up json file
configPwd = os.path.dirname(os.path.abspath(__file__)) + "\config.json"
print(configPwd)
with open(configPwd, "r") as config:
    getConfig = json.load(config)
# Showing URL for download
print(f"\033[32m Set url; {getConfig['config'][0]['url']}\033[39m")    
    
#Double checking if the default directory is set 
if getConfig["config"][0]["default"] == "":
    print("\033[31m \"default\" value in config.json isn't found, setting it up...\033[39m")
    getConfig["config"][0]["default"]=default_dir
    with open(configPwd, "r+") as config:
        json.dump(getConfig, config, indent=4)
    print(f"\033[32m Set up for {getConfig['config'][0]['default']}, is set!")
else:
    print(f"\033[32m \"default\" value in config.json is found; {getConfig['config'][0]['default']}\033[39m")
config.close()

#------------------------------------------------
# Configuring the main window 
mainWindow = tk.Tk()
mainWindow.title("Mod Installer Setup")
mainWindow.resizable(width=False, height=False)
mainWindow.config(bg="black")

# Setting up the title
title = tk.Label(text="Mod Installer Setup", font=('Helvetica', 18, 'bold'), fg="white", bg="black")
title.grid(row=0,column=0,columnspan=2)

def addMods():
    # Set up 
    with open(configPwd, "r") as config:
        getConfig = json.load(config)
    url = getConfig["config"][0]["url"]

    # Have the zip folder be in the mods folder
    print(f"\033[32m Installting the mods...\033[39m")
    file = f'{getConfig["config"][0]["default"]}/mods.zip'
    gdown.download(url, file, quiet=False)
    print(f"\033[32m Mods succesfully installed from {url}!\033[39m")

    # Export all contents in to the mods folder
    print(f"\033[32m Extracting {file}...\033[39m")
    with zipfile.ZipFile(file, mode="r") as modZip:
        modZip.extractall(getConfig["config"][0]["default"])
    print("\033[32m COMPLETE!")
    os.remove(file)
    print(f"\033[32m Deleted {file}!\033[39m")

    # Double check if the contents is all good
    with open(f"{getConfig['config'][0]['default']}/_listedMods.txt", 'r') as listedMods:
        modDir = os.listdir(getConfig["config"][0]['default'])
        lines = [line.rstrip() for line in listedMods]
        print("\033[32m Double checking if mods are made..\033[39m")
        notFoundMods = []
        for l in lines:
            if l in modDir:
                print(f"\033[32m Found {l} in mod directory\033[39m")
                continue
            elif l == "_listMods.txt":
                continue
            elif l not in modDir:
                print(f"\033[31m {l} is not found in mod directory...\033[39m")
                notFoundMods.append(l)
        if len(notFoundMods) != 0:
            print(f"Below are mods not originally added.. Double check if they are yours, and wanted to keep them and check version too!")
            for i in notFoundMods:
                print(f"\033[31m{i}\033[39m")
    os.remove(getConfig['config'][0]['default'] + "/_listedMods.txt")
    listedMods.close()
    config.close()
    messagebox.showinfo(message="Mods are succesfully installed/updated! Closing program.")
    mainWindow.destroy()
#------------------------------------------------
# Function for browsing the files
def browseFiles():
    modDirSelect = filedialog.askdirectory(title="Select Directory")    
    if modDir != default_dir:
        setDef = messagebox.askyesnocancel(message=f"Do you want to have\n{modDirSelect}\nas the default for future installs/updates?")
        if setDef == True:
            with open(configPwd, "r+") as config:
                getConfig = json.load(config)
            getConfig["config"][0]["default"]=modDirSelect
            with open(configPwd, "w") as config:
                json.dump(getConfig, config, indent=4)
            print(f"\033[32m Set up for {getConfig['config'][0]['default']}, is set!")
        else:
            pass
    else:
        pass
    modDir.delete(0, 'end')    
    modDir.insert(0, modDirSelect) 
    # Ask if you want it as a defualt

# Adding a entry to manully set up directory location if needed
# global modDir
with open(configPwd, "r") as config:
    getConfig = json.load(config)
modDir = tk.Entry(width=35, highlightbackground="black", highlightthickness=1)
modDir.insert(0,getConfig['config'][0]['default'])
modDir.grid(row=1, column=0, pady=5)
# Adding the button to set enter selected mod
setModDir = tk.Button(width=15, text="Browse Mod Folder", command=browseFiles)
setModDir.grid(row=1,column=1,pady=5)
config.close()

# GUI display for above
addModButton = tk.Button(text="Start Extraction", command=addMods, width=25)
addModButton.grid(row=4,column=0,pady=5)

#------------------------------------------------
# Side button for updating mods
def updateMods():
    with open(configPwd, "r") as config:
        getConfig = json.load(config)
    addBackup = messagebox.askyesnocancel(
        message=f"All the mods in the {getConfig['config'][0]['default']} folder will be deleted.\nDo you want to create backup to all the mods in a seperate folder?\n\nNOTE: The original 'Backed Mods' folder will be removed, if you originally have one."
        )
    if addBackup is True:
        backedModsDir = os.path.dirname(os.path.abspath(__file__)) + "\Backed Mods"
        try:
            shutil.rmtree(backedModsDir)
        except Exception:
            pass 
        shutil.copytree(getConfig["config"][0]['default'], backedModsDir)
        print(f"\033[32m Mods succesfully backed up to {backedModsDir}.")
        files = glob.glob(getConfig['config'][0]['default']+"\*")
        for f in files:
            os.remove(f)
        addMods()
    else:
        files = glob.glob(getConfig['config'][0]['default']+"\\*")
        for f in files:
            os.remove(f)
        addMods()

updateModButton = tk.Button(text="Update Mods", command=updateMods, width=25)
updateModButton.grid(row=4,column=1,pady=5)

#------------------------------------------------
def goToHelp():
    webbrowser.open_new(r"help.html")
link = tk.Button(mainWindow, text="Confused? Click here", command=goToHelp)
link.grid(row=6,column=1,pady=5)

#------------------------------------------------
# Just to keep the window updated
mainWindow.mainloop()
