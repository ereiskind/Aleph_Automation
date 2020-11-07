# Process for creating TKRs for HOL attached to a list of BIB records

from tkinter import messagebox
import os

#Section: Get the HOLs
# Eventually, this will be replaced with the script Create_Uploadable_List.py
#Subsection: Create Text File
messagebox.showinfo(title="Instructions", message="Copy the list of BIBs into an Excel spreadsheet, then use the formula \"=(TEXT([cell w/ SYS],\"000000000\") & \"UXU01\")\" to convert them to the proper format. Save the spreadsheet as a .txt file with a name starting \"fser\" containing no more than 10 characters with a \"b\" at or near the end. Remove the file extension from the newly created file.")

#Subsection: Upload BIBs
messagebox.showinfo(title="Instructions", message="Go to https://susopac.falsc.org/cgi-bin/afv for production, log in with Aleph credentials, and upload the newly created file to alephe/scratch.")
## https://susopac.falsc.org/cgi-bin/afv for production
## https://susopac.test.falsc.org/cgi-bin/afv for test
## https://susopac.rept.falsc.org/cgi-bin/afv for report

#Subsection: Run Manage-70
messagebox.showinfo(title="Instructions", message="Go to Services > General > Manage-70. Put the name of the newly created file in \"Input File\", the same name with a \"h\" in place of the \"b\" in \"Output File\", select \"BIB-TO-HOL\" for \"Convert Type\", and \"UXU01\" in both \"Convert Library\" and \"Library\".")


#Section: Create TKR File
#Subsection: Get Data for TKRs
messagebox.showinfo(title="Instructions", message="Go to Services > Retrieve Catalog Records > print-03. Put the name of the output file from manage-70 in \"Input File\", type a file name with no capital letters or spaces ending with a .txt file extension in \"Output File\", add \"CAT##\", \"852##\". in the first \"Field + Indicator\" boxes, confirm that \"Format\" is set to Aleph Sequential, and finally change \"Library\" to \"UXU60\". When Batch Log says the job is complete, download the file.")

#Subsection: Manipulate Data in OpenRefine
messagebox.showinfo(title="Instructions", message="Load file into OpenRefine with column widths 10, 5, 3.")
#ToDo: create pop-up that asks for the beginning part of the TKR, then insert that string into the JSON below
#Alert: OSO TKR is hard-coded into the JSON currently
#Alert: JSON works only for HOL with one or two CAT fields--https://github.com/sparkica/refine-stats may be the key to more
os.startfile('Create_TKR_File.json')
messagebox.showinfo(title="Instructions", message="Download the OpenRefine project, remove the first row, and save the spreadsheet as a .txt file.")


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