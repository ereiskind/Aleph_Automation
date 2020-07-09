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
messagebox.showinfo(title="Instructions", message="For list of HOLs, use print-03 to get Alpeh sequential file with TKR##, LKR##, STA##, 852## fields and indicators.")

#Subsection: Organize UXU01 Output
messagebox.showinfo(title="Instructions", message="Load Aleph Sequential file with UXU01 info into OpenRefine with column widths 10, 6, 2")
#ToDo: Create GUI element to capture name of this OpenRefine project and save it to variable UXU01OpenRefineProject
messagebox.showwarning(title="Ebook Central", message="The following JSON is for Ebook Central--the domain search regexes are hard coded")
messagebox.showwarning(title="Regex", message="The regex that should allow numbers that include dashes in them through doesn't.")
messagebox.showwarning(title="Credo", message="Credo IDs that are only letters don't get transfered to the \"001 ID\" column.")
messagebox.showwarning(title="JSTOR", message="Pulling a DOI from a JSTOR URL seems to involve all rows in that record having \"DOI\" appear in the \"URL Domain\" column.")
messagebox.showwarning(title="Titles Not Captured", message="If there's an issue with the 245$a field, the \"Title\" column will be left blank.")
os.startfile('Organize_UXU01_Output_pt1--Ebook_Central_Specific.json')
messagebox.showinfo(title="Instructions", message="Perform clustering on column \"URL Domain\" to change domain names into the platforms they represent.")
messagebox.showinfo(title="Instructions", message="Use text facets to change the values in \"001 ID Source\" and \"Unofficial 001 ID Source\" into the names of the platforms/sources they represent.")
messagebox.showwarning(title="YBP", message="Seperating the two different ID numbers provided by YBP is done by looking for those starting with \"999\" in the JSON--this should proobably be rethought.")
messagebox.showwarning(title="Record Number for Ebook Central IDs", message="All records with no Ebook Central IDs or DOIs were found to have the same value in \"Record Number\" later on--this problem should be isolated and removed.")
os.startfile('Organize_UXU01_Output_pt2--Ebook_Central_Specific.json')
messagebox.showinfo(title="Instructions", message="Filter by blanks on \"Temp\" to copy IDs from any unusually formatted URLs into \"URL ID.\"")
messagebox.showinfo(title="Instructions", message="Look at values with pipes in \"001 ID Source\" and determine which one to keep.")
os.startfile('Organize_UXU01_Output_pt3--Ebook_Central_Specific.json')
messagebox.showinfo(title="Instructions", message="Investigate ISBNs with lenghs other than 10 or 13, then clean up \"ISBN Types\" via clustering.")
messagebox.showinfo(title="Duplicate Dedupe Column Blank Down", message="The process for blanking down then removing rows with duplicate ISBNs for the record is done twice because the first time doesn't catch all the duplicates; the reason for this is unknown.")
messagebox.showwarning(title="Ebook Central", message="Non-Ebook Central ID sources that didn't have duplicate IDs have their columns removed in this JSON.")
messagebox.showwarning(title="Ebook Central", message="The following JSON contains hard coded fill up and down then blank down instructions--in actuality, a loop knowing the names of the columns created needs to create that part of the JSON.")
messagebox.showwarning(title="Exact Match via Ebook Central Columns", message="The \"Exact Match via Ebook Central ID\" column was created because there weren't any BIBs with multiple Ebook Central IDs.")
os.startfile('Organize_UXU01_Output_pt4--Ebook_Central_Specific.json')

#Subsection: Organixe UXU60 Output
messagebox.showinfo(title="Instructions", message="Load Aleph Sequential file with UXU60 info into OpenRefine with column widths 10, 5, 3")
os.startfile('Organize_HOL_for_Duplicate_BIB.json')
TKR_Loop(1,5)
messagebox.showwarning(title="Removing Non-FSU HOLs", message="Export results now for complete HOL info--next JSON will remove non-FSU HOLs.")
messagebox.showwarning(title="Cell Cross Project Name", message="The JSON currently has the OpenRefine project for Ebook Central's name hard-coded into it.")
messagebox.showwarning(title="Cell Cross Project Columns", message="The JSON currently has ID columns for the Ebook Central BIB project hard-coded into it.")
#ToDo: Create function that uses value stored in variable UXU01OpenRefineProject in cell cross functions in JSON below
os.startfile('Finish_Organizing_HOLs_and_Start_Matching_Records.json')
# UXU01 records without matching HOL are records that have no FSU HOL
# UXU60 records without matching BIB are cords where FSU BIB isn't for an Ebook Central record


#Section: Determine Which Records to Keep
#Subsection: Match Duplicate BIB Records
# Matching began in the final JSON of Organize UXU60 Output
"""
messagebox.showinfo(title="Instructions", message="Get 245 values for all BIBs and isolate the a subfields. Create sheet \"Composite\" with BIBs from 856 ID sheet and HOL sheet. Dedupe BIBs in column \"BIB Number\", then add columns \"BIB Values\", \"ACQ\", \"# of HOL\", \"Sublibrary\", \"Confirmed Duplicates\", \"Ebook Central ID\", \"Ebrary ID\", \"MyiLibrary ID\", \"DOI\", and \"Title\". Fill these columns with vlookups from the sheets with the corresponding info. For BIBs with multiple sublibraries, seperate the sublibraries with semicolons, not pipes; for suppressed HOLs, add \"\{Suppressed\}\" after the sublibrary code.")
#ToDo: Include formulas for how to do the above vlookups
"""

"""
messagebox.showinfo(title="Instructions", message="Upload sheet \"Composite\" to OpenRefine.")
os.startfile('Match_Duplicate_BIBs.json')
messagebox.showinfo(title="Instructions", message="Perform clustering on column\"Title\".")
os.startfile('Match_Duplicate_BIBs_pt2.json')
messagebox.showinfo(title="Instructions", message="At this point, check the BIB records for the openRefine records with three or more titles to determine if any can be condensed.")
"""

#Subsection: Determine Which BIB Records to Keep


#Section: Create Update Files For Records to Remain
#Subsection: If New 856$u Needed, Supply It
# Will need to get the UXU01 output and put it through OpenRefine again

#Subsection: If TKR Needed, Supply It


#Section: Remove Unneeded Records
#Subsection: If Other HOLs Attached to BIB, Delete FSUER HOL

#Subsection: If FSUER HOL is Only HOL, Delete HOL and BIB