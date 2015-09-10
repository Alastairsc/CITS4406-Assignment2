"""Main execution body for Assignment2 project.
"""

import sys

from data import *
from report import *
from editor import *


def main(filePath):
    """Create Data and Report objects, providing necessary information for them 
    to run analysis and create desired outputs (i.e. HTML report).

    """
    file = filePath
    data = Data(file)
    data.clean()
    editor = Editor(data)
    data.analyse()
    editor.make_corrected(file)
    report = Report(data, file)
    report.html_report()


if __name__ == '__main__':
    numFiles = len(sys.argv)
    for i in range(1,numFiles):
        main(sys.argv[i])
