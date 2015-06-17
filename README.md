# CITS4406 - Assignment 2
Provide a Python file to perform basic cleansing and statistical analysis on data provided via .csv. Ideally structure the project so that other students can easily pick up/extend the functionality at a later date.

### Data types
* Int
* Float
* Enumerated
* Str
* Dates?
* Geo-cords?

### Cleansing
* Inconsistent row lengths - Done
* Inconsistent types within columns
    * '-', dash character instead of '' - Done
    * '<1', numeric values with characters
* Blank values

### Desired analysis
* Numerical - Done
    * Minimum
    * First Quartile
    * Median
    * Mean
    * Third Quartile
    * Maximum
    * Mode?
* Top 5 occurring results

Todo:
* How does Python handle commas in a CSV value, e.g., 'Las Vegas, Nevada'
Commas out of place will result in garbled results. So long as enclosed in double quotes, no issue.

* Str identification/sorting of enumerated vs str

* Int's with leading 0's

* Implement testing
* Nice to have handling of multiple input files?
* Create makefile with venv included to allow easier use of things like jinja2?

Reader reads the csv file, and splits the rows with invalid lengths (too short/too long) from the rest of the data.
The format of the valid data returned is a list with the header value and a list of the row values. 
I.e, csv_data[0] is ['unitno', ['TKD0261', 'TKD0261', 'TKD0261', 'TKD0261', 'TKD0261', 'TKD0261', 'TKD0261']]
Cleaner converts cells with a value of '-' to '', and returns a new 'clean' list of data with columns that had >= 90% missing values stripped out. Again the 'stripped' values are also returned, for reporting later.
Evaluator isn't doing anything currently as I haven't come up with a satisfactory way of implementing it to append the column type onto the data set.
I.e. csv_data[i][2] should equal the column type (int/str/float/enum) after passing through Evaluator.
Analyser partially works, in that all the analysis required is there, it just hasn't been implemented to work on the actual data set.
Reporter, specifically HTMLReporter is working currently with functionality that has been implemented. It creates a HTML in the same directory as the source csv, with filename + '_report.html' (e.g., oil_original.csv_report.html), and shows the invalid rows and empty columns. See screenshot below for example.

You can run the project by extracting the zip, and running 'python application.py *csv filename here*'. Commenting/docstrings are largely missing currently; if you're uncertain about anything feel free to shoot me an email and I'll get back to you.