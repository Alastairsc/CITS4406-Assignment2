# UWA Data Analysis
Provide a Python file to perform basic cleansing and statistical analysis on data provided via a csv file. Ideally structure the project so that other students can easily pick up/extend the functionality at a later date.

### Contributors
* Liam Jones
* Alastair Chin
* Jordan Hedges
* Kieran Richards
* Leighton Lilford
* Jan Villanueva
* Alastair Mory


###Instructions

1. Install python 3 from 	https://www.python.org/downloads/release/python-343/

2. Install the Anaconda package from:
	http://continuum.io/downloads

###Ubuntu

Run the terminal, navigate to the directory containing the applicaiton.py and run using
	'python3 application.py *csv filename here*'. 

###Windows

Run the program in windows powershell, navigate to the directory containing the application.py file and run using 
	'python application.py *csv filename here*'.


You can specify multiple files using 'python3 application.py *csv_fileame* *csv_filename*'
You can use templates using 'python3 application.py *csv_filaname* -t *template_name*'

You must run the program from the directory containing the application.py file.
csv_filanames must be specified by relative or using its absolute path


### Supported Data types
* Int
* Float
* Enumerated
* String
* Email
* Currency
* Boolean
* Scientific notation
* Identifier


### Cleansing
* Inconsistent row lengths
* Inconsistent types within columns
* Blank values

### Desired analysis
* Numerical
    * Minimum
	* Maximum
	* Mean
    * First Quartile
    * Median
    * Third Quartile
    * Standard deviation
    * Mode
	* Distribution type
	* Outliers
* Top 5 occurring results
* Bottom 5 occuring results
* Number of unique entries


###Directory Structure
* The source code is all in the main directory
* csv_files contains test files used to evaluate the program
* Sphinx contains documentation of classes and methods of the         	program
