"""Analyser class for running analysis on columns depending on the column type"""


import re
from statistics import mode, StatisticsError

from math import floor, log10, pow, ceil

threshold = 0.9
max_Outliers = 100
standardDeviations = 3
re_date = re.compile('^((31(\/|-)(0?[13578]|1[02]))(\/|-)|((29|30)(\/|-)(0?[1,3-9]|1[0-2])(\/|-)))((1[6-9]|[2-9]\d)?\d{2})$|^(29(\/|-)0?2(\/|-)(((1[6-9]|[2-9]\d)?(0[48]|[2468][048]|[13579][26])|((16|[2468][048]|[3579][26])00))))$|^(0?[1-9]|1\d|2[0-8])(\/|-)((0?[1-9])|(1[0-2]))(\/|-)((1[6-9]|[2-9]\d)?\d{2})$')
re_dateDF = re.compile('^\d{1,2}(\/|-)((0?[12])|(12))')
re_dateMM = re.compile('^\d{1,2}(\/|-)(0?[3-5])')
re_dateJA = re.compile('^\d{1,2}(\/|-)(0?[6-8])')
re_dateSN = re.compile('^\d{1,2}(\/|-)((0?9)|(1[01]))')
re_time = re.compile('(^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$)|(^(1[012]|0?[1-9]):[0-5][0-9](\ )?(?i)(am|pm)$)')
re_timePM = re.compile('[pP][mM]$')
re_timeAM = re.compile('[aA][mM]$')
re_timehr = re.compile('^\d{1,2}')


class Analyser(object):
    """
    Base analysis class object. Initiate the object, and assigns the statistical mode, if any.
    
    Global variables:        
        max_Outliers -- the maximum amount of outliers that will be found.
        
        standardDeviations -- The number of standard deviations away from the mean a value is
        allowed to be before it is an error, default 3.  
        
        re_date --  A regular expression for dates.
    
        re_dateDF -- A regular expression for months December-February.
        
        re_dateMM -- A regular expression for months March-May
        
        re_dateJA -- A regular expression for months June-August.
        
        re_dateSN -- A regular expression for months September-November.
        
        re_time -- A regular expression for time.
        
        re_timePM -- A regular expression for PM times.
        
        re_timeAM -- A regular expression for AM times
        
        re_timehr -- A regular expression for the hour.
        
    Class variables:
        mode -- Returns the mode of the column analysed.
        
        unique -- The count of unique values in the column.
    
    Child classes and associated variables:
        StringAnalyser -- String column analysis.
        
        EmailAnalyser -- Email column analysis.
        
        EnumAnalyser -- Enumerated column analysis.
        
        NumericalAnalyser -- String/Float column analysis.
            min -- Minimum value in column values.
            
            max -- Maximum value in column values.
            
            mean -- Mean value in column values.
            
            lower quartile -- Lower quartile for column values.
            
            median -- Median value for column values.
            
            upper quartile -- Upper quartile for column values.
            
            normDist -- String Yes/No if columns value is normally distributed.
            
            stdev -- Standard deviation for column values, N/A if not normally distributed to
            within 95.5% confidence.
                    
            stDevOutliers -- List of values outside a certain number of standard deviations
            from the mean.
                        
        CurrencyAnalyser -- Child class of NumericalAnalyser
    
        BooleanAnalyser -- Boolean column analysis

        DateAnalyser -- Date column analysis

        TimeAnalyser -- Time column analysis

        CharAnalyser -- Character column Analysis

        DayAnalyser -- Day column Analysis

        HyperAnalyser -- Hyperlink column Analysis
        
        Class Methods:
            uniqueCount -- Returns the count of unique values in a list.
    """
    def uniqueCount(self, values):
        """Return the amount of unique values in the values list.
        
        Keyword arguments:
            values -- A list of values.
        """
        valSet = set()
        for vals in values:
            valSet.add(vals)
        return len(valSet)

    def __init__(self, values):
        try:
            self.mode = mode(values)
        except StatisticsError:
            self.mode = 'N/A'
        self.unique = self.uniqueCount(values)

class EmailAnalyser(Analyser):
    """Run email analysis, currently only using Analyser super class methods.
    
    Keyword arguments:
        Analyser -- An analyser object.
    """
    def __init__(self, values):
        super().__init__(values)
        # TODO Something actually useful for emails.
        
