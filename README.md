# Basic Lab Inventory System (BLIS)

# Creating new executable files
Executable files can be generated using the python package `pyinstaller` but must be generated using the operating system for which the executable will work. For example, a .EXE file for Windows must be generated in a Windows environment that has python, pyinstaller, and the various python packages used BLIS. To generate the executable, enter `pyinstaller --onefile BLIS.py`. This will generate the `dist` directory containing the executable file. Additionally, the `--noconsole` flag can be added to remove the debug window

# MacOS

to build, you will first need to:
	* install XCode (Development tools) via App Store
	* install Python3 from https://www.python.org
	* run ```pip3 install pyinstaller``` 
	* run ```pip3 install PySimpleGUI```
	* run ```pip3 install pandas```

then, to actually do the build, as above
	* ```pyinstaller --onefile BLIS.py```
	* ```cp -a ./dist/BLIS BLIS.osx.$(uname -p)"
	* ```git commit BLIS.osx.$(uname -p)```
	* ```git push```

To "install":
   * create the folder ```/Applications/BLIS/``` 
   * copy the files there:
       * ```BLIS.osx.arm```
       * ```BLIS.osx.i386```
       * ```BLIS```
       * ```_START_BLIS.osx.sh```


