# Process for creating TKRs for HOL attached to a list of BIB records

#Section: Get the HOLs
# Eventually, this will be replaced with the script Create_Uploadable_List.py
#Subsection: Create Text File
# # Get list of BIBs formatted as nine digits plus "UXU01"
# Save above to txt file named "fser" plus something ending with "b" no longer than 10 letters
# remove file extension

#Subsection: Upload BIBs
# Ask which server to go to
## https://susopac.falsc.org/cgi-bin/afv for production
## https://susopac.test.falsc.org/cgi-bin/afv for test
## https://susopac.rept.falsc.org/cgi-bin/afv for report
# Log in with Aleph credentials
# For uploader, choose file created above

#Subsection: Run Manage-70
# With the file name, run manage-70 bib to hol


#Section: Create TKR File
#Subsection: Get Data for TKRs
# run print-03 to get CAT## (?) LKR##, 852##

#Subsection: Manipulate Data in OpenRefine
#Upload data to OpenRefine
# Get TKR base
#for each HOL, isolate earliest cataloger date
# for each HOL, create line <BIB or HOL as 9 digits> TKR   L $$a<tickler>


#Section: Upload TKR File
'''
Manage-18: Add/Update Records
1. Create Alpeh Sequential .txt file
    Line format: <BIB or HOL as 9 digits> <MARC field and indicators--if indicators are null, use spaces> L $$<first subfield code><value of first subfield><repeat pattern of dollar signs, subfield code, and subfield value without spaces for all subfields>
2. Remove file extension
3. Go to https://susopac.falsc.org/cgi-bin/afv for production, https://susopac.test.falsc.org/cgi-bin/afv for test, https://susopac.rept.falsc.org/cgi-bin/afv for report and enter Aleph credentials
4. Select "uxu01/scratch" radio button for BIBs or "uxu60/scratch" radio button for HOLs
5. Upload file
6. Services > Load Catalog Records > Manage-18
7. Dialog box--Input file: name of file
8. Dialog box--Procedure to Run: indicate if adding records or updating existing records
9. Dialog box--If Updating Current Records: append
10. Dialog box--Cataloger Name: Alpeh login
11. Dialog box--Library: match to scratch directory file is in
'''