class NumericalAnalyser(Analyser):
    """Runs numeric analysis.
    
    Keyword arguments:
        Analyser -- An analyser object.    
    """
    def __init__(self, values, stdDevs): 
        new_values = []
        isNumeric = True
        for i in values:
            if i != '':
                try:
                    if "." in i:
                        new_values.append(float(i))
                    else:
                        new_values.append(int(i))
                except ValueError:
                    #assuming error cells are not passed to here
                    isNumeric = False
                    try:
                        print("Can't convert: ",i)
                    except UnicodeEncodeError:
                        # Character not recognised in python
                        pass
        values = [i for i in new_values]
        super().__init__(values)
        if isNumeric:
            self.stDevOutliers = []
            #standardDeviations = Decimal(stdDevs)
            length = len(values)
            if values:
                self.min = values[0]
                self.max = values[1]
            self.mean = 0
            for x in values:
                if x < self.min:
                    self.min = x
                if x > self.max:
                    self.max = x
                self.mean += x
            self.mean = self.mean /length
            self.stdev = 0
            for x in values:
                self.stdev += pow(x-self.mean, 2)
            self.stdev = pow(self.stdev/length, 1/2)
            values.sort()
            median_index = (length+1)/2 - 1
            qlow_index = (length+1)/4 - 1
            qup_index = 3*(length+1)/4 - 1
            if median_index % 1 == 0:
                self.median = values[int(median_index)]
            else:
                self.median = (values[floor(median_index)]+values[ceil(median_index)])/2
            if qlow_index % 1 == 0:
                self.quartile_low = values[int(qlow_index)]
                self.quartile_up = values[int(qup_index)]
            else:
                self.quartile_low = (values[floor(qlow_index)] + values[ceil(qlow_index)]) / 2
                self.quartile_up = (values[floor(qup_index)] + values[ceil(qup_index)]) / 2
            IQR = self.quartile_up - self.quartile_low
            outlier_count = 0
            for x, value in enumerate(values):
                if value < (self.quartile_low - stdDevs/2 * IQR) or value > (self.quartile_up + stdDevs/2 * IQR):
                    self.stDevOutliers.append("Row: %d Value: %s" % (x, value))
                    outlier_count += 1
            #if outlier_count > max_Outliers:
                #self.stDevOutliers = "%d outliers" % outlier_count
            self.max = self.round_significant(self.max)
            self.min = self.round_significant(self.min)
            self.mean = self.round_significant(self.mean)
            self.quartile_low = self.round_significant(self.quartile_low)
            self.quartile_up = self.round_significant(self.quartile_up)
            self.median = self.round_significant(self.median)
            self.stdev = self.round_significant(self.stdev)
        else:
            print("WARNING: Type error, cannot convert column to numerical value")
            self.min = 'N/A'
            self.max = 'N/A'
            self.mean = 'N/A'
            self.quartile_low = 'N/A'
            self.median = 'N/A'
            self.quartile_up =  'N/A'
            self.stdev = 'N/A'
            self.normDist = 'N/A'
            self.stDevOutliers = 'N/A'

    @staticmethod
    def round_significant(x):
        # Rounds to 6 significant figures
        if isinstance(x, int) and abs(x) < 1000000 and abs(x) > 0.000001 or x == 0:
            return x
        if abs(x) >= 1000000:
            return NumericalAnalyser.int_to_sci(x)
        return float('%.6g' % x)

    @staticmethod
    def int_to_sci(value):
        """Converts numbers into a string in scientific notation form

        Keyword arguments:
            value -- The value to be converted to scientific notation.
        """
        if value == 0:
            return "0E+0"
        power = floor(log10(abs(value)))
        base = round(value / pow(10, power), 5)

        if power > 0:
            return str(base) + "e+" + str(power)
        else:
            return str(base) + "e-" + str(power)

    @staticmethod
    def is_compatable(values):
        bad_values = 0
        for i in values:
            if i != '':
                try:
                    if "." in i:
                        float(i)
                    else:
                        int(i)
                except:
                    bad_values += 1
        if bad_values / len(values) >= threshold:
            return False
        return True

            
