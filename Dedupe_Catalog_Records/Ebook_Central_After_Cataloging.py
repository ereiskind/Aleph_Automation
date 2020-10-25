# Process specifically for handling Ebook Central after review by cataloging--begun on 10/5/2020
# Comment out code: Ctrl+k+c
# Remove commenting out: Ctrl+k+u

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
# WAU:KW in author= ProQuest AND WNS:KW in staff note= GOBI AND WSB:Sublibrary= FSUER {1106}
# WSB:Sublibrary= FSUER AND WUR:KW in URL= ebookcentral proquest com lib fsu AND WUR:KW in URL= FTaSU {5964}
# WSB:Sublibrary= FSUER AND WUR:KW in URL= myilibrary AND WUR:KW in URL= FTaSU {467}
# WSB:Sublibrary= FSUER AND WUR:KW in URL= ebrary AND WUR:KW in URL= FTaSU {693}
# WSB:Sublibrary= FSUER AND WUR:KW in URL= eblib AND WUR:KW in URL= FTaSU {486}
# All of the above: FSEREBCB5 {7310}


#Section: Collect BIB Information
#Subsection: Pull Info from Aleph
messagebox.showinfo(title="Instructions", message="For list of BIBs, use print-03 to generate Aleph sequential file with 856##, 035##, 599##, 020##, 776##, 245##, 250## fields and indicators.")
messagebox.showinfo(title="Instructions", message="For list of BIBs, use manage-70 to get list of HOLs.")
messagebox.showinfo(title="Instructions", message="For list of HOLs, use print-03 to get Aleph sequential file with TKR##, LKR##, STA##, 852## fields and indicators.")

#Subsection: Organize UXU01 Output
messagebox.showinfo(title="Instructions", message="Load Aleph Sequential file with UXU01 info into OpenRefine with column widths 10, 6, 2. Name the project \"UXU01_Cleanup\".")
messagebox.showwarning(title="Creating Title", message="The step to create the title column won't work unless there's a 245$a, 245$b, 245$n, and 250$a column. There's a column reorder in the JSON that calls for all four columns.")
messagebox.showwarning(title="Credo", message="Credo IDs that are only letters don't get transferred to the \"001 ID\" column.")
messagebox.showwarning(title="JSTOR", message="Pulling a DOI from a JSTOR URL seems to involve all rows in that record having \"DOI\" appear in the \"URL Domain\" column.")
os.startfile('Organize_UXU01_Output_pt1--Ebook_Central_Specific.json')
# The folowing is for a title where the volume info isn't in the BIB records
"""[
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "BIB Number",
          "expression": "grel:value==\"034636879\"",
          "columnName": "BIB Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": true,
                "l": "true"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Title",
    "expression": "value",
    "edits": [
      {
        "from": [
          "Handbook of autism and pervasive developmental disorders (ed=Fourth edition.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Handbook of autism and pervasive developmental disorders (ed=Fourth edition.)(vol=1)"
      }
    ],
    "description": "Mass edit cells in column Title"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "BIB Number",
          "expression": "grel:value==\"034026703\"",
          "columnName": "BIB Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": true,
                "l": "true"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Title",
    "expression": "value",
    "edits": [
      {
        "from": [
          "Handbook of autism and pervasive developmental disorders (ed=Fourth edition.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Handbook of autism and pervasive developmental disorders (ed=Fourth edition.)(vol=2)"
      }
    ],
    "description": "Mass edit cells in column Title"
  }
]"""

messagebox.showinfo(title="Instructions", message="Perform clustering on column \"URL Domain\" to change domain names into the platforms they represent.") # See Ebook_Central_Custom_Faceting_pt1.json
messagebox.showwarning(title="Regex Only URLs", message="The only URLs pulled out for their IDs are the ones that match the regexes.")
messagebox.showinfo(title="Instructions", message="Use text facets to change the values in \"001 ID Source\" and \"Unofficial 001 ID Source\" into the names of the platforms/sources they represent.") # See Ebook_Central_Custom_Faceting_pt1.json
messagebox.showwarning(title="Custom Faceting", message="All values in \"Unofficial 001 ID Source\" were handled in that JSON.")
messagebox.showwarning(title="Custom Faceting: YBP", message="YBP IDs or unlabeled 035 values that are 11 digits long have been relabeled \"Gobi\".")
os.startfile('Organize_UXU01_Output_pt2--Ebook_Central_Specific.json')

messagebox.showwarning(title="MyiLibrary", message="The following JSON Specifically contains a step for seperating the MyiLibrary ID source identifiers for the IDs from URLs and 035/599 fields.")
os.startfile('Organize_UXU01_Output_pt3--Ebook_Central_Specific.json')
messagebox.showinfo(title="Instructions", message="Investigate ISBNs with lengths other than 10 or 13, then clean up \"ISBN Types\" via clustering.") # See Ebook_Central_Custom_Faceting_pt2.json

