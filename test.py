#Script generates large files, change f_in to your own local path

f_in = open('C:\\Users\\Alastair\\Dropbox\\DataAnalysisProject\\FromMelinda\\GFunearthedallocnew.csv', 'rU')
f_out = open("csv_files\largefile.csv", 'w')
f_out.write(f_in.readline())
for i in range(0, 5):
    f_in.seek(0)
    f_in.readline()
    for line in f_in:
        f_out.write(line)