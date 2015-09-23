"""Class for reading templates to pass on information about how
to process the data for the data class"""     
        
class Template(object):
    """Object storing user input that describes data given. Able to specify:
        Columns - state column number and data type
        Delimiter - state delimiter character (for comma use the word not ',')
        Start row - row of header (0 for no header)
        
        Columns and rows start at 1 not 0"""
        
    def __init__(self, filename):
        self.columns = {}
        self.delimiter = ''
        self.header_row = 0
        self.data_start = 1
        self.data_size = {}
        
        self.read(filename)
        
    def read(self, filename):
        """Reads template file, assumes correct formatting, if user editing
        is permitted will need to be improved with more checks"""
        with open(filename, newline='') as csvfile:
            f = csv.reader(csvfile, delimiter=',')
            for row in f:
                if len(row) > 1:
                    if row[0].lower() == 'column':
                        self.columns[int(row[1])-1] = row[2] #column numbering starts at 1 instead of 0
                        if len(row) > 3 and row[2] == 'Identifier' and row[3] == 'size':
                            self.data_size[int(row[1])-1] = int(row[4])
                    elif row[0].lower() == 'delimiter':
                        if(row[1] == 'comma'):
                            self.delimiter = ','
                        else:
                            self.delimiter = row[1]
                    elif row[0].lower() == 'header':
                        self.header_row = int(row[1]) - 1
                        print("Set header: ", self.header_row)
                    elif row[0].lower() == 'data_start':
                        self.data_start = int(row[1]) - 1
                        