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
messagebox.showinfo(title="Instructions", message="Create a filter for blanks on \"Inexact Title Record Number\" and set it to true. If the titles in the record don't match, change the values in \"Inexact Title Record Number\" with `toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)`.") # Few enough titles remained after the filter that they could be examined together, and none were matches.

os.startfile('Organize_UXU01_Output_pt6--Ebook_Central_Specific.json')
messagebox.showinfo(title="Instructions", message="Create a filter for blanks on \"No Subtitle Record Number\" and set it to true. If the titles in the record don't match, change the values in \"No Subtitle Record Number\" with `toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)`.") # Single JSON step--see below
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
messagebox.showinfo(title="Instructions", message="Create custom filter on \"Record Number\" with the expression `and(contains(value,\"|\"),contains(value,\"::\"))`. For the BIBs that are true, determine which Ebook Central ID to keep.") # Just two JSON steps--see below
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
        # HOL for SciTech title = FALSE: SciTech Collection [ID <Ebook Central ID> | HOL <HOL number>]
messagebox.showinfo(title="Instructions", message="Create blanks filter on \"Keep HOL?\" and set to true. For the records that remain, adjust the values of \"Keep HOL?\" using the above formats as appropriate.") # See Ebook_Central_Custom_Faceting_pt6.json


#Section: Create Update Files For Records to Remain
#Subsection: Identify Perpetual Access Entitlements via Proprietary Identifiers
messagebox.showinfo(title="Instructions", message="Export a list of the Ebook Central perpetual access entitlements from LibCentral and combine it with a list of the non-FSU-owned perpetual access entitlements created via title match. Save as a CSV named \"Entitlements\" and upload to OpenRefine.")
messagebox.showinfo(title="Instructions", message="Apply the following JSON in the \"Entitlements csv\" project.")
os.startfile('Identify_Perpetual_Access_Entitlements_pt1--Ebook_Central_Specific.json')

messagebox.showinfo(title="Instructions", message="Switch back to the \"UXU60_Cleanup\" project.")
messagebox.showwarning(title="No Handling of New ID Being Duplicate", message="The sample data didn't contain an instance where the IDs found through \"Entitlements csv\" were already part of a record in the project, so there's no steps for handling that situation in the JSON.")
messagebox.showwarning(title="All Record Number Transfers in Single Row Records", message="All the records that gained a Ebook Central ID from \"Entitlements csv\" had a single row; there's no accounting for how to handle a situation where the newly determined ID isn't in the first row of the record. The \"Keep HOL?\" message for the only HOL for a record is also hard coded in.")
os.startfile('Identify_Perpetual_Access_Entitlements_pt2--Ebook_Central_Specific.json')

messagebox.showinfo(title="Instructions", message="Switch back to the \"Entitlements csv\" project.")
os.startfile('Identify_Perpetual_Access_Entitlements_pt3--Ebook_Central_Specific.json')