messagebox.showwarning(title="Duplicate Dedupe Column Blank Down", message="The process for blanking down then removing rows with duplicate ISBNs for the record is done twice because the first time doesn't catch all the duplicates; the reason for this is unknown.")
messagebox.showwarning(title="Ebook Central", message="Non-Ebook Central ID sources that didn't have duplicate IDs have their columns removed in this JSON.")
os.startfile('Organize_UXU01_Output_pt4--Ebook_Central_Specific.json')
#Alert: This seems to not include BIBs that don't have FSU 856 fields--is this a problem?
messagebox.showinfo(title="Instructions", message="Perform clustering on \"Temp Title 2\".") # See Ebook_Central_Custom_Faceting_pt3.json
messagebox.showinfo(title="Instructions", message="Perform clustering on \"Temp Title 3\".") # See Ebook_Central_Custom_Faceting_pt3.json

os.startfile('Organize_UXU01_Output_pt5--Ebook_Central_Specific.json')
messagebox.showinfo(title="Instructions", message="Create a filter for blanks on \"Inexact Title Record Number\" and set it to true. If the titles in the record don't match, change the values in \"Inexact Title Record Number\" with \"toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)\".") # Few enough titles remained after the filter that they could be examined together, and none were matches.

os.startfile('Organize_UXU01_Output_pt6--Ebook_Central_Specific.json')
messagebox.showinfo(title="Instructions", message="Create a filter for blanks on \"No Subtitle Record Number\" and set it to true. If the titles in the record don't match, change the values in \"No Subtitle Record Number\" with \"toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)\".") # Single JSON step--see below
"""[
      {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "No Subtitle Record Number",
          "expression": "isBlank(value)",
          "columnName": "No Subtitle Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": true,
                "l": "true"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        },
        {
          "type": "list",
          "name": "BIB Number",
          "expression": "value",
          "columnName": "BIB Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "035861419",
                "l": "035861419"
              }
            },
            {
              "v": {
                "v": "020661587",
                "l": "020661587"
              }
            },
            {
              "v": {
                "v": "034153576",
                "l": "034153576"
              }
            },
            {
              "v": {
                "v": "033330708",
                "l": "033330708"
              }
            },
            {
              "v": {
                "v": "028765055",
                "l": "028765055"
              }
            },
            {
              "v": {
                "v": "036768093",
                "l": "036768093"
              }
            },
            {
              "v": {
                "v": "022512571",
                "l": "022512571"
              }
            },
            {
              "v": {
                "v": "020691205",
                "l": "020691205"
              }
            },
            {
              "v": {
                "v": "022512751",
                "l": "022512751"
              }
            },
            {
              "v": {
                "v": "020692062",
                "l": "020692062"
              }
            },
            {
              "v": {
                "v": "036695441",
                "l": "036695441"
              }
            },
            {
              "v": {
                "v": "021179888",
                "l": "021179888"
              }
            },
            {
              "v": {
                "v": "030972673",
                "l": "030972673"
              }
            },
            {
              "v": {
                "v": "037551959",
                "l": "037551959"
              }
            },
            {
              "v": {
                "v": "032257080",
                "l": "032257080"
              }
            },
            {
              "v": {
                "v": "021111529",
                "l": "021111529"
              }
            },
            {
              "v": {
                "v": "035918051",
                "l": "035918051"
              }
            },
            {
              "v": {
                "v": "022492949",
                "l": "022492949"
              }
            },
            {
              "v": {
                "v": "020480642",
                "l": "020480642"
              }
            },
            {
              "v": {
                "v": "034195179",
                "l": "034195179"
              }
            },
            {
              "v": {
                "v": "036695222",
                "l": "036695222"
              }
            },
            {
              "v": {
                "v": "020168608",
                "l": "020168608"
              }
            },
            {
              "v": {
                "v": "028533388",
                "l": "028533388"
              }
            },
            {
              "v": {
                "v": "028730023",
                "l": "028730023"
              }
            }                                
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "No Subtitle Record Number",
    "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column No Subtitle Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
  }
]"""

os.startfile('Organize_UXU01_Output_pt7--Ebook_Central_Specific.json')
messagebox.showinfo(title="Instructions", message="In record view, create a filter for blanks on \"Record Number 1\" and set it to false. Create a text filter on \"Record Number 2\". Select each number in the \"Record Number 2\" text filter on at a time. Determine which BIBs have a given proprietary ID, change the value of \"Record Number\" to that ID by filtering on \"BIB Number\", then remove the BIB filter and null \"Ebook Central\" and then null \"Record Number 2\".") # See Ebook_Central_Custom_Faceting_pt4.json

os.startfile('Organize_UXU01_Output_pt8--Ebook_Central_Specific.json')
# messagebox.showinfo(title="Instructions", message="Create text filter on \"ISBN Values 1\" and select each string of IDs individually. Determine which Ebook Central ID is the best match for that BIB, then change \"Record Number\" to \"Ebook Central::\" plus that ID.") -- The only value in "ISBN Values 1" was "No ID found"

