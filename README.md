# sim-batcher
 Python package used to automate large batch tests for DDSPF 2016

## Quick Setup Guide:
Requires:
* Python 3
* DDSPF 2016
* AutoHotKey

1. Download this code as a .ZIP file and extract it to a directory
2. Open the Command Prompt (cmd.exe) **as administrator** and navigate to that directory ("cd \<directory\>")
3. Run `pip install -r requirements.exe`
4. Open up the settings.py file in the text editor / IDE of your choice and change the filepaths as needed
5. Open DDSPF and load the league you want to use (DSFL only at present)
6. Launch utils/MousePosWatch.ank.ahk script, press Ctrl-J to start it, and use it to identify the mouse coordinates needed for settings.py (Press Esc to exit the MousePosWatch script)
7. In the Command Prompt, run `python batchtest.py input/exampleStrats.py --home KCC --away MIN -N 50` (or you can use any other team codes you want for home/away)
8. Message me on Discord if you have any issues to this point. Otherwise start defining your own strategies and running your own sim tests!