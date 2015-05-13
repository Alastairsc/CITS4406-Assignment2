__author__ = 'Liam'

"""
def main():
    with open('dummy.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)

def main():
    with open('dummy.csv') as csvfile:
        reader = csv.DictReader(csvfile)

        number_of_columns = len(reader.fieldnames)

        for row in reader:
            print(row['column1'], row['column3'])

"""

import csv


def main():
    with open('dummy.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            for item in row[1]:
                print(item)


main()