class CurrencyAnalyser(NumericalAnalyser):
    """Run currency analysis, using NumericalAnalyser as a super class. Removes
    currency symbols in values. 
    
    Keyword arguments:
        NumericalAnalyser -- A NumericalAnalyser object.
    """
    def __init__(self, values, stdDevs):
        temp_values = [i for i in values]
        for x, value in enumerate(temp_values):
                    temp_values[x] = re.sub('(\$)|(€)|(£)', '', value)
                    temp_values[x] = temp_values[x].replace('(','-')#negatives
                    temp_values[x] = temp_values[x].replace(')','')
                    temp_values[x] = temp_values[x].replace(',','') #long numbers
        super().__init__(temp_values, stdDevs)


    @staticmethod
    def is_compatable(values):
        temp_values = [i for i in values]
        for x, value in enumerate(temp_values):
                    temp_values[x] = re.sub('(\$)|(€)|(£)', '', value)
                    temp_values[x] = temp_values[x].replace('(','-')#negatives
                    temp_values[x] = temp_values[x].replace(')','')
                    temp_values[x] = temp_values[x].replace(',','') #long numbers
        return super(CurrencyAnalyser, CurrencyAnalyser).is_compatable(temp_values)



class StringAnalyser(Analyser):
    """Run string analysis, currently only using Analyser super class methods.
    
    Keyword arguments:
        Analyser -- An analyser object.
    """
    def __init__(self, values):
        super().__init__(values)
        #  TODO Implement some string exclusive statistics.

class IdentifierAnalyser(Analyser):
    """Run identifier analysis, currently only using Analyser super class methods.
    
    Keyword arguments:
        Analyser -- An analyser object.
    """
    def __init__(self, values):
        super().__init__(values)
        # TODO Implement some identifier exclusive statistics.
        
class EnumAnalyser(Analyser):
    """Run enumerated analysis, currently only using Analyser super class methods.
    
    Keyword arguments:
        Analyser -- An analyser object.
    """
    def __init__(self, values):
        super().__init__(values)
        #  TODO Implement some enum exclusive statistics.
                             
class BooleanAnalyser(Analyser):
    """Run boolean analysis, currently only using Analyser super class methods.
    
    Keyword arguments:
        Analyser -- An analyser object.
    """
    def __init__(self, values):
        super().__init__(values)

class SciNotationAnalyser(Analyser):
    """Run scientific notation analysis.
    
    Keyword arguments:
        Analyser -- An analyser object.
        
    Class Methods:
        int_to_sci -- Converts a a given number into a string in scientific notation form. 
    """
    def __init__(self, values, stdDevs):
        standardDeviations = stdDevs 
        new_values = []
        isNumeric = True
        for i in values:
            if i != '':
                try:
                    new_values.append(float(i))
                except:
                    isNumeric = False
                    print("Can't convert: ", i)
        values = [i for i in new_values]
        super().__init__(values)
        if isNumeric:
            length = len(values)
            self.stDevOutliers = []
            if values:
                self.min = values[0]
                self.max = values[1]
            self.mean = 0
            for x in values:
                if x < self.min:
                    self.min = x
                if x > self.max:
                    self.max = x
                self.mean += x
            self.min = NumericalAnalyser.int_to_sci(self.min)
            self.max = NumericalAnalyser.int_to_sci(self.max)
            self.mean = self.mean /length
            self.stdev = 0
            for x in values:
                self.stdev += pow(x-self.mean, 2)
            self.stdev = pow(self.stdev/length, 1/2)
            values.sort()
            median_index = (length + 1) / 2 - 1
            qlow_index = (length + 1) / 4 - 1
            qup_index = 3 * (length + 1) / 4 - 1
            if median_index % 1 == 0:
                self.median = values[int(median_index)]
            else:
                self.median = (values[floor(median_index)] + values[ceil(median_index)]) / 2
            if qlow_index % 1 == 0:
                self.quartile_low = values[int(qlow_index)]
                self.quartile_up = values[int(qup_index)]
            else:
                self.quartile_low = (values[floor(qlow_index)] + values[ceil(qlow_index)]) / 2
                self.quartile_up = (values[floor(qup_index)] + values[ceil(qup_index)]) / 2
            IQR = self.quartile_up - self.quartile_low
            outlier_count = 0
            for x, value in enumerate(values):
                if value < (self.quartile_low - 1.5 * IQR) or value > (self.quartile_up + 1.5 * IQR):
                    self.stDevOutliers.append("Row: %d Value: %s" % (x, value))
                    outlier_count += 1
            #if outlier_count > max_Outliers:
                #self.stDevOutliers = "%d outliers" % outlier_count
            self.mean = NumericalAnalyser.round_significant(self.mean)
            self.quartile_low = NumericalAnalyser.round_significant(self.quartile_low)
            self.quartile_up = NumericalAnalyser.round_significant(self.quartile_up)
            self.median = NumericalAnalyser.round_significant(self.median)
            self.stdev = NumericalAnalyser.round_significant(self.stdev)
            if self.mode != 'N/A':
                self.mode = NumericalAnalyser.int_to_sci(self.mode)

        else:
            print("WARNING Cannot convert to scientific notation")
            self.min = 'N/A'
            self.max = 'N/A'
            self.mean = 'N/A'
            self.quartile_low = 'N/A'
            self.median = 'N/A'
            self.quartile_up =  'N/A'
            self.stdev = 'N/A'
            self.normDist = 'N/A'
            self.stDevOutliers = 'N/A'

    @staticmethod
    def is_compatable(values):
        bad_values = 0
        for i in values:
            if i != '':
                try:
                    float(i)
                except:
                    bad_values += 1
        if bad_values / len(values) >= threshold:
            return False
        return True
        
