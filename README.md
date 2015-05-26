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
* Inconsistent row lengths
* Inconsistent types within columns
    * '-', dash character instead of None/NaN
    * '<1', numeric values with characters
* Blank values


### Desired analysis
* Numerical
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
Commas out of place will result in garbled results.

* Str identification/sorting of enumerated vs str
* Int's with leading 0's
* Implement testing