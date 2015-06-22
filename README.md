# CITS4406 - Assignment 2
Provide a Python file to perform basic cleansing and statistical analysis on data provided via a csv file. Ideally structure the project so that other students can easily pick up/extend the functionality at a later date.

### Data types
* Int
* Float
* Enumerated
* Str


### Cleansing
* Inconsistent row lengths
* Inconsistent types within columns
    * '-', dash character instead of ''
* Blank values

### Desired analysis
* Numerical
    * Minimum
    * First Quartile
    * Median
    * Mean
    * Third Quartile
    * Maximum
    * Mode
* Top 5 occurring results

Todo:
* Boolean type?
* Dates type
* Geo-cords type
* Cleansing of '<1', numeric values with characters - Currently excluded/not matched.
* Implement testing
* Nice to have handling of multiple input files?
* Create makefile with venv included to allow easier use of things like jinja2?


You can run the project by extracting the zip, and running 'python3 application.py *csv filename here*'. 
