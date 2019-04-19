import tkinter as tk
from tkinter import filedialog

import os
import csv

imgFileNames = [];

def readFile(file):
    with open(file, mode='r') as csv_file:
            reader = csv.reader(csv_file)
            index = 1
            for row in reader:
                if any(row[0] in sublist for sublist in imgFileNames):
                    print(str(index) + ': ' + row[0])
                else:
                    fileNames = [row[0], row[1]]
                    imgFileNames.append(fileNames)
                index = index + 1

def csvUpload():
    fname = filedialog.askopenfilename(initialdir = "/Downloads", title = "Select CSV file")
    try:
        readFile(fname)
    except:                     # <- naked except is a bad idea
            print("Open Source File", "Failed to read file\n'%s'" % fname)
    return

def readFolder(folder):
    skipped = ''
    for root, dirs, files in os.walk(folder):
        for filename in files:
            renamed = False
            for nameTouple in imgFileNames:
                if nameTouple[0].lower() == filename.lower() and nameTouple[0].lower() != nameTouple[1].lower():
                    renamed = True
                    os.rename(os.path.join(root, filename), os.path.join(root, nameTouple[1]));
            if renamed == False:
                skipped = skipped + filename + '\n'
    print(skipped);

def imgFolderUpload():
    fname = filedialog.askdirectory(initialdir = "/Downloads", title = "Select folder")
    if fname:
            try:
                readFolder(fname)
            except Exception as e:                     # <- naked except is a bad idea
                print(e)
            return


root = tk.Tk()
frame = tk.Frame(root)
frame.pack()

csvFile = tk.Button(frame,
                   text="Select CSV",
                   bg="green",
                   padx = 100,
                   command=csvUpload)
csvFile.pack(side=tk.LEFT)


imgFolder = tk.Button(frame,
                   text="Select Folder",
                   bg="green",
                   padx = 100,
                   command=imgFolderUpload)
imgFolder.pack(side=tk.LEFT)

exit = tk.Button(frame,
                   text="Quit",
                   bg="green",
                   padx = 100,
                   command=quit)
exit.pack(side=tk.RIGHT)


root.mainloop()
