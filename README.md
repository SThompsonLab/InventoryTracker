# Basic Lab Inventory System (BLIS)

# Creating new executable files
Executable files can be generated using the python package `pyinstaller` but must be generated using the operating system for which the executable will work. For example, a .EXE file for Windows must be generated in a Windows environment that has python, pyinstaller, and the various python packages used BLIS. To generate the executable, enter `pyinstaller --onefile BLIS.py`. This will generate the `dist` directory containing the executable file. Additionally, the `--noconsole` flag can be added to remove the debug window

For MacOSX, create the folder ```/Applications/BLIS/``` and copy the files ```BLIS``` and ```_START_BLIS.osx.sh``` there.

