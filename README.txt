########################################
Install Instructions:
########################################
1. Make sure python version 3.5 or newer is installed properly and is
   added to the "path".
2. Only for the first time execute 'install.bat' in order to install the dependencies.
3. on Linux - Execute 'run.bash' to start the app.
   on PC - run 'mirPredict' or 'run.bat'.

########################################
               MirPredict
########################################
MirPredict is a small app that is targeted at mapping micro RNA into their
corresponding RNA by using the two biggest engines: 'Diana' and 'MirDB'.
The app uses headless selenium browsers to scrap the data from the web, and 
then analyse it. The search proccess includes using data from two additional
data sources: 'ensembl' and 'MirBase'. 
****************************************
- Files and Folders
	- searches_data: Here are located all the saved searches. The folder
			 can be cleared at all time.
		- AAAAAA_######: Common folder name contains 6 letters from the end of the
		 		 miR and 6 random digits.
				-diana.csv: All the data from
				-mirdb.csv:
	- ensembl:
  		- mart_export.csv: the Ensembl DB, if the file is old it can be deleted
                         and the app will download a new one.
****************************************
- Debug Modes:
  In order to use the Debug mode insert the following code line instead
  of the one in app.py: "controller = Controller(debug=)" and insert in the
  desired debug mode.
    - 'False' or no value - No Debug.
    - 'True' - The scraping browsers are not headless to see what went
		wrong.

- There are two Debug Functions that can be used in the __init__ function of 
  the controler: 
	- auto_search(search_id): directly opens a certain search results
****************************************
Tissue Expression
The Data is taken from www.proteinatlas.org database and contains four categories
of reliability: Approved, Enhanced, Supported, and Uncertain. In the app all
the Entries with reliability of Uncertain were omitted
In addition the levels of expressions are set from High to not detected
while there is another category 'Not Representative' which is ommited from
query.
****************************************