os.startfile('Organize_UXU01_Output_pt9--Ebook_Central_Specific.json')
messagebox.showinfo(title="Instructions", message="Create custom filter on \"Record Number\" with the expression \"and(contains(value,\"|\"),contains(value,\"::\"))\". For the BIBs that are true, determine which Ebook Central ID to keep.") # Just two JSON steps--see below
"""[
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "BIB Number",
          "expression": "value",
          "columnName": "BIB Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "034026703",
                "l": "034026703"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Record Number",
    "expression": "grel:\"Ebook Central::4033723\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::4033723\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "BIB Number",
          "expression": "value",
          "columnName": "BIB Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "034636879",
                "l": "034636879"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Record Number",
    "expression": "grel:\"Ebook Central::4033722\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::4033722\""
  }
]"""

#Subsection: Organize UXU60 Output
messagebox.showinfo(title="Instructions", message="Load Aleph Sequential file with UXU60 info into OpenRefine with column widths 10, 5, 3. Name the project \"UXU60_Cleanup\".")
os.startfile('Organize_HOL_for_Duplicate_BIB.json')
TKR_Loop(1,5)
messagebox.showwarning(title="Removing Non-FSU HOLs", message="Export results now for complete HOL info--next JSON will remove non-FSU HOLs.")
os.startfile('Finish_Organizing_HOLs.json')
# UXU01 records without matching HOL are records that have no FSU HOL
# UXU60 records without matching BIB are records where FSU BIB isn't for an Ebook Central record

#Subsection: Get List of FSU URLs
messagebox.showinfo(title="Instructions", message="Load Aleph Sequential file with UXU01 info into OpenRefine with column widths 10, 6, 2 as a project named \"URLs\".")
messagebox.showwarning(title="Identifying SciTech URLs", message="The Ebook Central specific JSON has steps to identify the URLs with 856$3 indicating that the records are for SciTech titles.")
os.startfile('Extract_URLs--Ebook_Central_Specific.json')


#Section: Determine Which Records to Keep
#Subsection: Match Duplicate BIB Records
messagebox.showinfo(title="Instructions", message="This JSON continues using the UXU60 OpenRefine project.")
messagebox.showwarning(title="Cell Cross Project Columns", message="The JSON currently has ID columns for the Ebook Central BIB project hard-coded into it.")
messagebox.showwarning(title="Fill Down", message="The JSON fills down all the columns, so it needs to know what columns it has.")
messagebox.showwarning(title="Fill Up and Down Ticklers", message="The JSON fills up and down then blanks down the TKR columns as well, so in addition to needing to know how many to do, a loop needs to be created.")
os.startfile('Match_Duplicate_Records--Ebook_Central_Specific.json')
# messagebox.showinfo(title="Instructions", message="Set text filter on \"Ebook Central IDs\" to false and create a text filter for \"HOL Number\". For all records that match, select the HOL numbers, change the view to rows, clear the filter on \"Ebook Central IDs\", and change the value of \"Record Number\" to match the URL with \"\"Ebook Central::\"+match(cells[\"Ebook Central BIB URLs\"].value,/https:\\/\\/ebookcentral\\.proquest\\.com\\/lib\\/fsu\\/detail\\.action\\?docID=(\\d*)/)[0])\". Confirm that the record in question doesn't have replacement characters in any of the titles or that all of the titles have TKRs for other platforms; if they do, make the appropriate changes or removals now.") -- No titles had ID mismatched between the UXU01 OpenRefine project and the FSU URL
# messagebox.showinfo(title="Instructions", message="Set text filter on \"Replacement Character in Title\" to true and edit the titles as needed to match the 245 fields in the BIBs of origin.") -- No replacement characters in any titles
# messagebox.showinfo(title="Instructions", message="Set filter for blanks on \"Record Number\" to true and create text filter on \"TKRs\" and \"Record Number\". For each value in the text filter on \"TKRs\", use filtering by \"Record Number\" to remove the records were all the rows have a tickler for another platform.") -- No records met this criteria

#Subsection: Determine Which HOL Records to Keep
messagebox.showinfo(title="Instructions", message="Create spreadsheet \"Cross-Reference.xlsx\" with columns \"BIB Checked for ACQ\", listing all the BIBs cataloging checked for an attached ACQ record formatted as text, and \"BIB has ACQ\", containing a boolean indicating if the adjacent BIB is attached to a FSU ACQ record. Load into OpenRefine as \"Cross-Reference\".")
messagebox.showwarning(title="3+ HOL Sublibrary/BIB Mismatch Not Handled", message="The JSON doesn't handle the situation where the comparison of the BIB and sublibraries of the first and second row in a record to the subsequent rows leads to different results to those later rows.")
os.startfile('Select_HOL_to_Keep_pt1--EC_After_Cataloging.json')
# "Record Number" formats
    # Ebook Central::<Ebook Central ID> = title matched to an Ebook Central ID
    # HOL <HOL Number> without ID = HOL is only one for that title
    # Duplicate <sublibrary code> Sublibrary for BIB <BIB number> = multiple HOLs for same sublibrary on same BIB record found (theoretically, shouldn't be possible) {Same BIB, Same Sublibrary}
    # BIBs <list of BIB numbers> Match = HOLs for the same sublibrary found on multiple BIB records {Different BIB, Same Sublibrary}
    # Different Sublibraries for BIB <BIB Number> = HOLs found on same BIB record but for different sublibraries {Same BIB, Different Sublibrary}
    # BIBs <list of BIB numbers> Match with Different Sublibraries = HOLs for different sublibraries found on different BIB records {Different BIB, Different Sublibrary}
