"""Main execution body for program. Contains GUI interface and exporting class that creates files instead
of generating HTML Reports

Author: Alastair Chin
Last Updated: 28/02/2017
"""

import argparse
import webbrowser
import textwrap
import pandas as pd
import os
from tkinter import *
from tkinter import filedialog, ttk
from threading import Thread
from functools import partial
try:
    from .data import *
    from .report import *
    from .template_reader import *
except SystemError:
    from data import *
    from report import *
    from template_reader import *

terminal = False

"""
    Global Variables:
        terminal -- boolean value whether program is running through terminal or through GUI
        progress -- Progress bar showing progress through program
"""
class DisplayWindow:
    """GUI for application allowing users to interact with program in simpler and more explanatory way

    Methods:
        dataaskopenfile -- Asks for files to process and displays them in the output window
        dataaskopenfolder -- Asks for folder to process and displays the contained files in the output window
        filetext -- Fills output box given a list of files
        maketemplate -- Links to Create template web page of Data-oracle website
        process_report -- Runs program and generates report for all files processed
        process_export -- Runs program and creates a file containing analysis of all files processed
        removefile -- Removes file from being processed after being selected in output window
        reset -- Resets the program removing all files from the process queue and sets progress bar back to the start
        templateaskopenfile -- Asks for a template to use during processing and displays it in the output window

    Variables:
        datafiles -- list of datafiles to be processed
        display -- output window Frame object
        template -- template to use in process if applicable
    """
    def __init__(self):
        root = Tk()
        root.wm_title("UWA Data-oracle")
        self.datafiles = []
        self.template = None
        #Main Window
        mainwindow = Frame(root)
        self.display = Frame(mainwindow)
        Label(mainwindow, text="Select File(s) or Folder(s) to process: ").grid(row=0, sticky=E, pady=10)
        Label(mainwindow, text="Select template file(optional): ").grid(row=1, sticky=E, pady=10)
        label3 = Label(mainwindow, text="> Create Template", fg="blue")
        label3.bind("<Button-1>", self.maketemplate)
        label3.grid(row=2)

        Button(mainwindow, text="Browse Files...", command=  self.dataaskopenfile).grid(row=0, column=1, padx=5, sticky='ew')
        Button(mainwindow, text='Browse Folders...', command=  self.dataaskopenfolder).grid(row=0, column=2, padx=5)
        Button(mainwindow, text="Browse Templates...", command=self.templateaskopenfile).grid(row=1, column=1, padx=5)
        Button(mainwindow, text="View Report", command=self.process_report).grid(row=4, column=1,sticky='ew', padx=5)
        Button(mainwindow, text="Export", command=self.process_export).grid(row=4, column=2, sticky='ew')
        Button(mainwindow, text="Reset", command=self.reset).grid(row=6, column=1, sticky='ew')
        Button(mainwindow, text="Exit", command=mainwindow.quit).grid(row=6, column=2, sticky='ew', pady=5)
        global progress #global allowing access from all methods
        progress = ttk.Progressbar(mainwindow, orient="horizontal", mode="determinate")
        progress.grid(row=5, columnspan=3, sticky='ew', padx=10, pady=5)
        mainwindow.pack()

        #Output Window
        self.display.grid(row=0, column=3, rowspan=7, sticky=N)

        #Status Bar
        global statusText
        statusText = StringVar()
        statusText.set("Waiting for File...")
        status = Label(root, textvariable=statusText, bd=1, relief=SUNKEN, anchor=W)
        status.pack(side=BOTTOM, fill=X)

        root.mainloop()

    def dataaskopenfile(self):
        """ Asks for files to process and displays them in the output window"""
        self.reset()
        if self.template != None:
            Label(self.display, text=str("Template Selected: " + self.template.name), anchor='w').pack(fill=X)
        self.datafiles = filedialog.askopenfiles(mode='r', filetypes=[('All Files', '.*'),('Csv Files','*.csv'),
                                                 ('Excel Workbook', '*.xlsx'), ('Excel 97-2003 Workbook', '.xls')],
                                                 defaultextension="*.csv")
        self.datafiles = [file.name for file in self.datafiles]
        Label(self.display, text="Selected Files: ", anchor='w').pack(fill=X)
        self.filetext(self.datafiles)
        statusText.set("Ready to Process Files...")
        return self.datafiles

    def dataaskopenfolder(self):
        """Asks for folder to process and displays the contained files in the output window"""
        self.reset()
        if self.template != None:
            Label(self.display, text=str("Template Selected: " + self.template.name), anchor='w').pack(fill=X)
        folder = filedialog.askdirectory()
        self.datafiles = []
        for file in os.listdir(folder):
            self.datafiles.append(os.path.join(folder,file))
        Label(self.display, text=str("Selected Folder: " + folder), anchor='w').pack(fill=X)
        self.filetext(self.datafiles)
        return folder

    def filetext(self, files):
        """Provides text for output box given a list of files"""
        remove_file = lambda x, m: (lambda p: self.removefile(x, m))
        for file in files:
            label = Label(self.display, text=str("\t" + file), anchor='w')
            label.bind("<Button-3>", remove_file(file, label))
            label.pack(fill=X)

    def maketemplate(self, event):
        """Opens webbrowser to create template page on Data-oracle website"""
        webbrowser.open_new("http://35.165.229.31/upload/createTemplate/")

    def process_report(self):
        """Runs program and generates report at the end"""
        progress["value"] = 0
        statusText.set("Processing Files...")
        thread = Thread(target=process_files, args=(self.datafiles, self.template))
        thread.start()

    def process_export(self):
        """Runs program and exports results to file"""
        progress["value"] = 0
        statusText.set("Processing Files...")
        exportfile = filedialog.asksaveasfile(mode='w', defaultextension='*.csv', filetypes=[('Csv Files', '*.csv'),
                                                                                                 ('All Files', '.*')])
        exportfile.close()
        thread = Thread(target=process_files, args=(self.datafiles, self.template, exportfile.name))
        thread.start()

    def removefile(self, file, label):
        """Removes file from process list and removes label"""
        print("Removing: ", file)
        self.datafiles.remove(file)
        label.destroy()

    def reset(self):
        """Resets all files"""
        mainwindow = self.display.winfo_parent()
        mainwindow = self.display._nametowidget(mainwindow)
        self.display.destroy()
        self.display = Frame(mainwindow)
        self.display.grid(row=0, column=3, rowspan=7, sticky=N)
        statusText.set("Waiting for File...")
        progress["value"] = 0

    def templateaskopenfile(self):
        """Asks for template to use in processing"""
        self.template = filedialog.askopenfile(mode='r', filetypes=[('All Files', '.*'), ('Csv Files', '*.csv')],
                                               defaultextension="*.csv")
        Label(self.display, text=str("Template Selected: " + self.template.name), anchor='w').pack(fill=X)
        statusText.set("Ready to Process Folder...")
        return self.template