#Subsection: Determine Records that Need to be Unsuppressed
messagebox.showinfo(title="Instructions", message="Switch back to the \"UXU60_Cleanup\" project.")
messagebox.showwarning(title="Removal of False Positives", message="HOLs for non-Ebook Central holdings on BIBs where another school has an Ebook Central holding are removed here.")
os.startfile('Determine_HOL_to_Unsuppress_pt1--Ebook_Central_Specific.json')
messagebox.showinfo(title="Instructions", message="For any records where \"ID Title\" is a mismatch for \"Title\", null the value of \"Record Number 2\".")
messagebox.showinfo(title="Instructions", message="Use the links in \"Ebook Central BIB URLs\" to confirm the values in \"Record Number 2\". Null any values that are mismatches.")
messagebox.showinfo(title="Instructions", message="Set a blanks filter on \"Ebook Central BIB URLs\" to true and a blanks filter on \"Other BIB URL Info\" to false. Remove the records that don't represent HOL that need to be updated, suppressed, or removed.") # Single JSON step--see below
"""[
  {
    "op": "core/row-removal",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Other BIB URL Info",
          "expression": "isBlank(value)",
          "columnName": "Other BIB URL Info",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": false,
                "l": "false"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        },
        {
          "type": "list",
          "name": "Ebook Central BIB URLs",
          "expression": "isBlank(value)",
          "columnName": "Ebook Central BIB URLs",
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
          "name": "Record Number",
          "expression": "value",
          "columnName": "Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "Ebook Central::4843765",
                "l": "Ebook Central::4843765"
              }
            },
            {
              "v": {
                "v": "HOL 077474858 without ID",
                "l": "HOL 077474858 without ID"
              }
            },
            {
              "v": {
                "v": "HOL 077477918 without ID",
                "l": "HOL 077477918 without ID"
              }
            },
            {
              "v": {
                "v": "Ebook Central::1866947",
                "l": "Ebook Central::1866947"
              }
            },
            {
              "v": {
                "v": "HOL 077154360 without ID",
                "l": "HOL 077154360 without ID"
              }
            },
            {
              "v": {
                "v": "HOL 077474854 without ID",
                "l": "HOL 077474854 without ID"
              }
            },
            {
              "v": {
                "v": "Different sublibraries for BIB 020672657",
                "l": "Different sublibraries for BIB 020672657"
              }
            },
            {
              "v": {
                "v": "Ebook Central::5855425",
                "l": "Ebook Central::5855425"
              }
            },
            {
              "v": {
                "v": "HOL 077152842 without ID",
                "l": "HOL 077152842 without ID"
              }
            },
            {
              "v": {
                "v": "Ebook Central::3443044",
                "l": "Ebook Central::3443044"
              }
            },
            {
              "v": {
                "v": "Ebook Central::5746709",
                "l": "Ebook Central::5746709"
              }
            },
            {
              "v": {
                "v": "Different sublibraries for BIB 020652580",
                "l": "Different sublibraries for BIB 020652580"
              }
            },
            {
              "v": {
                "v": "HOL 077477900 without ID",
                "l": "HOL 077477900 without ID"
              }
            },
            {
              "v": {
                "v": "Ebook Central::5651879",
                "l": "Ebook Central::5651879"
              }
            },
            {
              "v": {
                "v": "Ebook Central::4863266",
                "l": "Ebook Central::4863266"
              }
            },
            {
              "v": {
                "v": "Different sublibraries for BIB 020652214",
                "l": "Different sublibraries for BIB 020652214"
              }
            },
            {
              "v": {
                "v": "Ebook Central::5495919",
                "l": "Ebook Central::5495919"
              }
            },
            {
              "v": {
                "v": "HOL 077093441 without ID",
                "l": "HOL 077093441 without ID"
              }
            },
            {
              "v": {
                "v": "Ebook Central::5317541",
                "l": "Ebook Central::5317541"
              }
            },
            {
              "v": {
                "v": "HOL 078310079 without ID",
                "l": "HOL 078310079 without ID"
              }
            },
            {
              "v": {
                "v": "HOL 111455030 without ID",
                "l": "HOL 111455030 without ID"
              }
            },
            {
              "v": {
                "v": "HOL 096639842 without ID",
                "l": "HOL 096639842 without ID"
              }
            },
            {
              "v": {
                "v": "Ebook Central::5208444",
                "l": "Ebook Central::5208444"
              }
            },
            {
              "v": {
                "v": "Ebook Central::5742555",
                "l": "Ebook Central::5742555"
              }
            },
            {
              "v": {
                "v": "Ebook Central::5884274",
                "l": "Ebook Central::5884274"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "description": "Remove rows"
  }
]"""
messagebox.showinfo(title="Instructions", message="Using that same filter setup, examine the records that have both Ebook Central and other URLs and confirm the appropriate message is in \"Keep HOL?\". If necessary, make updates.") # Single JSON step--see below
"""[
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Other BIB URL Info",
          "expression": "isBlank(value)",
          "columnName": "Other BIB URL Info",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": false,
                "l": "false"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        },
        {
          "type": "list",
          "name": "Ebook Central BIB URLs",
          "expression": "isBlank(value)",
          "columnName": "Ebook Central BIB URLs",
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
          "name": "Record Number",
          "expression": "value",
          "columnName": "Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "Ebook Central::635509",
                "l": "Ebook Central::635509"
              }
            },
            {
              "v": {
                "v": "Ebook Central::3301384",
                "l": "Ebook Central::3301384"
              }
            },
            {
              "v": {
                "v": "Ebook Central::3318823",
                "l": "Ebook Central::3318823"
              }
            },
            {
              "v": {
                "v": "Ebook Central::864058",
                "l": "Ebook Central::864058"
              }
            },
            {
              "v": {
                "v": "Ebook Central::601941",
                "l": "Ebook Central::601941"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Keep HOL?",
    "expression": "grel:if(isNotNull(cells[\"Ebook Central BIB URLs\"].value),\"TRUE: FSUER HOL for \"+split(value,\" \")[-1],value)",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Keep HOL? using expression grel:if(isNotNull(cells[\"Ebook Central BIB URLs\"].value),\"TRUE: FSUER HOL for \"+split(value,\" \")[-1],value)"
  }
]"""

