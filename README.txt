########################################
Install Instructions:
########################################
1. Make sure python 3 is installed properly and is added to the path.
2. Only for the first time execute 'install.bat' in order to install dependencies.
3. Execute 'run.bat' to start the app.

########################################
               MirPredict
########################################
MirPredict is a small app that is targeted at mapping micro RNA into their
corresponding RNA by using the two biggest engines: 'Diana' and 'MirDB'.
The app uses headless selenium browsers to scrap the data from the web,
afterward, it uses DB for RNA taken from 'ensembl', and does some analytics
in order to ease the right RNA to match the miR.
****************************************
- Files and Folders
	- searches_data: Here are located all the saved searches. The folder
			 can be cleared at all time.
		- AAAAAA_######: Common folder name contains 6 letters from the end of the
		 									miR and 6 random digits.
				-diana.csv: All the data from
				-mirdb.csv:
	- ensembl:
  	- mart_export.csv:

****************************************
- Proccess
	1.

****************************************
- Debug Modes:
  In order to use the Debug mode insert the following code line instead
  of the one in app.py: "controller = Controller(debug=)" and insert in the
  desired debug mode.
    - 'False' - No Debug.
    - '1' - The scraping browsers are not headless to see what went wrong.
    - 'AAAAAA_######' - Insert an existing search folder (any subfolder of one
       search not the entire folder of all the searches). know the app uses 
       the searches data and the main screen can be examined.

