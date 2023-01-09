#!/usr/bin/python
import os
import sys
import argparse
import re
from datetime import datetime
import pandas as pd

# Read credit card statement file, parse through the file to find the needed fields.
# Return the list of parsed fields
def parseCreditFile(creditFile):
    CREDITPATTERN = r'^(\d{2}\/\d{2}) ([\w\d\s\#\'\./-]*|.*)\s+(Home Improvement|Restaurants|Merchandise|Gasoline|Services|Supermarkets|Travel\/Entertainment) \$(\d+\.\d{2})'
 
    print(creditFile)
    with open(creditFile, "r") as f:
        txt_file = f.read()

    matches = re.findall(CREDITPATTERN, txt_file, flags=re.MULTILINE)
    items = [ [m[0], m[1], m[2], '-%s' % m[3]] for m in matches]
    return items

def parseBankFile(bankFile):
    BANKPATTERN = r'^(\d{2}-\d{2}-\d{4})(.*)[\n ]+(-?\d+[,.]\d*[.]?\d*) (\d*[,.]\d*[.]?\d*)'

    print(bankFile)
    with open(bankFile, "r") as f:
        txt_file = f.read()

    matches = re.findall(BANKPATTERN, txt_file, flags=re.MULTILINE)
    items = [ [m[0], m[1], 'None', m[2]] for m in matches]
    return items


# Parse arguments, define argument options. '*' any number of args
parser = argparse.ArgumentParser()
parser.add_argument('--bank', '-b',  nargs='*', help="Document is a bank statement (TDECU).")
parser.add_argument('--credit', '-c', nargs='*', help="Docuemnt is a credit card statement(Discover).")

args = parser.parse_args()
print(args)
print("Args %s" % (args.credit))
parsedData = []

if args.credit:
    for file in args.credit:
        parsedData += parseCreditFile(file)
if args.bank:
    for file in args.bank:
        parsedData += parseBankFile(file)

if parsedData:
    print('Parsed Data:\n %s' % parsedData)
    # Create a DF for the expenses
    df = pd.DataFrame(data=parsedData)
    # Reset the index so we have an actual column for it
    df.reset_index(inplace=True)
    # Rename the columns
    df.columns=["ID", "Date", "Description", "Category", "Withdraw/Deposits"]
    # Increase all IDs so they start at 1
    df["ID"] += 1
    # Name of file to save data to
    dtString = datetime.now().strftime("%m-%d-%y-%H%M")
    # Export it as a CSV
    df.to_csv("ParsedStatements%s.csv" % dtString, index=False)
    print("Successfully parsed data. Savd data to file ParsedStatements%s.csv" % dtString)
else:
    print('Could not parse data.')
