  MirPredict
====================


MirPredict is a small app that is targeted at mapping micro RNA into their
corresponding RNA by using the two biggest engines: 'Diana' and 'MirDB'.
The app uses headless selenium browsers to scrap the data from the web, and 
then analyse it. The search proccess includes using data from two additional
data sources: 'ensembl' and 'MirBase'. 

<img src="shot_1.jpg" width="500">

### Download
1. Click the links below to download a setup file.
2. Install it localy on your PC. 


| Version      | Link |
| ----------- | ----------- |
| 1.0 | mirPredict_v1.0       |

### Tissue Expression
The Data is taken from www.proteinatlas.org database and contains four categories
of reliability: Approved, Enhanced, Supported, and Uncertain. In the app all
the Entries with reliability of Uncertain were omitted
In addition the levels of expressions are set from High to not detected
while there is another category 'Not Representative' which is ommited from
query.