class Exporter(object):
    """Class that creates a file containing analysis of all files run in program

    Methods:
        write_stats -- writes summary of a single data object
        write_summary -- writes summary of all files to be run after processing all files

    Variables:
        filename -- file name to save export file as
        total_files -- total number of files processed
        total_invalid -- total number of invalid rows
        total_empty -- total number of empty columns
        total_errors -- total numher of errors throughout files
    """
    def __init__(self, filename):
        self.filename = filename
        self.total_files = 0
        self.total_invalid = 0
        self.total_empty = 0
        self.total_errors = 0

    def write_stats(self, data):
        """Writes statistics of a single data object"""
        with open(self.filename, 'r+') as fp:
            fp.seek(0,2)
            fp.write("Analysis of " + os.path.split(data.filename)[1] + '\n')
            self.total_files += 1
            fp.write("Number of Invalid rows:  " + str(len(data.invalid_rows)) + '\n')
            self.total_invalid += len(data.invalid_rows)
            empty_columns = [column.header for column in data.columns if column.empty]
            fp.write("Number of Empty Columns:  " + str(len(empty_columns)) + '\n')
            self.total_empty = len(empty_columns)
            fp.write("Number of Error Cells:  " + str(len(data.errors)) + '\n')
            self.total_errors = len(data.errors)
            fp.write("Delimiter:  " + data.delimiter_type + '\n')
            fp.write("\n")

    def write_summary(self):
        """Writes summary of all files processed"""
        temp_file = os.path.join(os.path.split(self.filename)[0],"Tempfile")
        with open( temp_file, 'w')  as fp:
            fp.write("Error Report " + os.path.split(self.filename)[1] + "\n\n")
            fp.write("Total Files Analysed: " + str(self.total_files) + "\n")
            fp.write("Total Invalid Rows: " + str(self.total_invalid) + "\n")
            fp.write("Total Empty Columns: " + str(self.total_empty) + "\n")
            fp.write("Total Errors: " + str(self.total_errors) + "\n\n")
            with open(self.filename, 'r') as fd:
                for line in fd:
                    fp.write(line)
        os.remove(self.filename)
        os.rename(temp_file, self.filename)



