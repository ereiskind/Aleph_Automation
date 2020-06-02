'''
Print-03: Output files
1. Services > Retrieve Catalog Records
2. Dialog box--Input File: saved search or list of BIBs or HOLs imported via above process
3. Dialog box--Library: set to UXU01 if input file is BIBs; set to UXU60 if input file is HOLs
4. Dialog box--Field # + Indicator
    "ALL" in the first field will download all fields in records
    For MARC fields, five digits required
    Wild card is "#"
    Null is "ZZ"
5. Dialog box--Format: Aleph Sequential or MARC with alphanumeric tags
    Alpeh Sequential generates a text file with a row for each field which starts with the BIB or HOL, indicates the MARC field tag, and contains the MARC subfield delimeters if subfield wasn't specified
    MARC with alphanumeric tags generates a MARC record file
6. Dialog box--Output file: name of output file
    No spaces or capital letters
    No special characters
    If Aleph Sequential, end ".txt"; if MARC, end ".mrc"
'''

# Default start for Aleph Sequential file is column lengths of 10, 6, 2 characters long