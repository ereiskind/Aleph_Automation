# Process for handling having multiple records for a given owned title in UXU01 and possibly UXU60

import os
from tkinter import messagebox
import json


#Section: Functions
def TKR_Loop(ColumnNumber, ColumnPosition): #Both arguments should be initalized to one less than their first desired values
    """Generates the OpenRefine JSONs to move all a record's TKRs onto a single row.

    Creates a messagebox asking if there are more TKRs; if yes, creates sequentially named columns with sequential insert indexes for the top value in column "TKR$a", then removes that value from that column. The function repeats until the messagebox gets a "no" answer.
    """
    MoreTKRs = True
    while MoreTKRs == True:
        MoreTKRs = messagebox.askyesno(title="Instructions", message="Are there any more TKRs in the \"TKR$a\" column?")
        if MoreTKRs == False:
            ClearingFile = open('TKR_Loop_Iterations.json', 'w')
            ClearingFile.write("")
            ClearingFile.close
            break
        ColumnNumber += 1
        ColumnPosition +=1
        with open('TKR_Loop.json') as TemplateJSON:
            InstructionJSON = json.load(TemplateJSON)
        
        # Replace ColumnNumber
        InstructionJSON[0]['newColumnName'] = InstructionJSON[0]['newColumnName'].format(ColumnNumber)
        InstructionJSON[1]['expression'] = InstructionJSON[1]['expression'].format(ColumnNumber)
        InstructionJSON[2]['columnName'] = InstructionJSON[2]['columnName'].format(ColumnNumber)
        # Replace ColumnPosition
        InstructionJSON[0]['columnInsertIndex'] = ColumnPosition

        with open('TKR_Loop_Iterations.json', 'w') as CopyJSON:
            json.dump(InstructionJSON, CopyJSON, indent=4)
            CopyJSON.close
        os.startfile('TKR_Loop_Iterations.json')


#Section: Determine What BIBs Have ACQ Records
#Subsection: Collect all possible BIB numbers for the platform/collection in question

#Subsection: Send those BIBs to cataloging to have them check which ones have ACQ records attached


#Section: Collect BIB Information
#Subsection: Pull Info from Aleph
# For BIBs, print-03 Aleph sequential of 856 fields
# For BIBs, manage-70 for BIB-to-HOL
# For HOLs, print-03 Aleph sequential of TKR, LKR, STA

#Subsection: Organize UXU01 Output--Get IDs from URLs
messagebox.showinfo(title="Instructions", message="Load Aleph Sequential file into OpenRefine with column widths 10, 6, 2")
messagebox.showwarning(title="Ebook Central", message="The following JSON is for Ebook Central")
os.startfile('Get_Ebook_Central_URLs_from_856_Aleph_Sequential.json')
messagebox.showinfo(title="Instructions", message="Perform clustering on column \"URL Domain.\"")
os.startfile('Isolate_IDs_from_URLs.json')
messagebox.showinfo(title="Instructions", message="Copy IDs from any unusually formatted URLs in \"Temp\" into \"URL ID.\"")
messagebox.showwarning(title="Ebook Central", message="The following JSON is for Ebook Central--the fill up and andwn then blank down is hard coded")
os.startfile('Match_Duplicate_Records_by_856_Info.json')

#Subsection: Organize UXU01 Output--Get IDs from ISBNs
# Load list of BIBs which didn't have IDs from the 856 into Alpeh, run print-03 for 020 and 776
messagebox.showinfo(title="Instructions", message="Load Aleph Sequential file into OpenRefine with column widths 10, 6, 2")
os.startfile('Organize_ISBNs_from_Aleph_Sequential.json')
messagebox.showinfo(title="Instructions", message="Clean up \"ISBN Types\" via clustering.")
# ISBN pt. 2 JSON
messagebox.showinfo(title="Instructions", message="Organize numbering in \"ISBN Types\" via clustering; don't remove length numbers.")
#ToDo: create list of ISBN-13 that can be cross-referenced against a propriatary ID list--don't necessarily need to get broken out into columns if BIB fill down is last step, but deduping would be beneficial

#Subsection: Organixe UXU60 Output
messagebox.showinfo(title="Instructions", message="Load Aleph Sequential file into OpenRefine with column widths 10, 5, 3")
os.startfile('Organize_HOL_for_Duplicate_BIB.json')
TKR_Loop(1,5)
os.startfile('Finish_Organizing_HOLs.json')


#Section: Determine Which Records to Keep
# Using Excel vlookups and LibCentral, got Ebook Central, Ebrary, MyiLibrary IDs for as many BIBs as possible
# Combined BIBs from 856 and HOL outputs in Excel
#Subsection: Match Duplicate BIB Records
# New JSON for the IDs and matching up the duplications--cell cross with a list of Ebook Central/MyiLibrary/Ebrary numbers probably needed

#Subsection: Determine Which BIB Records to Keep


#Section: Create Update Files For Records to Remain
#Subsection: If New 856$u Needed, Supply It
# Will need to get the UXU01 output and put it through OpenRefine again

#Subsection: If TKR Needed, Supply It


#Section: Remove Unneeded Records
#Subsection: If Other HOLs Attached to BIB, Delete FSUER HOL

#Subsection: If FSUER HOL is Only HOL, Delete HOL and BIB