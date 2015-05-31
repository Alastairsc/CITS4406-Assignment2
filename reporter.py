__author__ = 'Liam'


class HTMLReport(object):
    """
    Creates a HTML based report based on results from the cleaner and analyser
    objects.
    """

    def __init__(self, csv_file, cleaner, analyser):
        html_str = """
<h1>CITS4401 Assignment 2 HTML Analysis Report on {}</h1>

<h2>Invalid Rows</h2>
{}

<h2></h2>
        """.format(
            csv_file,
            self.list_creator(cleaner.invalid_length_rows)
        )

        html_file = open("{}_report.html".format(csv_file), "w")
        html_file.write(html_str)
        html_file.close()

    @staticmethod
    def list_creator(list_items):
        html = '<ul>'
        for i in list_items:
            html += '<li>' + str(i) + '</li>'
        html += '</ul>'
        return html


class TxtReport(object):
    """
    Placeholder for creating a TXT based report.
    """

    def __init__(self):
        pass
