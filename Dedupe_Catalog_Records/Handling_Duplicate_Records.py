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
messagebox.showinfo(title="Instructions", message="For list of BIBs, use print-03 to generate Alpeh sequential file with 856##, 035##, 599##, 020##, 776##, 245##, 250## fields and indicators.")
messagebox.showinfo(title="Instructions", message="For list of BIBs, use manage-70 to get list of HOLs.")
messagebox.showinfo(title="Instructions", message="For list of HOLs, use print-03 to get Alpeh sequential file with TKR##, LKR##, STA## fields and indicators.")

#Subsection: Organize UXU01 Output
messagebox.showinfo(title="Instructions", message="Load Aleph Sequential file with 856 fields into OpenRefine with column widths 10, 6, 2")

'''
#Subsection: Organize UXU01 Output--Get IDs from URLs
messagebox.showinfo(title="Instructions", message="Load Aleph Sequential file with 856 fields into OpenRefine with column widths 10, 6, 2")
messagebox.showwarning(title="Ebook Central", message="The following JSON is for Ebook Central")
os.startfile('Get_Ebook_Central_URLs_from_856_Aleph_Sequential.json')
messagebox.showinfo(title="Instructions", message="Perform clustering on column \"URL Domain.\"")
os.startfile('Isolate_IDs_from_URLs.json')
messagebox.showinfo(title="Instructions", message="Copy IDs from any unusually formatted URLs in \"Temp\" into \"URL ID.\"")
messagebox.showwarning(title="Ebook Central", message="The following JSON is for Ebook Central--the fill up and and then blank down is hard coded")
os.startfile('Match_Duplicate_Records_by_856_Info.json')

#Subsection: Organize UXU01 Output--Organize Propriatary IDs from 001 Fields
messagebox.showinfo(title="Instructions", message="Load Aleph Sequential file with fields 035 and 599 into OpenRefine with column widths 10, 5, 3")
messagebox.showwarning(title="Regex", message="The regex that should allow numbers that include dashes in them through doesn't.")
os.startfile('Get_IDs_from_035_and_599_Fields.json')
messagebox.showinfo(title="Instructions", message="Use text facets to change the ID source column values into the platforms and bib resources they represent.")
messagebox.showwarning(title="Ebook Central", message="The following JSON is for Ebook Central--the fill up and and then blank down is hard coded")
os.startfile('Get_IDs_from_035_and_599_Fields_pt2.json')

#Subsection: Organize UXU01 Output--Get IDs from ISBNs
# Load list of BIBs which didn't have IDs from the 856 into Alpeh, run print-03 for 020 and 776
messagebox.showinfo(title="Instructions", message="Load Aleph Sequential file into OpenRefine with column widths 10, 6, 2")
os.startfile('Organize_ISBNs_from_Aleph_Sequential.json')
messagebox.showinfo(title="Instructions", message="Investigate ISBNs with lenghs other than 10 or 13, then clean up \"ISBN Types\" via clustering.")
os.startfile('Dedupe_ISBNs_in_Single_Column.json')
#messagebox.showinfo(title="Instructions", message="Organize numbering in \"ISBN Types\" via clustering; don't remove length numbers.")
messagebox.showinfo(title="Instructions", message="Specific to Ebook Central: Run complete ISBN list in LibCentral title match feature, save result as \"Ebook Central ISBN and ID.xlsx\", and upload into OpenRefine.")
messagebox.showwarning(title="OpenRefine Cache Clearing", message="If there's already a project with that name in OpenRefine, the project will need to be deleted and OpenRefine restarted; without the restart, OpenRefine will continue to try and use the older project.")
os.startfile('Match_ISBNs_to_Ebook_Central_IDs.json')
messagebox.showinfo(title="Instructions", message="Confirm any values remaining in \"eISBN Match\" or \"ISBN Match\" aren't the best matches for the BIB record.")
os.startfile('Finish_Getting_IDs_from_ISBNs.json')

#Subsection: Organize UXU01 Output--Get Titles
messagebox.showinfo(title="Instructions", message="Load Aleph Sequential file with 245 and 250 fields into OpenRefine with column widths 10, 6, 2")
os.startfile('Get_Titles_from_245_and_250.json')
'''

#Subsection: Organixe UXU60 Output
messagebox.showinfo(title="Instructions", message="Load Aleph Sequential file into OpenRefine with column widths 10, 5, 3")
os.startfile('Organize_HOL_for_Duplicate_BIB.json')
TKR_Loop(1,5)
messagebox.showinfo(title="Instructions", message="Export results now for complete HOL info--next JSON will create connection between FSU sublibrary codes and BIBs")
messagebox.showwarning(title="TKR Removal", message="The JSON has removal for three extra TKR columns.")
#ToDo: Create loop to get the right number of TKR columns removals
os.startfile('Finish_Organizing_HOLs.json')


#Section: Determine Which Records to Keep
messagebox.showinfo(title="Instructions", message="Get 245 values for all BIBs and isolate the a subfields. Create sheet \"Composite\" with BIBs from 856 ID sheet and HOL sheet. Dedupe BIBs in column \"BIB Number\", then add columns \"BIB Values\", \"ACQ\", \"# of HOL\", \"Sublibrary\", \"Confirmed Duplicates\", \"Ebook Central ID\", \"Ebrary ID\", \"MyiLibrary ID\", \"DOI\", and \"Title\". Fill these columns with vlookups from the sheets with the corresponding info. For BIBs with multiple sublibraries, seperate the sublibraries with semicolons, not pipes; for suppressed HOLs, add \"\{Suppressed\}\" after the sublibrary code.")
#ToDo: Include formulas for how to do the above vlookups

#Subsection: Match Duplicate BIB Records
messagebox.showinfo(title="Instructions", message="Upload sheet \"Composite\" to OpenRefine.")
os.startfile('Match_Duplicate_BIBs.json')
messagebox.showinfo(title="Instructions", message="Perform clustering on column\"Title\".")
os.startfile('Match_Duplicate_BIBs_pt2.json')
messagebox.showinfo(title="Instructions", message="At this point, check the BIB records for the openRefine records with three or more titles to determine if any can be condensed.")

#Subsection: Determine Which BIB Records to Keep


#Section: Create Update Files For Records to Remain
#Subsection: If New 856$u Needed, Supply It
# Will need to get the UXU01 output and put it through OpenRefine again

#Subsection: If TKR Needed, Supply It


#Section: Remove Unneeded Records
#Subsection: If Other HOLs Attached to BIB, Delete FSUER HOL

#Subsection: If FSUER HOL is Only HOL, Delete HOL and BIB