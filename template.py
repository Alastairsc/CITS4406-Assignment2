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
<link rel="stylesheet" href="../main.css">

<title>Analysis Report on {header}</title>

</head>
<body>

<nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#">Contents</a>
        </div>
        <div id="navbar" class="collapse navbar-collapse">
          <ul class="nav navbar-nav">
            <li><a href="#invalid">Invalid/Empty</a></li>
            <li><a href="#numerical">Numerical</a></li>
            <li><a href="#string">String</a></li>
            <li><a href="#enum">Enum</a></li>
            <li><a href="#email">Email</a></li>
            <li><a href="#currency">Currency</a></li>
            <li><a href="#boolean">Boolean</a></li>
          </ul>
        </div>
      </div>
    </nav>

<br>&nbsp<br>
<div class="container">
    <h1>Analysis Report on {header}</h1>
</div>

<div class="container">
    <div class="row">
        <hr id="invalid"/>
        <div class="col-md-6">
            <h2>Invalid Rows ({len_invalid_rows})</h2>
            <p>These rows contain either too many or too few columns.</p>
            {invalid_rows}
        </div>

        <div class="col-md-6">
            <h2>Empty Columns ({len_empty_columns})</h2>
            <p>These columns contain >= 90% empty values.</p>
            {empty_columns}
        </div>
        
        <div class="col-md-6">
            <h2>Error Columns ({len_error_columns})</h2>
            <p>These column/row combinations contain invalid values.</p>
            {error_columns}
        </div>
    </div>
</div>

<div class="container">
    <div class="row">
        <div class="col-md-12">
            <h2>Column Analysis (Based on {len_columns} rows)</h2>
            <hr id="numerical"/>
            <h2>Numerical</h2>
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
                    <th>Normally Distributed</th>
                    <th>Standard Deviation</th>
                    <th>Outliers</th>
                    <th>Most Common (Top 5)</th>
                    <th>Least Common (Top 5)</th>
                    <th>Unique Items</th>
                </tr>
                {numerical_analysis}
            </table>
            
            <hr id="string"/>
            <h2>String</h2>
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
            
            <hr id="enum"/>
            <h2>Enumerated</h2>
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
            
            <hr id="email"/>
            <h2>Email</h2>
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
            
            <hr id="currency"/>
            <h2>Currency</h2>
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
                    <th>Normally Distributed</th>
                    <th>Standard Deviation</th>
                    <th>Outliers</th>
                    <th>Most Common (Top 5)</th>
                    <th>Least Common (Top 5)</th>
                    <th>Unique Items</th>
                </tr>
                {currency_analysis}
            </table>
            
            <hr id="boolean"/>
            <h2>Boolean</h2>
            <table class="table table-bordered table-hover">
                <tr>
                    <th>Column</th>
                    <th>Mode</th>
                    <th>Most Common (Top 5)</th>
                    <th>Least Common (Top 5)</th>
                    <th>Unique Items</th>
                </tr>
                {boolean_analysis}
            </table>
            
        </div>
    </div>
</div>

<script src="https://code.jquery.com/jquery-2.1.4.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
</body>
"""
