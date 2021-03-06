"""Provide a base HTML template variable for population with appropriate
statistics in the report.py module.
"""

base_template = \
"""
<head>

<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
<link rel="stylesheet" href="/static/report/main.css">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js"></script>
<script type="text/javascript" src="https://www.google.com/jsapi"></script>
<script src="/static/report/main.js"></script>
<script>
init();
{chart_data}
</script>
<title>Analysis Report </title>

</head>
<body>

<nav id="initialNavBar" class="navbar navbar-inverse navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
      <a class="navbar-brand" href={previous}>Back</a>
        </div>
        <div id="navbar" class="collapse navbar-collapse">
          <ul class="nav navbar-nav">
            <li><a href="#invalid">Invalid/Empty</a></li>
            <li><a href="#numerical">Numerical</a></li>
            <li><a href="#string">String</a></li>
            <li><a href="#boolean">Boolean</a></li>
            <li><a href="#enum">Enum</a></li>
            <li><a href="#identifier">Identifier</a></li>
            <li><a href="#datetime">Date Time</a></li>
            <li><a href="#date">Date</a></li>
            <li><a href="#time">Time</a></li>
            <li><a href="#day">Day</a></li>
            <li><a href="#email">Email</a></li>
            <li><a href="#char">Character</a></li>
            <li><a href="#hyper">Hyperlink</a></li>
            <li><a href="#currency">Currency</a></li>
          </ul>
        </div>
      </div>
    </nav>

<br>&nbsp<br>
<br>&nbsp<br>
<br>&nbsp<br>
<div class="container">
    <h1>Analysis Report of {filename}</h1>
</div>

<div class="container">
    <div class="row">
        <hr id="invalid"/>
        <div class="col-md-6">
            <h2 class="titleRow">Invalid Rows ({len_invalid_rows})</h2>
            <p>These rows contain either too many or too few columns.</p>
            {invalid_rows}
        </div>

        <div class="col-md-6">
            <h2 class="titleRow">Empty Columns ({len_empty_columns})</h2>
            <p>These columns contain >= 90% empty values.</p>
            {empty_columns}
        </div>
        <div class="col-md-6">
            <h2 class="titleRow">Anomaly Cells ({len_error_columns})</h2>
            <p>These cells contain invalid values.</p>
            {error_columns}
        </div>

        <div class="col-md-6">
            <h2 class="titleRow">Delimiter</h2>
            <p>This file contains the delimiter type:</p>
            <h4><b>{delimiter_type}</b></h4>
        </div>

        <div class="col-md-6">
            <h2 class="titleRow">Columns ({num_columns})</h2>
            <p>Detected columns and their determined type.<p>
            {column_details}
        </div>
    </div>
</div>

<div class="container">
    <div class="row">
        <div class="col-md-12">
            <h2 class="titleRow" id="col_analysis">Column Analysis (Based on {len_columns} rows)</h2>
            <h2 class="titleRow" id="charts_header">Charts</h2>
            <p>Click 'Show Data' at the end of the table to view a chart. (Disabled for offline reports)</p>
            <p>Note: If numerical/currency data contains more than 10,000 values only the top 10,000 will be displayed in the chart.</p>
            <h4>Showing chart for column:</h4>
            <div id="Stats_Chart_data" class='hidden'>data here</div>
            <div id="Stats_Chart" class='hidden' style="width: 900px; height: 500px;"></div>
            <hr id="numerical"/>
            <h2 class="titleRow">Numerical</h2>
            <table class="table table-bordered table-hover">
                <tr>
                    <th style="width:100px">Column</th>
                    <th>Most Common (Top 5)</th>
                    <th>Least Common (Top 5)</th>
                    <th>Unique Items</th>
                    <th>Range</th>
                    <th>Distribution</th>
                    <th>Quartiles</th>
                    <th>Outliers</th>
                </tr>
                {numerical_analysis}
                
            </table>
            
            <hr id="string"/>
            <h2 class="titleRow">String</h2>
            <table class="table table-bordered table-hover">
                <tr>
                    <th>Column</th>
                    <th>Mode</th>
                    <th>Most Common (Top 5)</th>
                    <th>Least Common (Top 5)</th>
                    <th>Unique Items</th>
                </tr>
                {string_analysis}
            </table>
            
            <hr id="boolean"/>
            <h2 class="titleRow">Boolean</h2>
            <table class="table table-bordered table-hover">
                <tr>
                    <th>Column</th>
                    <th>Mode</th>
                    <th>Most Common (Top 5)</th>
                    <th>Least Common (Top 5)</th>
                    <th>Unique Items</th>
                    <th>Total "True"</th>
                    <th>Total "False"</th>
                    <th>Total "Yes"</th>
                    <th>Total "No"</th>
                    <th>Total Boolean Values</th>
                </tr>
                {boolean_analysis}
            </table>
            
            <hr id="enum"/>
            <h2 class="titleRow">Categorised (Enumerated)</h2>
            <table class="table table-bordered table-hover">
                <tr>
                    <th>Column</th>
                    <th>Mode</th>
                    <th>Most Common (Top 5)</th>
                    <th>Least Common (Top 5)</th>
                    <th>Unique Items</th>
                </tr>
                {enum_analysis}
            </table>
            
            <hr id="identifier"/>
            <h2 class="titleRow">Identifier</h2>
            <table class="table table-bordered table-hover">
                <tr>
                    <th>Column</th>
                    <th>Mode</th>
                    <th>Most Common (Top 5)</th>
                    <th>Least Common (Top 5)</th>
                    <th>Unique Items</th>
                </tr>
                {identifier_analysis}
            </table>

            <hr id="datetime"/>
            <h2 class="titleRow">Datetime</h2>
            <table class="table table-bordered table-hover">
                <tr>
                    <th>Column</th>
                    <th>Mode</th>
                    <th>Most Common (Top 5)</th>
                    <th>Least Common (Top 5)</th>
                    <th>Unique Items</th>
                </tr>
                {datetime_analysis}
            </table>
            
            <hr id="date"/>
            <h2 class="titleRow">Date</h2>
            <table class="table table-bordered table-hover">
                <tr>
                    <th>Column</th>
                    <th>Mode</th>
                    <th>Most Common (Top 5)</th>
                    <th>Least Common (Top 5)</th>
                    <th>Unique Items</th>
                    <th>Dec - Feb Tally</th>
                    <th>Mar - May Tally</th>
                    <th>Jun - Aug Tally</th>
                    <th>Sep - Nov Tally</th>
                </tr>
                {date_analysis}
            </table>
            
            <hr id="time"/>
            <h2 class="titleRow">Time</h2>
            <table class="table table-bordered table-hover">
                <tr>
                    <th>Column</th>
                    <th>Mode</th>
                    <th>Most Common (Top 5)</th>
                    <th>Least Common (Top 5)</th>
                    <th>Unique Items</th>
                    <th>Most Common Hours (Top 5) (hour,count)</th>
                    <th>Least Common Hours (Top 5) (hour,count)</th>
                </tr>
                {time_analysis}
            </table>
            
            <hr id="day"/>
            <h2 class="titleRow">Day</h2>
            <table class="table table-bordered table-hover">
                <tr>
                    <th>Column</th>
                    <th>Mode</th>
                    <th>Most Common (Top 5)</th>
                    <th>Least Common (Top 5)</th>
                    <th>Unique Items</th>
                </tr>
                {day_analysis}
            </table>
            
            <hr id="email"/>
            <h2 class="titleRow">Email</h2>
            <table class="table table-bordered table-hover">
                <tr>
                    <th>Column</th>
                    <th>Mode</th>
                    <th>Most Common (Top 5)</th>
                    <th>Least Common (Top 5)</th>
                    <th>Unique Items</th>
                </tr>
                {email_analysis}
            </table>

            <hr id="char"/>
            <h2 class="titleRow">Character</h2>
            <table class="table table-bordered table-hover">
                <tr>
                    <th>Column</th>
                    <th>Mode</th>
                    <th>Most Common (Top 5)</th>
                    <th>Least Common (Top 5)</th>
                    <th>Unique Items</th>
                </tr>
                {char_analysis}
            </table>

            <hr id="hyper"/>
            <h2 class="titleRow">Hyperlink</h2>
            <table class="table table-bordered table-hover">
                <tr>
                    <th>Column</th>
                    <th>Mode</th>
                    <th>Most Common (Top 5)</th>
                    <th>Least Common (Top 5)</th>
                    <th>Unique Items</th>
                </tr>
                {hyper_analysis}
            </table>
            
            <hr id="currency"/>
            <h2 class="titleRow">Currency</h2>
            <table class="table table-bordered table-hover">
                <tr>
                    <th>Column</th>
                    <th>Min</th>
                    <th>Max</th>
                    <th>Mode</th>
                    <th>Mean</th>
                    <th>Median Low</th>
                    <th>Median</th>
                    <th>Median High</th>
                    <th>Standard Deviation</th>
                    <th>Outliers</th>
                    <th>Most Common (Top 5)</th>
                    <th>Least Common (Top 5)</th>
                    <th>Unique Items</th>
                </tr>
                {currency_analysis}
            </table>
            
            
            
        </div>
    </div>
</div>

<script src="https://code.jquery.com/jquery-2.1.4.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
</body>
"""