messagebox.showwarning(title="Removal of Public Ebook Library URLs", message="After the public library URLs are removed, there's not a removal of any rows that amy be completely blank because there weren't any in the initial sample.")
os.startfile('Determine_HOL_to_Unsuppress_pt2--EC_After_Cataloging.json')
messagebox.showinfo(title="Instructions", message="Set a blanks filter on \"Record Number 2\" to true and a custom filter with \"startsWith(value,\"Ebook Central\")\" on \"Record Number\" to false. Follow the links in \"Ebook Central BIB URLs\" for the visible titles to find their Ebook Central IDs. If the title is a perpetual access entitlement, change \"Record Number 2\" to the ID value, otherwise, change the value of \"Record Number 2\" to \"Not Accessible\".") # See Ebook_Central_Custom_Faceting_pt7.json

messagebox.showwarning(title="Handling \"Keep HOL?\" for Newly Consolidated Records", message="Not all of the steps for generating \"Keep HOL?\" values were replicated from Select_HOL_to_Keep--EC_After_Cataloging.json, just the ones for a BIB seemingly loaded for its URL and the pair to such a BIB.")
os.startfile('Determine_HOL_to_Unsuppress_pt3--EC_After_Cataloging.json')

#Subsection: If New 856$u Needed, Supply It
messagebox.showwarning(title="Ebook Central URLs with Proxy", message="None of the Ebook Central URLs had the proxy header, so there's no step for calling those out.")
os.startfile('Create_New_URLs--EC_After_Cataloging.json')

#Subsection: If TKR Needed, Supply It
messagebox.showwarning(title="Hard Coded Number of TKR Columns", message="This hard codes that there are four TKR columns being combined; it needs to be redone as a loop.")
os.startfile('Create_New_TKRs_pt1--EC_After_Cataloging.json')
messagebox.showinfo(title="Instructions", message="Set a blanks filter on \"TKR manage-18\" to false and download the project. Remove all columns but \"HOL Number\" and paste `=(TEXT(A2,\"000000000\") & \"UXU60\")` into cell B2. Fill the formula down, move the results to copy as value to column A, then delete column B and row 1. Save the file as a .txt with a name of lowercase letter and numbers totaling less than 10 characters. Close the file, go to the file location, and remove the .txt extension from the file name.")
messagebox.showinfo(title="Instructions", message="Go to https://susopac.falsc.org/cgi-bin/afv for the production server, log in with Aleph credentials, and upload the newly created file to \"alephe/scratch\".")
messagebox.showinfo(title="Instructions", message="In Alpeh Production, go to Services > Retrieve Catalog Records > print-03. Put the name of the file in \"Input File\", type a file name with no capital letters or spaces ending with a .txt file extension in \"Output File\", enter \"CAT##\" and \"852##\" in the first \"Field + Indicator\" boxes, confirm that \"Format\" is set to Aleph Sequential, and finally change \"Library\" to \"UXU60\". When Batch Log says the job is complete, download the file.")
messagebox.showinfo(title="Instructions", message="Load recently downloaded Aleph Sequential file into OpenRefine, parsing the data as fixed-width field text files with column widths 10, 4, 4. Name the project \"HOL_Dates\".")

messagebox.showinfo(title="Instructions", message="Run the following JSON on project \"HOL_Dates\".")
os.startfile('Create_New_TKRs_pt2--EC_After_Cataloging.json')


#Section: Indicate Records to Remove
# Previously had subsections for "Indicate HOLs where BIB and HOL Deletion is Possible" and "If Other HOLs Attached to BIB, Suppress FSUER HOL"--number of steps needed for each is so few, combining them made more sense
os.startfile('Indicate_Removals_pt1--EC_After_Cataloging.json')
messagebox.showinfo(title="Instructions", message="Create text filters on \"Keep Status\" and \"Removal Reason\", a custom filter on \"Record Number\" using `row.record.toRowIndex-row.record.fromRowIndex`, and a custom filter on \"Keep HOL?\" using `replace(value,find(value,/ID \d*/)[0],\"ID\")`. Set the \"Keep Status\" filter to \"FALSE\".")
messagebox.showinfo(title="Instructions", message="Use the \"Record Number\" filter to review the records with three or more rows. Change the values of \"Removal Reason\" as appropriate.") # See Ebook_Central_Custom_Faceting_pt8.json
messagebox.showinfo(title="Instructions", message="Set the \"Record Number\" filter to \"2\". Select \"TRUE: FSUER HOL with ACQ for ID\" in \"Keep HOL?\" and \"FALSE: FSUER HOL with ACQ\" in \"Removal Reason\". Check the ACQ attached to all of the visible BIBs, double check which BIB/HOL combo to keep, and provide details on the reason for removal on the BIB/HOL combo suggested for removal.") # See Ebook_Central_Custom_Faceting_pt8.json

messagebox.showinfo(title="Instructions", message="Change view to rows, then filter for non-blanks in \"Removal Reason\" to get list of records to remove.")