class DateAnalyser(Analyser):
    """Run date analysis, currently only using Analyser super class methods.
    
    Keyword Arguments:
        Analyser -- An analyser object.
        

    """
    def __init__(self, values):
        super().__init__(values)

        DFcount = 0
        MMcount = 0
        JAcount = 0
        SNcount = 0

        for value in values:
            if re_date.search(value):
                if re_dateDF.search(value):
                    DFcount += 1
                if re_dateMM.search(value):
                    MMcount += 1
                if re_dateJA.search(value):
                    JAcount += 1
                if re_dateSN.search(value):
                    SNcount += 1
        self.dateDF = DFcount
        self.dateMM = MMcount
        self.dateJA = JAcount
        self.dateSN = SNcount

        
class TimeAnalyser(Analyser):
    """Run time analysis, currently only using Analyser super class methods.
    
    Keyword arguments:
        Analyser -- An analyser object.
    """
    def __init__(self, values):

        hourcount = []

        for x in range(0,24):
            hourcount.append([])
            hourcount[x].append(x)
            hourcount[x].append(0)
        
        super().__init__(values)
        for value in values:
            if re_time.search(value):
                temp=int(re_timehr.search(value).group(0))
                if re_timePM.search(value) and temp != 12:
                    temp += 12
                elif re_timeAM.search(value) and temp == 12:
                    temp = 0
                hourcount[temp][1]+= 1

        hoursort= sorted(hourcount,key=lambda l:l[1], reverse=True)
        self.hourCS = hoursort
        

class CharAnalyser(Analyser):
    """Run char analysis, currently only using Analyser super class methods.
    
    Keyword arguments:
        Analyser -- An analyser object.
    """
    def __init__(self, values):
        super().__init__(values)
        
class DayAnalyser(Analyser):
    """Run day analysis, currently only using Analyser super class methods.
    
    Keyword arguments:
        Analyser -- An analyser object.
    """
    def __init__(self, values):
        super().__init__(values)

class HyperAnalyser(Analyser):
    """Run hyperlink analysis, currently only using Analyser super class methods.
    
    Keyword arguments:
        Analyser -- An analyser object.
    """
    def __init__(self, values):
        super().__init__(values)
        # TODO Implement some hyperlink unique stats, e.g. domain frequency.

class DatetimeAnalyser(Analyser):
    """Run datetime analysis, currenytly only using Analyser super class methods.
    """
    def __init__(self, values):
        super().__init__(values)
        # TODO implement datetime unique stats

def normaltest(values):
    """Normality test of values based on Jarque-Bera Test"""
    """xbar = mean(values)
    n = len(values)
    s_top = sum([pow(x-xbar, 3) for x in values])/n
    std = sum([pow(x-xbar,2) for x in values])/n
    s_bot = pow(std, 3/2)
    S = s_top/s_bot
    c_top = sum([pow(x-xbar, 4) for x in values])/n
    c_bot = pow(std , 2)
    C = c_top/c_bot
    JB = (n /6) * (pow(S,2) + 0.25 * pow(C-3, 2))
    print("JB: ", JB)"""