messagebox.showinfo(title="Instructions", message="Remove the blanks filter on \"Duplication\". Create text filter on \"HOL Sublibrary\" and select all values but \"FSUER\", then invert. Use \"Transform...\" to change the value of the matching records to \"Only FSUER HOL\".") # Single JSON step--see below
"""[
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "HOL Sublibrary",
          "expression": "value",
          "columnName": "HOL Sublibrary",
          "invert": true,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "FSUPC",
                "l": "FSUPC"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "FSUER HOL",
    "expression": "grel:\"Only FSUER HOL\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column FSUER HOL using expression grel:\"Only FSUER HOL\""
  }
]"""

os.startfile('Select_HOL_to_Keep_pt2--EC_After_Cataloging.json')
messagebox.showinfo(title="Instructions", message="Create text filter on \"ACQ Test\" and switch to row mode. Filter for \"BIB Not Checked for ACQ\", and check those BIBs to see if an ACQ is attached, and change to value of \"ACQ Test\" accordingly.") # See Ebook_Central_Custom_Faceting_pt5.json

os.startfile('Select_HOL_to_Keep_pt3--EC_After_Cataloging.json')
# "Keep HOL?" Formats
    # HOLs being kept
        # Only HOL for record = TRUE: Only HOL for ID <Ebook Central ID> | TRUE: Only HOL for Title [HOL <HOL number>]
        # FSUER HOL with ACQ = TRUE: FSUER HOL with ACQ for <Ebook Central ID | "Title">
        # FSUER HOL without ACQ = TRUE: FSUER HOL for <Ebook Central ID | "Title">
        # FSUER HOL in record with other HOL/BIBs believed to have been loaded for URL = TRUE: Other FSUER HOL for <Ebook Central ID | "Title"> Probably Loaded for URL
    # HOLs to remove
        # FSUER HOL with ACQ for non-Ebook Central BIB = N/A: Non-Ebook Central Holding with ACQ for <Ebook Central ID | "Title">
        # FSUER HOL without ACQ for non-Ebook Central BIB = N/A: Non-Ebook Central Holding for <Ebook Central ID | "Title">
        # FSUER HOL without ACQ = FALSE: FSUER HOL without ACQ for <Ebook Central ID | "Title">
        # FSUER HOL believed to have been loaded for URL = FALSE: Probably Loaded for URL for <Ebook Central ID | "Title">
        # Other sublibrary HOL on same BIB = N/A: Other Sublibrary HOL on FSUER BIB for <Ebook Central ID | "Title">
        # FSUER HOL with ACQ = FALSE: FSUER HOL with ACQ for <Ebook Central ID | "Title">
messagebox.showinfo(title="Instructions", message="Create blanks filter on \"Keep HOL?\" and set to true. For the records that remain, adjust the values of \"Keep HOL?\" using the above formats as appropriate.") # See Ebook_Central_Custom_Faceting_pt6.json


#Section: Create Update Files For Records to Remain
#Subsection: Identify Perpetual Access Entitlements
os.startfile('Identify_Perpetual_Access_Entitlements_pt1--Ebook_Central_Specific.json')
messagebox.showinfo(title="Instructions", message="Export a list of the Ebook Central perpetual access entitlements from LibCentral and combine it with a list of the non-FSU-owned perpetual access entitlements created via title match. Save as a CSV named \"Entitlements\" and upload to OpenRefine.")
messagebox.showinfo(title="Instructions", message="Apply the following JSON in the \"Entitlements csv\" project.")
os.startfile('Identify_Perpetual_Access_Entitlements_pt2--Ebook_Central_Specific.json')

