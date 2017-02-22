"""Analyser class for running analysis on columns depending on the column type"""


import re
from statistics import mean, mode, median_low, median, median_high, stdev, StatisticsError, Decimal
from scipy.stats import mstats
from numpy import array

from math import floor, log10, pow

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
            
            median_low -- Low median for column values.
            
            median -- Median value for column values.
            
            median_high -- High median for column values.
            
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
        values = [i for i in new_values]
        super().__init__(values)
        if isNumeric:
            self.stDevOutliers = []
            standardDeviations = Decimal(stdDevs)
            if len(values) >= 8:
                self.pval = mstats.normaltest(array(values))[1]
            else:
                self.pval = 100
            self.min = min(values)
            self.max = max(values)
            self.mean = Decimal(mean(values)).quantize(Decimal('.00000'))
            self.median_low = median_low(values)
            self.median = median(values)
            self.median_high = median_high(values)
            self.stdev = Decimal(stdev(values)).quantize(Decimal('.00'))
            self.normDist = 'No'
            if(self.pval > 0.055):
                self.normDist = 'Yes'
            elif self.pval == 100:
                self.normDist = 'N/A'
            if self.normDist == 'Yes':
                outlier_count = 0
                for x, value in enumerate(values):
                    if value < (self.mean - standardDeviations * self.stdev) or \
                    value > (self.mean + standardDeviations * self.stdev):  
                        if outlier_count > max_Outliers:
                            self.stDevOutliers = ">%d outliers" % max_Outliers
                            break
                        self.stDevOutliers.append("Row: %d Value: %s" % (x, value))
                        outlier_count += 1
        else:
            print("WARNING: Type error, cannot convert column to numerical value")
            self.min = 'N/A'
            self.max = 'N/A'
            self.mean = 'N/A'
            self.median_low = 'N/A'
            self.median = 'N/A'
            self.median_high =  'N/A'
            self.stdev = 'N/A'
            self.normDist = 'N/A'
            self.stDevOutliers = 'N/A'

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
        values = [i for i in new_values]
        super().__init__(values)
        if isNumeric:
            self.stDevOutliers = []
            if len(values) >= 8:
                self.pval = mstats.normaltest(array(values))[1]
            else:
                self.pval = 100
            if self.mode != 'N/A':
                self.mode = self.int_to_sci(self.mode)
            self.min = self.int_to_sci(min(values))
            self.max = self.int_to_sci(max(values))
            self.mean = self.int_to_sci(mean(values))
            self.median_low = self.int_to_sci(median_low(values))
            self.median = self.int_to_sci(median(values))
            self.median_high =  self.int_to_sci(median_high(values))
            self.stdev = self.int_to_sci(stdev(values))
            self.normDist = 'No'
            if(self.pval < 0.055):
                self.normDist = 'Yes'
            elif(self.pval == 100):
                self.normDist = 'N/A'
            if self.normDist == 'Yes':
                outlier_count = 0
                for x, value in enumerate(values):
                    if value < (float(self.mean) - standardDeviations * float(self.stdev)) or \
                    value > (float(self.mean) + standardDeviations * float(self.stdev)):               
                        if outlier_count > max_Outliers:
                            self.stDevOutliers = ">%d outliers" % max_Outliers
                            break
                        self.stDevOutliers.append("Row: %d Value: %s" % (x, value))
                        outlier_count += 1
        else:
            print("WARNING Cannot convert to scientific notation")
            self.min = 'N/A'
            self.max = 'N/A'
            self.mean = 'N/A'
            self.median_low = 'N/A'
            self.median = 'N/A'
            self.median_high =  'N/A'
            self.stdev = 'N/A'
            self.normDist = 'N/A'
            self.stDevOutliers = 'N/A'
            
    def int_to_sci(self, value):
        """Converts numbers into a string in scientific notation form
        
        Keyword arguments:
            value -- The value to be converted to scientific notation.
        """
        if value == 0:
            return "0E+0"
        power = floor(log10(abs(value)))
        base = round(value / pow(10, power), 4)
    
        if power > 0:
            return str(base) + "E+" + str(power)
        else:
            return str(base) + "E" + str(power)

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