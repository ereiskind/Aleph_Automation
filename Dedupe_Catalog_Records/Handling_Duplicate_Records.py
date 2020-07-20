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
messagebox.showinfo(title="Instructions", message="Load Aleph Sequential file with UXU01 info into OpenRefine with column widths 10, 6, 2. Name the project \"UXU01_Cleanup\".")
messagebox.showwarning(title="Creating Title", message="The step to create the title column won't work unless there's a 245$a, 245$b, 245$n, and 250$a column. There's a column reorder in the JSON that calls for all four columns.")
messagebox.showwarning(title="Ebook Central", message="The following JSON is for Ebook Central--the domain search regexes are hard coded. On a related note, any URLs from those domains not fitting the regexes are excluded.")
messagebox.showwarning(title="Credo", message="Credo IDs that are only letters don't get transfered to the \"001 ID\" column.")
messagebox.showwarning(title="JSTOR", message="Pulling a DOI from a JSTOR URL seems to involve all rows in that record having \"DOI\" appear in the \"URL Domain\" column.")
os.startfile('Organize_UXU01_Output_pt1--Ebook_Central_Specific.json')
messagebox.showinfo(title="Instructions", message="Perform clustering on column \"URL Domain\" to change domain names into the platforms they represent. \"Change_Domain_Names_to_Platform_Names.json\" can help with this.")
messagebox.showwarning(title="Regex Only URLs", message="The only URLs pulled out for their IDs are the ones that match the regexes.")
messagebox.showinfo(title="Instructions", message="Use text facets to change the values in \"001 ID Source\" and \"Unofficial 001 ID Source\" into the names of the platforms/sources they represent. \"Change_001_Source_Abbreviations.json\" can help with this.")
messagebox.showwarning(title="YBP", message="\"YBP-long\" 001 IDs are identified as those at least 10 digits long and beginning with \"999\".")
messagebox.showwarning(title="Credo", message="Credo IDs that are letters followed by numbers have the letters in the \"Unofficial 001 ID\" column.")
os.startfile('Organize_UXU01_Output_pt2--Ebook_Central_Specific.json')
messagebox.showinfo(title="Instructions", message="Look at values with pipes in \"001 ID Source\" and determine which one to keep.")
os.startfile('Organize_UXU01_Output_pt3--Ebook_Central_Specific.json')
messagebox.showinfo(title="Instructions", message="Investigate ISBNs with lengths other than 10 or 13, then clean up \"ISBN Types\" via clustering.")
messagebox.showwarning(title="Duplicate Dedupe Column Blank Down", message="The process for blanking down then removing rows with duplicate ISBNs for the record is done twice because the first time doesn't catch all the duplicates; the reason for this is unknown.")
messagebox.showwarning(title="Ebook Central", message="Non-Ebook Central ID sources that didn't have duplicate IDs have their columns removed in this JSON.")
messagebox.showwarning(title="Ebook Central", message="The following JSON contains hard coded fill up and down then blank down instructions--in actuality, a loop knowing the names of the columns created needs to create that part of the JSON.")
#ToDo: figure out how to constructo loop for fill up and down then blank down hard coded into the pt4 JSON
messagebox.showwarning(title="Exact Match via Ebook Central Columns", message="The \"Exact Match via Ebook Central ID\" column was created because there weren't any BIBs with multiple Ebook Central IDs.")
#ToDo: Get list of columns that will need to be moved over to UXU60 OpenRefine project
os.startfile('Organize_UXU01_Output_pt4--Ebook_Central_Specific.json')
#Alert: This seems to not include BIBs that don't have FSU 856 fields--is this a problem?

#Subsection: Organize UXU60 Output
messagebox.showinfo(title="Instructions", message="Load Aleph Sequential file with UXU60 info into OpenRefine with column widths 10, 5, 3.")
os.startfile('Organize_HOL_for_Duplicate_BIB.json')
TKR_Loop(1,5)
messagebox.showwarning(title="Removing Non-FSU HOLs", message="Export results now for complete HOL info--next JSON will remove non-FSU HOLs.")
os.startfile('Finish_Organizing_HOLs.json')
# UXU01 records without matching HOL are records that have no FSU HOL
# UXU60 records without matching BIB are records where FSU BIB isn't for an Ebook Central record

#Subsection: Get List of FSU URLs
messagebox.showinfo(title="Instructions", message="Load Aleph Sequential file with UXU01 info into OpenRefine with column widths 10, 6, 2 as a project named \"URLs\".")
os.startfile('Extract_URLs.json')


#Section: Determine Which Records to Keep
#Subsection: Match Duplicate BIB Records
messagebox.showinfo(title="Instructions", message="This JSON continues using the UXU60 OpenRefine project.")
messagebox.showwarning(title="Cell Cross Project Columns", message="The JSON currently has ID columns for the Ebook Central BIB project hard-coded into it.")
#ToDo: Get list of columns to pull from UXU01 OpenRefine project and create loop to load them into this project with the last column being the first JSON object so all the object can use the same column insert index
os.startfile('Match_Duplicate_Records--Ebook_Central_Specific.json')
messagebox.showwarning(title="Ebook Central", message="Following instructions are very specific to Ebook Central.")
messagebox.showinfo(title="Instructions", message="Download the OpenRefine project into Excel. Dedupe \"INDX Ebook Central 1\" and copy into LibCentral's title match feature. Save the ISBN and ID columns from the title match output as \"ISBNs and eBook Central IDs.xlsx\".")
os.startfile('Match_Duplicate_Records_pt2--Ebook_Central_Specific.json')
messagebox.showinfo(title="Instructions", message="Create custom text filter with \"toString(startsWith(value,"*"))\" and set to true. For all titles in the matching records, manually determine the appropriate ID and change the value in \"INDX Ebook Central\" to that ID.")
#HOL 077392679 = Ebook Central ID 3052071
#HOL 077465248 = Ebook Central ID 3053278
#HOL 099570882 = Ebook Central ID 1121224
#HOL 103492998 = Ebook Central ID 4197994
#HOL 100419984 = Ebook Central ID 1698569

#Subsection: Determine Which HOL Records to Keep
messagebox.showinfo(title="Instructions", message="Save all BIBs that have an ACQ record attached in a spreadsheet named \"BIB with ACQ\" and upload to OpenRefine. Cell A1 should contain \"BIB Number\" and all the BIBs be nine-digit text strings.")
messagebox.showwarning(title="Ebook Central and TKRs", message="The second step in this JSON is for reordering columns--that makes it specific to Ebook Central in the column names and the number of TKR columns.")
messagebox.showwarning(title="FSU Sublibraries", message="The inverse of FSUER sublibraries lists out the excluded sublibraries.")
os.startfile('Select_HOL_to_Keep_pt1--Ebook_Central_Specific.json')
#ToDo: Make INDX forst column
#ToDo: Do checks on which row in each record to keep
#ToDo: Final format--Records by Ebook Central ID with BIB and HOL combinations


#Section: Create Update Files For Records to Remain
#Subsection: If New 856$u Needed, Supply It

#Subsection: If TKR Needed, Supply It


#Section: Remove Unneeded Records
#Subsection: If Other HOLs Attached to BIB, Delete FSUER HOL

#Subsection: If FSUER HOL is Only HOL, Delete HOL and BIB