# #Subsection: Determine Records that Need to be Unsuppressed
# messagebox.showinfo(title="Instructions", message="Switch back to the \"UXU60_Cleanup\" project.")
# messagebox.showwarning(title="Non-Perpetual Access Titles with Multiple HOL", message="Steps to remove records with blank \"Record Number Copy\" values which have multiple rows because of multiple HOL attached to the same BIB not included as no such records existed in the data.")
# os.startfile('Determine_HOL_to_Unsuppress_pt1--Ebook_Central_Specific.json')
# messagebox.showinfo(title="Instructions", message="Set custom text filter \"isNumeric(value)\" on \"Record Number Copy\" to false. Remove single-HOL records with TKRs for other platforms.")
# """[
#   {
#     "op": "core/row-removal",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number Copy",
#           "expression": "grel:isNumeric(value)",
#           "columnName": "Record Number Copy",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": false,
#                 "l": "false"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "Ebook Central BIB URLs",
#           "expression": "isBlank(value)",
#           "columnName": "Ebook Central BIB URLs",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": true,
#                 "l": "true"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "Record Number",
#           "expression": "grel:row.record.toRowIndex-row.record.fromRowIndex>1",
#           "columnName": "Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": false,
#                 "l": "false"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "TKR 2",
#           "expression": "isBlank(value)",
#           "columnName": "TKR 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": true,
#                 "l": "true"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "FSU Tickler",
#           "expression": "value",
#           "columnName": "FSU Tickler",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "(FTaSU)FS-Oxford Reference Premium20151023",
#                 "l": "(FTaSU)FS-Oxford Reference Premium20151023"
#               }
#             },
#             {
#               "v": {
#                 "v": "(FTaSU)FS-Oxford Quick Reference20150108",
#                 "l": "(FTaSU)FS-Oxford Quick Reference20150108"
#               }
#             },
#             {
#               "v": {
#                 "v": "(FTaSU)FS-Oxford Quick Reference20140325",
#                 "l": "(FTaSU)FS-Oxford Quick Reference20140325"
#               }
#             },
#             {
#               "v": {
#                 "v": "(FTaSU)FS-Oxford Quick Reference20131021",
#                 "l": "(FTaSU)FS-Oxford Quick Reference20131021"
#               }
#             },
#             {
#               "v": {
#                 "v": "(FTaSU)FS-SageResearchMethods20150216",
#                 "l": "(FTaSU)FS-SageResearchMethods20150216"
#               }
#             },
#             {
#               "v": {
#                 "v": "(FTaSU)SpringerPalgrave20170314",
#                 "l": "(FTaSU)SpringerPalgrave20170314"
#               }
#             },
#             {
#               "v": {
#                 "v": "(FTaSU)CredoReference20161212",
#                 "l": "(FTaSU)CredoReference20161212"
#               }
#             },
#             {
#               "v": {
#                 "v": "(FTaSU)FS-GVRL20150413",
#                 "l": "(FTaSU)FS-GVRL20150413"
#               }
#             },
#             {
#               "v": {
#                 "v": "(FTaSU)DramaOnline20170104",
#                 "l": "(FTaSU)DramaOnline20170104"
#               }
#             },
#             {
#               "v": {
#                 "v": "(FTaSU)EBSCO20160923",
#                 "l": "(FTaSU)EBSCO20160923"
#               }
#             },
#             {
#               "v": {
#                 "v": "(FTaSU)EBSCO20160922",
#                 "l": "(FTaSU)EBSCO20160922"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "description": "Remove rows"
#   }
# ]"""
# messagebox.showinfo(title="Instructions", message="Compare the titles with no value in \"Match\" in \"Entitlement csv\" and the titles with no value in \"Record Number Copy\" in \"UXU60_cleanup\" to see what manual matches can be found that way. For matches found that way, change the value of \"Record Number Copy\" to the Ebook Central ID as a number.")
# #Alert: Other matches to perpetual access entitlement Ebook Central IDs are being added here as well
# """[
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 103466744 without ID\",toNumber(4397417),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 103466744 without ID\",toNumber(4397417),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 102925045 without ID\",toNumber(4000882),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 102925045 without ID\",toNumber(4000882),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 102834448 without ID\",toNumber(3421587),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 102834448 without ID\",toNumber(3421587),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 103222852 without ID\",toNumber(4054135),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 103222852 without ID\",toNumber(4054135),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 103487017 without ID\",toNumber(4083293),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 103487017 without ID\",toNumber(4083293),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 103164015 without ID\",toNumber(4091394),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 103164015 without ID\",toNumber(4091394),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 104159088 without ID\",toNumber(4504330),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 104159088 without ID\",toNumber(4504330),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 104159089 without ID\",toNumber(4007440),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 104159089 without ID\",toNumber(4007440),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 103222894 without ID\",toNumber(4007484),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 103222894 without ID\",toNumber(4007484),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 104159068 without ID\",toNumber(4054857),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 104159068 without ID\",toNumber(4054857),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 102991852 without ID\",toNumber(3421506),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 102991852 without ID\",toNumber(3421506),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 103189528 without ID\",toNumber(4218258),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 103189528 without ID\",toNumber(4218258),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 104171499 without ID\",toNumber(4332395),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 104171499 without ID\",toNumber(4332395),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 102983628 without ID\",toNumber(4000626),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 102983628 without ID\",toNumber(4000626),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 103164020 without ID\",toNumber(4179718),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 103164020 without ID\",toNumber(4179718),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 103486992 without ID\",toNumber(4082151),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 103486992 without ID\",toNumber(4082151),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 104917681 without ID\",toNumber(4003800),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 104917681 without ID\",toNumber(4003800),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 104174471 without ID\",toNumber(4533281),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 104174471 without ID\",toNumber(4533281),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 103483773 without ID\",toNumber(4009369),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 103483773 without ID\",toNumber(4009369),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 104212041 without ID\",toNumber(3421492),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 104212041 without ID\",toNumber(3421492),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 104174473 without ID\",toNumber(4340019),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 104174473 without ID\",toNumber(4340019),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 103222842 without ID\",toNumber(3301299),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 103222842 without ID\",toNumber(3301299),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 103184452 without ID\",toNumber(3138607),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 103184452 without ID\",toNumber(3138607),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 104159111 without ID\",toNumber(4007475),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 104159111 without ID\",toNumber(4007475),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 103486999 without ID\",toNumber(4008976),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 103486999 without ID\",toNumber(4008976),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 103487000 without ID\",toNumber(4186126),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 103487000 without ID\",toNumber(4186126),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 104159112 without ID\",toNumber(4107602),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 104159112 without ID\",toNumber(4107602),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 103483794 without ID\",toNumber(4218953),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 103483794 without ID\",toNumber(4218953),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 105491819 without ID\",toNumber(3408980),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 105491819 without ID\",toNumber(3408980),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 103164022 without ID\",toNumber(4082316),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 103164022 without ID\",toNumber(4082316),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 102991860 without ID\",toNumber(4093129),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 102991860 without ID\",toNumber(4093129),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 103014616 without ID\",toNumber(3305799),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 103014616 without ID\",toNumber(3305799),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 103014618 without ID\",toNumber(3305813),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 103014618 without ID\",toNumber(3305813),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 102758832 without ID\",toNumber(3569837),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 102758832 without ID\",toNumber(3569837),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 103014620 without ID\",toNumber(3294736),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 103014620 without ID\",toNumber(3294736),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 103419322 without ID\",toNumber(3290371),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 103419322 without ID\",toNumber(3290371),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 103228944 without ID\",toNumber(4386857),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 103228944 without ID\",toNumber(4386857),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 104159130 without ID\",toNumber(4306187),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 104159130 without ID\",toNumber(4306187),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 103014633 without ID\",toNumber(4000355),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 103014633 without ID\",toNumber(4000355),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 103536290 without ID\",toNumber(3399583),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 103536290 without ID\",toNumber(3399583),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 105461651 without ID\",toNumber(3297902),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 105461651 without ID\",toNumber(3297902),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 104605241 without ID\",toNumber(3316164),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 104605241 without ID\",toNumber(3316164),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 104168814 without ID\",toNumber(4217757),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 104168814 without ID\",toNumber(4217757),value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#        "facets": [],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:if(value==\"HOL 077685056 without ID\",toNumber(4656802),value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:if(value==\"HOL 077685056 without ID\",toNumber(4656802),value)"
#   }
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number Copy",
#           "expression": "grel:isNumeric(value)",
#           "columnName": "Record Number Copy",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": false,
#                 "l": "false"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "Record Number",
#           "expression": "value",
#           "columnName": "Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "Ebook Central::1666575",
#                 "l": "Ebook Central::1666575"
#               }
#             },
#             {
#               "v": {
#                 "v": "Ebook Central::4441715",
#                 "l": "Ebook Central::4441715"
#               }
#             },
#             {
#               "v": {
#                 "v": "Ebook Central::4938606",
#                 "l": "Ebook Central::4938606"
#               }
#             },
#             {
#               "v": {
#                 "v": "Ebook Central::1768917",
#                 "l": "Ebook Central::1768917"
#               }
#             },
#             {
#               "v": {
#                 "v": "Ebook Central::4731363",
#                 "l": "Ebook Central::4731363"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number Copy",
#     "expression": "grel:toNumber(substring(value,indexOf(value,\"::\")+2))",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number Copy using expression grel:toNumber(substring(value,indexOf(value,\"::\")+2))"
#   }
# ]"""
# messagebox.showinfo(title="Instructions", message="Use the URLs in \"Ebook Central BIB URLs\" to remove titles we no longer have access to from the project.")
# """[
#   {
#     "op": "core/row-removal",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number Copy",
#           "expression": "grel:isNumeric(value)",
#           "columnName": "Record Number Copy",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": false,
#                 "l": "false"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "Record Number",
#           "expression": "value",
#           "columnName": "Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "Ebook Central::864877",
#                 "l": "Ebook Central::864877"
#               }
#             },
#             {
#               "v": {
#                 "v": "Ebook Central::5568659",
#                 "l": "Ebook Central::5568659"
#               }
#             },
#             {
#               "v": {
#                 "v": "Ebook Central::3061842",
#                 "l": "Ebook Central::3061842"
#               }
#             },
#             {
#               "v": {
#                 "v": "Ebook Central::908989",
#                 "l": "Ebook Central::908989"
#               }
#             },
#             {
#               "v": {
#                 "v": "Ebook Central::203818",
#                 "l": "Ebook Central::203818"
#               }
#             },
#             {
#               "v": {
#                 "v": "Ebook Central::4813409",
#                 "l": "Ebook Central::4813409"
#               }
#             },
#             {
#               "v": {
#                 "v": "Ebook Central::4353619",
#                 "l": "Ebook Central::4353619"
#               }
#             },
#             {
#               "v": {
#                 "v": "Ebook Central::3377935",
#                 "l": "Ebook Central::3377935"
#               }
#             },
#             {
#               "v": {
#                 "v": "Ebook Central::144666",
#                 "l": "Ebook Central::144666"
#               }
#             },
#             {
#               "v": {
#                 "v": "Ebook Central::4866498",
#                 "l": "Ebook Central::4866498"
#               }
#             },
#             {
#               "v": {
#                 "v": "Ebook Central::5208444",
#                 "l": "Ebook Central::5208444"
#               }
#             },
#             {
#               "v": {
#                 "v": "Ebook Central::1638619",
#                 "l": "Ebook Central::1638619"
#               }
#             },
#             {
#               "v": {
#                 "v": "Ebook Central::990471",
#                 "l": "Ebook Central::990471"
#               }
#             },
#             {
#               "v": {
#                 "v": "Ebook Central::143915",
#                 "l": "Ebook Central::143915"
#               }
#             },
#             {
#               "v": {
#                 "v": "Ebook Central::1121224",
#                 "l": "Ebook Central::1121224"
#               }
#             },
#             {
#               "v": {
#                 "v": "Ebook Central::3571668",
#                 "l": "Ebook Central::3571668"
#               }
#             },
#             {
#               "v": {
#                 "v": "Ebook Central::817847",
#                 "l": "Ebook Central::817847"
#               }
#             },
#             {
#               "v": {
#                 "v": "Ebook Central::157018",
#                 "l": "Ebook Central::157018"
#               }
#             },
#             {
#               "v": {
#                 "v": "Ebook Central::1935748",
#                 "l": "Ebook Central::1935748"
#               }
#             },
#             {
#               "v": {
#                 "v": "Ebook Central::4557224",
#                 "l": "Ebook Central::4557224"
#               }
#             },
#             {
#               "v": {
#                 "v": "Ebook Central::4415653",
#                 "l": "Ebook Central::4415653"
#               }
#             },
#             {
#               "v": {
#                 "v": "Ebook Central::294757",
#                 "l": "Ebook Central::294757"
#               }
#             },
#             {
#               "v": {
#                 "v": "Ebook Central::203669",
#                 "l": "Ebook Central::203669"
#               }
#             },
#             {
#               "v": {
#                 "v": "Ebook Central::253684",
#                 "l": "Ebook Central::253684"
#               }
#             },
#             {
#               "v": {
#                 "v": "Ebook Central::6147813",
#                 "l": "Ebook Central::6147813"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "description": "Remove rows"
#   },
#   {
#     "op": "core/row-removal",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number Copy",
#           "expression": "grel:isNumeric(value)",
#           "columnName": "Record Number Copy",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": false,
#                 "l": "false"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "Record Number",
#           "expression": "value",
#           "columnName": "Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "BIBs 021843274, 032802627 Match",
#                 "l": "BIBs 021843274, 032802627 Match"
#               }
#             },
#             {
#               "v": {
#                 "v": "HOL 078302595 without ID",
#                 "l": "HOL 078302595 without ID"
#               }
#             },
#             {
#               "v": {
#                 "v": "HOL 078302588 without ID",
#                 "l": "HOL 078302588 without ID"
#               }
#             },
#             {
#               "v": {
#                 "v": "HOL 078302592 without ID",
#                 "l": "HOL 078302592 without ID"
#               }
#             },
#             {
#               "v": {
#                 "v": "HOL 078302578 without ID",
#                 "l": "HOL 078302578 without ID"
#               }
#             },
#             {
#               "v": {
#                 "v": "HOL 077072085 without ID",
#                 "l": "HOL 077072085 without ID"
#               }
#             },
#             {
#               "v": {
#                 "v": "HOL 078302596 without ID",
#                 "l": "HOL 078302596 without ID"
#               }
#             },
#             {
#               "v": {
#                 "v": "HOL 078302597 without ID",
#                 "l": "HOL 078302597 without ID"
#               }
#             },
#             {
#               "v": {
#                 "v": "HOL 077178230 without ID",
#                 "l": "HOL 077178230 without ID"
#               }
#             },
#             {
#               "v": {
#                 "v": "HOL 078302593 without ID",
#                 "l": "HOL 078302593 without ID"
#               }
#             },
#             {
#               "v": {
#                 "v": "HOL 078302587 without ID",
#                 "l": "HOL 078302587 without ID"
#               }
#             },
#             {
#               "v": {
#                 "v": "HOL 078302601 without ID",
#                 "l": "HOL 078302601 without ID"
#               }
#             },
#             {
#               "v": {
#                 "v": "HOL 078302600 without ID",
#                 "l": "HOL 078302600 without ID"
#               }
#             },
#             {
#               "v": {
#                 "v": "HOL 076979262 without ID",
#                 "l": "HOL 076979262 without ID"
#               }
#             },
#             {
#               "v": {
#                 "v": "HOL 078302580 without ID",
#                 "l": "HOL 078302580 without ID"
#               }
#             },
#             {
#               "v": {
#                 "v": "HOL 078302590 without ID",
#                 "l": "HOL 078302590 without ID"
#               }
#             },
#             {
#               "v": {
#                 "v": "HOL 078302591 without ID",
#                 "l": "HOL 078302591 without ID"
#               }
#             },
#             {
#               "v": {
#                 "v": "HOL 078302589 without ID",
#                 "l": "HOL 078302589 without ID"
#               }
#             },
#             {
#               "v": {
#                 "v": "HOL 078302581 without ID",
#                 "l": "HOL 078302581 without ID"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "Ebook Central BIB URLs",
#           "expression": "isBlank(value)",
#           "columnName": "Ebook Central BIB URLs",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": false,
#                 "l": "false"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "description": "Remove rows"
#   },
#   {
#     "op": "core/row-removal",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number Copy",
#           "expression": "grel:isNumeric(value)",
#           "columnName": "Record Number Copy",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": false,
#                 "l": "false"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "Record Number",
#           "expression": "value",
#           "columnName": "Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "BIBs 021843274, 032802627 Match",
#                 "l": "BIBs 021843274, 032802627 Match"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "description": "Remove rows"
#   }
# ]"""
# messagebox.showinfo(title="Instructions", message="Use LibCentral to confirm that none of the remaining records with multiple HOL are perpetual access entitlements, then remove them.")
# """[
#   {
#     "op": "core/row-removal",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number Copy",
#           "expression": "grel:isNumeric(value)",
#           "columnName": "Record Number Copy",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": false,
#                 "l": "false"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "Record Number",
#           "expression": "value",
#           "columnName": "Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "Ebook Central::413356",
#                 "l": "Ebook Central::413356"
#               }
#             },
#             {
#               "v": {
#                 "v": "Ebook Central::224643",
#                 "l": "Ebook Central::224643"
#               }
#             },
#             {
#               "v": {
#                 "v": "Ebook Central::214288",
#                 "l": "Ebook Central::214288"
#               }
#             },
#             {
#               "v": {
#                 "v": "Ebook Central::191308",
#                 "l": "Ebook Central::191308"
#               }
#             },
#             {
#               "v": {
#                 "v": "BIBs 022688409, 020857739 Match with Different Sublibraries",
#                 "l": "BIBs 022688409, 020857739 Match with Different Sublibraries"
#               }
#             },
#             {
#               "v": {
#                 "v": "Ebook Central::227613",
#                 "l": "Ebook Central::227613"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "description": "Remove rows"
#   }
# ]"""
# messagebox.showinfo(title="Instructions", message="Use LibCentral to confirm that none of the remaining records with Ebook Central IDs are perpetual access entitlements, then remove them.")
# """[
#   {
#     "op": "core/row-removal",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number Copy",
#           "expression": "grel:isNumeric(value)",
#           "columnName": "Record Number Copy",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": false,
#                 "l": "false"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "Record Number Copy",
#           "expression": "grel:contains(value,\"::\")",
#           "columnName": "Record Number Copy",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": true,
#                 "l": "true"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "description": "Remove rows"
#   }
# ]"""

