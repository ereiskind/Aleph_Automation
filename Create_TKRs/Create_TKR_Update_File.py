# Process for creating TKRs for HOL attached to a list of BIB records

from tkinter import messagebox

#Section: Get the HOLs
# Eventually, this will be replaced with the script Create_Uploadable_List.py
#Subsection: Create Text File
messagebox.showinfo(title="Instructions", message="Copy the list of BIBs into an Excel spreadsheet, then use the formula \"=(TEXT([cell w/ SYS],\"000000000\") & \"UXU01\")\" to convert them to the proper format. Save the spreadsheet as a .txt file with a name starting \"fser\" containing no more than 10 characters with a \"b\" at or near the end. Remove the file extension from the newly created file.")

#Subsection: Upload BIBs
messagebox.showinfo(title="Instructions", message="Go to https://susopac.falsc.org/cgi-bin/afv for production, long in with Aleph credentials, and upload the newly created file to ???.")
messagebox.showwarning(title="Problem with Upload", message="Unable to get upload accepted as valid file--further investigation needed.")
## https://susopac.falsc.org/cgi-bin/afv for production
## https://susopac.test.falsc.org/cgi-bin/afv for test
## https://susopac.rept.falsc.org/cgi-bin/afv for report

#Subsection: Run Manage-70
messagebox.showinfo(title="Instructions", message="Go to Services > General > Manage-70. Put the name of the newly created file in \"Input File\", the same name with a \"h\" in place of the \"b\" in \"Output File\", select \"BIB-TO-HOL\" for \"Convert Type\", and \"UXU01\" in both \"Convert Library\" and \"Library\".")


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