#TODO Export method after analysis has completed
def main(*args, exporter=None):
    """
    Create Data and Report objects, providing necessary information for them 
    to run analysis and create desired outputs (i.e. HTML report or writing to exported file).
    
        Keyword Arguments:
            args -- Arguments provided to the program at runtime.
            exporter -- Exporter object if applicable
    """
    #tr = classtracker.ClassTracker()
    #tr.track_class(Data)
    #tr.create_snapshot()
    filename = args[0]
    print("[Step 1/7] Processing file: ",filename)
    print("[Step 2/7] Reading data")
    if not terminal:
        global progress
        progress.step()
        global statusText
        statusText.set("Processing " + filename + "...")
    if len(args) > 1:
        temp = Template(args[1])
        data = Data(filename, temp)
    else:
        data = Data(filename)
    data.remove_invalid()
    data.create_columns()
    #tr.create_snapshot()
    data.clean()
    print("[Step 3/7] Running pre-analysis")
    if not terminal:
        progress.step()
    data.pre_analysis()
    #tr.create_snapshot()
    print("[Step 4/7] Finding Errors")
    if not terminal:
        progress.step()
    data.find_errors()
    #tr.create_snapshot()
    print("[Step 5/7] Running Analysis")
    if not terminal:
        progress.step()
        statusText.set("Running Analysis on " + filename + "...")
    data.analysis()
    #tr.create_snapshot()
    if exporter == None:
        report = Report(data)
        str_report = report.html_report()
        print("[Step 6/7] Generating report")
        html = report.gen_html(str_report)
        #returns string of html, also generates html report for debugging purposes
        print("[Step 7/7] Report Successfully Generated")
        print("Completed analysis for: ",filename)
        if not terminal:
            progress.step()
        webbrowser.open("file://"+html,new=2)
    else:
        print("[Step 6/7] Generating report")
        exporter.write_stats(data)
        print("[Step 7/7] Report Successfully Generated")
        if not terminal:
            progress.step()
        print("Completed analysis for: ", filename)
    if not terminal:
        statusText.set("Completed Analysis for " + filename)
    #tr.create_snapshot()
    #tr.stats.print_summary()
            
def get_file_dir(location):
    """Returns the directory of the file with the file name
    
    Keyword arguments:
        location -- A file path.
    """
    return location.rpartition('\\')

def process_files(files, templates, exportfile=''):
    """Process files and templates and runs the program over them. Converts excel files
    and applies template to each file

    Keyword arguments:
        files -- files to be processed
        templates -- files to use as templates in processing
        exportfile -- file to export analsysis to if applicable
    """
    filenames = []
    for file in files:
        name_ext = os.path.splitext(file)
        # TODO handle empty sheets
        if name_ext[1] == '.xls' or name_ext[1] == '.xlsx':
            print("[Step 0/7] Converting to csv file")
            xls = pd.ExcelFile(file)
            sheet_names = xls.sheet_names
            if len(sheet_names) == 1:
                df = xls.parse(sheet_names[0], index_col=None, na_values=['NA'])
                new_name = os.path.splitext(file)[0] + ".csv"
                df.to_csv(new_name, index=False)
                filenames.append(new_name)
            else:
                file_dir = os.getcwd()
                if not os.path.exists(os.path.join(file_dir, "csv_copies")):
                    os.makedirs(os.path.join(file_dir, "csv_copies"))
                    # makes new directory to store new csv files
                for sheet in sheet_names:
                    df = xls.parse(sheet, index_col=None, na_values=['NA'])
                    new_name = os.path.join(file_dir, "csv_copies", \
                                            os.path.splitext(os.path.split(file)[1])[0] + "_" + sheet + ".csv")
                    df.to_csv(new_name, index=False)
                    filenames.append(new_name)
        elif name_ext[1] == '.csv':
            filenames.append(file)
    if exportfile != '':
        export = Exporter(exportfile)
    else:
        export = None
    if not terminal:
        global progress
        progress["value"] = 0
        progress["maximum"] = len(filenames) * 5.0 + 0.01
    if templates != None:
        if len(templates) == 1:
            for name in filenames:
                main(name, templates, exporter=export)
        else:
            num_templates = len(templates)
            num_files = len(filenames)
            if (num_templates == num_files):
                for i in range(0, num_files):
                    main(filenames[i], templates[i], exporter=export)
            else:
                # TODO keep functionality when excel files have multiple sheets
                print("Error, different number of files and templates")
    else:
        for name in filenames:
            main(name, exporter=export)
    if export != None:
        export.write_summary()
    
if __name__ == '__main__':
    """If the program is run with application.py as the argument to the command line
    execution begins here. This will process all the command line arguments before 
    proceeding.
    """
    files = []
    templates = []
    if len(sys.argv) > 1:
        terminal = True
        pathname = os.path.dirname(sys.argv[0])
        parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,\
            description=textwrap.dedent('''\
                    Processes Csv files.
            ----------------------------------
            Can process one or more csv files. Can specify template to describe
            data further. Templates can be used to describe one or more csv files.
            If using multiple templates for multiple files list templates in the
            same order as the files they correspond to.
        '''))
        parser.add_argument('filenames', nargs='+',\
            help='one or more filenames for the processor to analyse')
        parser.add_argument('-t', nargs='+', metavar='template', help='a template for the given files')
        args = parser.parse_args()
        process_files(args.filenames, args.t)
    else:
        DisplayWindow()