# #ToDo: Look at non-Ebook Central ID FSUER HOL in LibCentral--search by title and compare to the other propriatary IDs
# #ToDo: Assess what non-FSUER HOL remain and if manual check for if FSUER HOL is needed is a good idea

# # Privacy Alerts
#   # HOL 103222944 without ID
#   # HOL 103222942 without ID

# # Found on LibCentral by searching for title without other IDs to confirm that match is correct
#   # HOL 078310273 without ID = 6301246
#   # HOL 078310413 without ID = 6298842
#   # HOL 078310443 without ID = 6302355
#   # HOL 078310266 without ID = 6286342
#   # HOL 078310256 without ID = 6295252
#   # HOL 078310248 without ID = 6301696
#   # HOL 078310244 without ID = 6284652
#   # HOL 078310231 without ID = 6296709
#   # HOL 078310212 without ID = 6301336
#   # HOL 078302756 without ID = 6281766
#   # HOL 078302582 without ID = 6285174
#   # HOL 078302579 without ID = 6287931
#   # HOL 078302577 without ID = 6297305
#   # HOL 078302576 without ID = 6298931


# os.startfile('Determine_HOL_to_Unsuppress_pt2--Ebook_Central_Specific.json')
# #Todo: determine if record selected to keep has "true" in suppressed column, and flag HOL if so--probably change column value to "Needs to be unsuppressed"

# #Subsection: If New 856$u Needed, Supply It
# #ToDo: Determine if value of "Ebook Central BIB URLs" for HOL where "Keep HOL?" starts "TRUE" matches Ebook Central regex
# #ToDo: For HOL not matching above, create new column with Ebook Central URLs
# #ToDo: Add to new column so full contents match line needed in file for manage-18

# #Subsection: If TKR Needed, Supply It
# #See TKR section of repo


# #Section: Remove Unneeded Records
# #Subsection: If FSUER HOL is Only HOL, Delete HOL and BIB
# #ToDo: Delete HOL with "Keep HOL?" starting with "FALSE: Probably Loaded for URL for"

# #Subsection: If Other HOLs Attached to BIB, Suppress FSUER HOL
# #ToDo: All remaining HOL with "Keep HOL?" values starting with "FALSE"
