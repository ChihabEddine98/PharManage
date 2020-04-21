import cx_Freeze
import sys
import os
from tkinter import *
import tkinter.ttk
import sys
from tkinter.simpledialog import *
import hashlib
from tkinter.messagebox import *
import time
from tkcalendar import Calendar, DateEntry
from gmplot import gmplot
import webbrowser
from urllib.request import urlopen
import json



base=None

os.environ['TCL_LIBRARY']=r'C:\Users\Chihab Eddine\AppData\Local\Programs\Python\Python36\tcl\tcl8.6'
os.environ['TK_LIBRARY']=r'C:\Users\Chihab Eddine\AppData\Local\Programs\Python\Python36\tcl\tk8.6'




if sys.platform=="win32":
    base="Win32GUI"

executable=[cx_Freeze.Executable("PharManage.py",base=base,icon="images/icon.ico")]

cx_Freeze.setup( name="PharManage",
                 options={"build_exe":{"include_files":[("images","images")]}},
                 version="1.0",
                 description=" Description du logiciel ! ",
                 executables=executable
                )

















