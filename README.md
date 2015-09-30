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


### Running the program
* The program requires Python3, the scipy module, numpy module, alabaster module and pandas 
* module to run, it is recommended that you install these via the python distribution "Anaconda"
* found here: http://continuum.io/downloads

###Directory Structure
* The source code is all in the main directory
* csv_files contains test files used to evaluate the program
* Sphinx contains documentation of classes and methods of the         	program

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
* Date
* Time
* Char
* Day
* Hyperlink


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

You can run the project by extracting the zip, and running 'python3 application.py *csv filename here*'. 
You can specify multiple files using 'python3 application.py *csv_fileame* *csv_filename*'
You can use templates using 'python3 application.py *csv_filaname* -t *template_name*'

You must run the program from the directory containing the source files.
csv_filanames must either be put in the source directory or specified using its absolute path
