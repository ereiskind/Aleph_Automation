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

# os.startfile('Organize_UXU01_Output_pt5--Ebook_Central_Specific.json')
# messagebox.showinfo(title="Instructions", message="Create a filter for blanks on \"Inexact Title Record Number\" and set it to true. If the titles in the record don't match, change the values in \"Inexact Title Record Number\" with \"toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)\".")
# """[
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Inexact Title Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "Inexact Title Record Number",
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
#           "name": "Inexact Title Record Number",
#           "expression": "value",
#           "columnName": "Inexact Title Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "10182",
#                 "l": "10182"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Inexact Title Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Inexact Title Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "Inexact Title Record Number",
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
#           "name": "Inexact Title Record Number",
#           "expression": "value",
#           "columnName": "Inexact Title Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "10665",
#                 "l": "10665"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Inexact Title Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Inexact Title Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "Inexact Title Record Number",
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
#           "name": "Inexact Title Record Number",
#           "expression": "value",
#           "columnName": "Inexact Title Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "11148",
#                 "l": "11148"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Inexact Title Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Inexact Title Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "Inexact Title Record Number",
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
#           "name": "Inexact Title Record Number",
#           "expression": "value",
#           "columnName": "Inexact Title Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "1119",
#                 "l": "1119"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Inexact Title Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Inexact Title Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "Inexact Title Record Number",
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
#           "name": "Inexact Title Record Number",
#           "expression": "value",
#           "columnName": "Inexact Title Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "11203",
#                 "l": "11203"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Inexact Title Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Inexact Title Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "Inexact Title Record Number",
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
#           "name": "Inexact Title Record Number",
#           "expression": "value",
#           "columnName": "Inexact Title Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "11211",
#                 "l": "11211"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Inexact Title Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Inexact Title Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "Inexact Title Record Number",
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
#           "name": "Inexact Title Record Number",
#           "expression": "value",
#           "columnName": "Inexact Title Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "1158",
#                 "l": "1158"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Inexact Title Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Inexact Title Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "Inexact Title Record Number",
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
#           "name": "Inexact Title Record Number",
#           "expression": "value",
#           "columnName": "Inexact Title Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "12343",
#                 "l": "12343"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Inexact Title Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Inexact Title Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "Inexact Title Record Number",
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
#           "name": "Inexact Title Record Number",
#           "expression": "value",
#           "columnName": "Inexact Title Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "2253",
#                 "l": "2253"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Inexact Title Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Inexact Title Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "Inexact Title Record Number",
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
#           "name": "Inexact Title Record Number",
#           "expression": "value",
#           "columnName": "Inexact Title Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "238",
#                 "l": "238"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Inexact Title Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Inexact Title Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "Inexact Title Record Number",
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
#           "name": "Inexact Title Record Number",
#           "expression": "value",
#           "columnName": "Inexact Title Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "253",
#                 "l": "253"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Inexact Title Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Inexact Title Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "Inexact Title Record Number",
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
#           "name": "Inexact Title Record Number",
#           "expression": "value",
#           "columnName": "Inexact Title Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "2589",
#                 "l": "2589"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Inexact Title Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Inexact Title Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "Inexact Title Record Number",
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
#           "name": "Inexact Title Record Number",
#           "expression": "value",
#           "columnName": "Inexact Title Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "263",
#                 "l": "263"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Inexact Title Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Inexact Title Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "Inexact Title Record Number",
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
#           "name": "Inexact Title Record Number",
#           "expression": "value",
#           "columnName": "Inexact Title Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "282",
#                 "l": "282"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Inexact Title Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Inexact Title Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "Inexact Title Record Number",
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
#           "name": "Inexact Title Record Number",
#           "expression": "value",
#           "columnName": "Inexact Title Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "3675",
#                 "l": "3675"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Inexact Title Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Inexact Title Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "Inexact Title Record Number",
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
#           "name": "Inexact Title Record Number",
#           "expression": "value",
#           "columnName": "Inexact Title Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "456",
#                 "l": "456"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Inexact Title Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Inexact Title Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "Inexact Title Record Number",
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
#           "name": "Inexact Title Record Number",
#           "expression": "value",
#           "columnName": "Inexact Title Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "7394",
#                 "l": "7394"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Inexact Title Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Inexact Title Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "Inexact Title Record Number",
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
#           "name": "Inexact Title Record Number",
#           "expression": "value",
#           "columnName": "Inexact Title Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "8105",
#                 "l": "8105"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Inexact Title Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Inexact Title Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "Inexact Title Record Number",
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
#           "name": "Inexact Title Record Number",
#           "expression": "value",
#           "columnName": "Inexact Title Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "8528",
#                 "l": "8528"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Inexact Title Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Inexact Title Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "Inexact Title Record Number",
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
#           "name": "Inexact Title Record Number",
#           "expression": "value",
#           "columnName": "Inexact Title Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "8932",
#                 "l": "8932"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Inexact Title Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Inexact Title Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "Inexact Title Record Number",
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
#           "name": "Inexact Title Record Number",
#           "expression": "value",
#           "columnName": "Inexact Title Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "8984",
#                 "l": "8984"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Inexact Title Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Inexact Title Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "Inexact Title Record Number",
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
#           "name": "Inexact Title Record Number",
#           "expression": "value",
#           "columnName": "Inexact Title Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "9993",
#                 "l": "9993"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Inexact Title Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   }
# ]"""
# os.startfile('Organize_UXU01_Output_pt6--Ebook_Central_Specific.json')
# messagebox.showinfo(title="Instructions", message="Create a filter for blanks on \"No Subtitle Record Number\" and set it to true. If the titles in the record don't match, change the values in \"No Subtitle Record Number\" with \"toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)\".")
# """[
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "No Subtitle Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "No Subtitle Record Number",
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
#           "name": "No Subtitle Record Number",
#           "expression": "value",
#           "columnName": "No Subtitle Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "10917",
#                 "l": "10917"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "No Subtitle Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column No Subtitle Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "No Subtitle Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "No Subtitle Record Number",
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
#           "name": "No Subtitle Record Number",
#           "expression": "value",
#           "columnName": "No Subtitle Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "1356",
#                 "l": "1356"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "No Subtitle Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column No Subtitle Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "No Subtitle Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "No Subtitle Record Number",
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
#           "name": "No Subtitle Record Number",
#           "expression": "value",
#           "columnName": "No Subtitle Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "1890",
#                 "l": "1890"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "No Subtitle Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column No Subtitle Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "No Subtitle Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "No Subtitle Record Number",
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
#           "name": "No Subtitle Record Number",
#           "expression": "value",
#           "columnName": "No Subtitle Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "1951",
#                 "l": "1951"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "No Subtitle Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column No Subtitle Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "No Subtitle Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "No Subtitle Record Number",
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
#           "name": "No Subtitle Record Number",
#           "expression": "value",
#           "columnName": "No Subtitle Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "2217",
#                 "l": "2217"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "No Subtitle Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column No Subtitle Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "No Subtitle Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "No Subtitle Record Number",
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
#           "name": "No Subtitle Record Number",
#           "expression": "value",
#           "columnName": "No Subtitle Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "234",
#                 "l": "234"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "No Subtitle Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column No Subtitle Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "No Subtitle Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "No Subtitle Record Number",
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
#           "name": "No Subtitle Record Number",
#           "expression": "value",
#           "columnName": "No Subtitle Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "249",
#                 "l": "249"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "No Subtitle Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column No Subtitle Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "No Subtitle Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "No Subtitle Record Number",
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
#           "name": "No Subtitle Record Number",
#           "expression": "value",
#           "columnName": "No Subtitle Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "2511",
#                 "l": "2511"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "No Subtitle Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column No Subtitle Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "No Subtitle Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "No Subtitle Record Number",
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
#           "name": "No Subtitle Record Number",
#           "expression": "value",
#           "columnName": "No Subtitle Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "278",
#                 "l": "278"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "No Subtitle Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column No Subtitle Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "No Subtitle Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "No Subtitle Record Number",
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
#           "name": "No Subtitle Record Number",
#           "expression": "value",
#           "columnName": "No Subtitle Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "3191",
#                 "l": "3191"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "No Subtitle Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column No Subtitle Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "No Subtitle Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "No Subtitle Record Number",
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
#           "name": "No Subtitle Record Number",
#           "expression": "value",
#           "columnName": "No Subtitle Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "3287",
#                 "l": "3287"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "No Subtitle Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column No Subtitle Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "No Subtitle Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "No Subtitle Record Number",
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
#           "name": "No Subtitle Record Number",
#           "expression": "value",
#           "columnName": "No Subtitle Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "4281",
#                 "l": "4281"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "No Subtitle Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column No Subtitle Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "No Subtitle Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "No Subtitle Record Number",
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
#           "name": "No Subtitle Record Number",
#           "expression": "value",
#           "columnName": "No Subtitle Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "4498",
#                 "l": "4498"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "No Subtitle Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column No Subtitle Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "No Subtitle Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "No Subtitle Record Number",
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
#           "name": "No Subtitle Record Number",
#           "expression": "value",
#           "columnName": "No Subtitle Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "4616",
#                 "l": "4616"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "No Subtitle Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column No Subtitle Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "No Subtitle Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "No Subtitle Record Number",
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
#           "name": "No Subtitle Record Number",
#           "expression": "value",
#           "columnName": "No Subtitle Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "4731",
#                 "l": "4731"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "No Subtitle Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column No Subtitle Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "No Subtitle Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "No Subtitle Record Number",
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
#           "name": "No Subtitle Record Number",
#           "expression": "value",
#           "columnName": "No Subtitle Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "4767",
#                 "l": "4767"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "No Subtitle Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column No Subtitle Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "No Subtitle Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "No Subtitle Record Number",
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
#           "name": "No Subtitle Record Number",
#           "expression": "value",
#           "columnName": "No Subtitle Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "5896",
#                 "l": "5896"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "No Subtitle Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column No Subtitle Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "No Subtitle Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "No Subtitle Record Number",
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
#           "name": "No Subtitle Record Number",
#           "expression": "value",
#           "columnName": "No Subtitle Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "6267",
#                 "l": "6267"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "No Subtitle Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column No Subtitle Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "No Subtitle Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "No Subtitle Record Number",
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
#           "name": "No Subtitle Record Number",
#           "expression": "value",
#           "columnName": "No Subtitle Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "6945",
#                 "l": "6945"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "No Subtitle Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column No Subtitle Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "No Subtitle Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "No Subtitle Record Number",
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
#           "name": "No Subtitle Record Number",
#           "expression": "value",
#           "columnName": "No Subtitle Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "7750",
#                 "l": "7750"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "No Subtitle Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column No Subtitle Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "No Subtitle Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "No Subtitle Record Number",
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
#           "name": "No Subtitle Record Number",
#           "expression": "value",
#           "columnName": "No Subtitle Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "8747",
#                 "l": "8747"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "No Subtitle Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column No Subtitle Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "No Subtitle Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "No Subtitle Record Number",
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
#           "name": "No Subtitle Record Number",
#           "expression": "value",
#           "columnName": "No Subtitle Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "9390",
#                 "l": "9390"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "No Subtitle Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column No Subtitle Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "No Subtitle Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "No Subtitle Record Number",
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
#           "name": "No Subtitle Record Number",
#           "expression": "value",
#           "columnName": "No Subtitle Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "9395",
#                 "l": "9395"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "No Subtitle Record Number",
#     "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column No Subtitle Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
#   }
# ]"""
# #ToDo: Get list of columns that will need to be moved over to UXU60 OpenRefine project--the pivot happens in the following JSON
# os.startfile('Organize_UXU01_Output_pt7--Ebook_Central_Specific.json')
# messagebox.showinfo(title="Instructions", message="In record view, create a filter for blanks on \"Record Number 1\" and set it to false. Create a text filter on both \"Record Number 1\" and \"Record Number 2\".")
# messagebox.showinfo(title="Instructions", message="Selct \"false\" on the blanks filter for \"Record Number 1\". For the records that match, determine which propriatary ID matches the title and change all values in \"Record Number\" with the propriatary ID to that number.")
# """[
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 1",
#           "expression": "value",
#           "columnName": "Record Number 1",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "false",
#                 "l": "false"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "030808190",
#                 "l": "030808190"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:if(startsWith(toString(value),\"Ebook Central\"),substring(value,0,indexOf(value,\"::\")+2)+\"951321\",value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:if(startsWith(toString(value),\"Ebook Central\"),substring(value,0,indexOf(value,\"::\")+2)+\"951321\",value)"
#   }
# ]"""
# messagebox.showinfo(title="Instructions", message="Select each number in the \"Record Number 2\" text filter on at a time. Determine which BIBs have a given propriatary ID, change the value of \"Record Number\" to that ID by filtering on \"BIB Number\", then remove the BIB filter and null \"Ebook Central\" and then null \"Record Number 2\".")
# """[
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "034026703",
#                 "l": "034026703"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "value",
#           "columnName": "Record Number 1",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "false",
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
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::4033723\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::4033723\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "030808190",
#                 "l": "030808190"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "value",
#           "columnName": "Record Number 1",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "false",
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
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::951321\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::951321\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 3303,
#                 "l": "3303"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "020372573",
#                 "l": "020372573"
#               }
#             },
#             {
#               "v": {
#                 "v": "030829337",
#                 "l": "030829337"
#               }
#             },
#             {
#               "v": {
#                 "v": "036694721",
#                 "l": "036694721"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::371984\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::371984\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 3303,
#                 "l": "3303"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "022485946",
#                 "l": "022485946"
#               }
#             },
#             {
#               "v": {
#                 "v": "036719919",
#                 "l": "036719919"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::993561\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::993561\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 3303,
#                 "l": "3303"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "031038180",
#                 "l": "031038180"
#               }
#             },
#             {
#               "v": {
#                 "v": "036720121",
#                 "l": "036720121"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::1083660\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::1083660\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 3303,
#                 "l": "3303"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Ebook Central",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Ebook Central using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 3303,
#                 "l": "3303"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number 2",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number 2 using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 4804,
#                 "l": "4804"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "035303187",
#                 "l": "035303187"
#               }
#             },
#             {
#               "v": {
#                 "v": "036719727",
#                 "l": "036719727"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::918160\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::918160\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 4804,
#                 "l": "4804"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "036719767",
#                 "l": "036719767"
#               }
#             },
#             {
#               "v": {
#                 "v": "035303192",
#                 "l": "035303192"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::947601\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::947601\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 4804,
#                 "l": "4804"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Ebook Central",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Ebook Central using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 4804,
#                 "l": "4804"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number 2",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number 2 using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 10325,
#                 "l": "10325"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "037183163",
#                 "l": "037183163"
#               }
#             },
#             {
#               "v": {
#                 "v": "035303308",
#                 "l": "035303308"
#               }
#             },
#             {
#               "v": {
#                 "v": "035032697",
#                 "l": "035032697"
#               }
#             },
#             {
#               "v": {
#                 "v": "037183125",
#                 "l": "037183125"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::1882091\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::1882091\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 10325,
#                 "l": "10325"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "035303309",
#                 "l": "035303309"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::1794093\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::1794093\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 10325,
#                 "l": "10325"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Ebook Central",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Ebook Central using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 10325,
#                 "l": "10325"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number 2",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number 2 using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 10208,
#                 "l": "10208"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "035302892",
#                 "l": "035302892"
#               }
#             },
#             {
#               "v": {
#                 "v": "036695744",
#                 "l": "036695744"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::487648\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::487648\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 10208,
#                 "l": "10208"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "037183151",
#                 "l": "037183151"
#               }
#             },
#             {
#               "v": {
#                 "v": "034592084",
#                 "l": "034592084"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::1840834\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::1840834\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 10208,
#                 "l": "10208"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Ebook Central",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Ebook Central using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 10208,
#                 "l": "10208"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number 2",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number 2 using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 2248,
#                 "l": "2248"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "025126910",
#                 "l": "025126910"
#               }
#             },
#             {
#               "v": {
#                 "v": "036695934",
#                 "l": "036695934"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::4657614\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::4657614\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 2248,
#                 "l": "2248"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "032013136",
#                 "l": "032013136"
#               }
#             },
#             {
#               "v": {
#                 "v": "036695965",
#                 "l": "036695965"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::4960447\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::4960447\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 2248,
#                 "l": "2248"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Ebook Central",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Ebook Central using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 2248,
#                 "l": "2248"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number 2",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number 2 using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 3613,
#                 "l": "3613"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "036695101",
#                 "l": "036695101"
#               }
#             },
#             {
#               "v": {
#                 "v": "032598854",
#                 "l": "032598854"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::615908\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::615908\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 3613,
#                 "l": "3613"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "036695100",
#                 "l": "036695100"
#               }
#             },
#             {
#               "v": {
#                 "v": "032598855",
#                 "l": "032598855"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::615902\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::615902\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 3613,
#                 "l": "3613"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Ebook Central",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Ebook Central using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 3613,
#                 "l": "3613"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number 2",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number 2 using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 5805,
#                 "l": "5805"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "036719259",
#                 "l": "036719259"
#               }
#             },
#             {
#               "v": {
#                 "v": "032080849",
#                 "l": "032080849"
#               }
#             },
#             {
#               "v": {
#                 "v": "032080848",
#                 "l": "032080848"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::240427\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::240427\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 5805,
#                 "l": "5805"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "036719258",
#                 "l": "036719258"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::240426\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::240426\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 5805,
#                 "l": "5805"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Ebook Central",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Ebook Central using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 5805,
#                 "l": "5805"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number 2",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number 2 using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 6999,
#                 "l": "6999"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "036719534",
#                 "l": "036719534"
#               }
#             },
#             {
#               "v": {
#                 "v": "034157131",
#                 "l": "034157131"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::728546\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::728546\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 6999,
#                 "l": "6999"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "036719533",
#                 "l": "036719533"
#               }
#             },
#             {
#               "v": {
#                 "v": "034157132",
#                 "l": "034157132"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::728471\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::728471\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 6999,
#                 "l": "6999"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Ebook Central",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Ebook Central using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 6999,
#                 "l": "6999"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number 2",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number 2 using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 7895,
#                 "l": "7895"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "036695699",
#                 "l": "036695699"
#               }
#             },
#             {
#               "v": {
#                 "v": "023804958",
#                 "l": "023804958"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::874224\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::874224\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 7895,
#                 "l": "7895"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "034796376",
#                 "l": "034796376"
#               }
#             },
#             {
#               "v": {
#                 "v": "030808190",
#                 "l": "030808190"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::951321\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::951321\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 7895,
#                 "l": "7895"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Ebook Central",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Ebook Central using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 7895,
#                 "l": "7895"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number 2",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number 2 using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 2134,
#                 "l": "2134"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "037183193",
#                 "l": "037183193"
#               }
#             },
#             {
#               "v": {
#                 "v": "033325517",
#                 "l": "033325517"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::1895824\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::1895824\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 2134,
#                 "l": "2134"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "036855676",
#                 "l": "036855676"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::4455265\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::4455265\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 2134,
#                 "l": "2134"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Ebook Central",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Ebook Central using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 2134,
#                 "l": "2134"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number 2",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number 2 using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 8944,
#                 "l": "8944"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "037183598",
#                 "l": "037183598"
#               }
#             },
#             {
#               "v": {
#                 "v": "034650631",
#                 "l": "034650631"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::4523847\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::4523847\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 8944,
#                 "l": "8944"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Ebook Central",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Ebook Central using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 8944,
#                 "l": "8944"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number 2",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number 2 using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 9471,
#                 "l": "9471"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "037026615",
#                 "l": "037026615"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::5824668\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::5824668\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 9471,
#                 "l": "9471"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "037497728",
#                 "l": "037497728"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::5878292\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::5878292\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 9471,
#                 "l": "9471"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Ebook Central",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Ebook Central using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 9471,
#                 "l": "9471"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number 2",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number 2 using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 8997,
#                 "l": "8997"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "036810109",
#                 "l": "036810109"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::1808781\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::1808781\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 8997,
#                 "l": "8997"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "036848159",
#                 "l": "036848159"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::4940426\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::4940426\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 8997,
#                 "l": "8997"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Ebook Central",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Ebook Central using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 8997,
#                 "l": "8997"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number 2",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number 2 using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 8671,
#                 "l": "8671"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "036810107",
#                 "l": "036810107"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::4741076\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::4741076\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 8671,
#                 "l": "8671"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "036810113",
#                 "l": "036810113"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::1931604\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::1931604\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 8671,
#                 "l": "8671"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Ebook Central",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Ebook Central using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 8671,
#                 "l": "8671"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number 2",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number 2 using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 2749,
#                 "l": "2749"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "037182928",
#                 "l": "037182928"
#               }
#             },
#             {
#               "v": {
#                 "v": "033802155",
#                 "l": "033802155"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::1652169\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::1652169\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 2749,
#                 "l": "2749"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "033254284",
#                 "l": "033254284"
#               }
#             },
#             {
#               "v": {
#                 "v": "037202570",
#                 "l": "037202570"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::270457\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::270457\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 2749,
#                 "l": "2749"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Ebook Central",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Ebook Central using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 2749,
#                 "l": "2749"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number 2",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number 2 using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 748,
#                 "l": "748"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "037182824",
#                 "l": "037182824"
#               }
#             },
#             {
#               "v": {
#                 "v": "033118104",
#                 "l": "033118104"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::1584082\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::1584082\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 748,
#                 "l": "748"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "037182725",
#                 "l": "037182725"
#               }
#             },
#             {
#               "v": {
#                 "v": "033118119",
#                 "l": "033118119"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::1378784\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::1378784\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 748,
#                 "l": "748"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Ebook Central",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Ebook Central using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 748,
#                 "l": "748"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number 2",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number 2 using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 10894,
#                 "l": "10894"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "034208538",
#                 "l": "034208538"
#               }
#             },
#             {
#               "v": {
#                 "v": "034592122",
#                 "l": "034592122"
#               }
#             },
#             {
#               "v": {
#                 "v": "037183295",
#                 "l": "037183295"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::2194890\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::2194890\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 10894,
#                 "l": "10894"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Ebook Central",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Ebook Central using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 10894,
#                 "l": "10894"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number 2",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number 2 using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 1711,
#                 "l": "1711"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "036810110",
#                 "l": "036810110"
#               }
#             },
#             {
#               "v": {
#                 "v": "037228798",
#                 "l": "037228798"
#               }
#             },
#             {
#               "v": {
#                 "v": "036810112",
#                 "l": "036810112"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::1769040\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::1769040\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 1711,
#                 "l": "1711"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Ebook Central",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Ebook Central using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 1711,
#                 "l": "1711"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number 2",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number 2 using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 10963,
#                 "l": "10963"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "034636858",
#                 "l": "034636858"
#               }
#             },
#             {
#               "v": {
#                 "v": "037183301",
#                 "l": "037183301"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::3035208\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::3035208\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 10963,
#                 "l": "10963"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Ebook Central",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Ebook Central using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 10963,
#                 "l": "10963"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number 2",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number 2 using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 1181,
#                 "l": "1181"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "036695787",
#                 "l": "036695787"
#               }
#             },
#             {
#               "v": {
#                 "v": "035303347",
#                 "l": "035303347"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::2056249\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::2056249\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 1181,
#                 "l": "1181"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Ebook Central",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Ebook Central using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 1181,
#                 "l": "1181"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number 2",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number 2 using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 4125,
#                 "l": "4125"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "021325065",
#                 "l": "021325065"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::3375635\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::3375635\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 4125,
#                 "l": "4125"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "021560792",
#                 "l": "021560792"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::3375698\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::3375698\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 4125,
#                 "l": "4125"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Ebook Central",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Ebook Central using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 4125,
#                 "l": "4125"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number 2",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number 2 using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 726,
#                 "l": "726"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "035303349",
#                 "l": "035303349"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::4416046\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::4416046\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 726,
#                 "l": "726"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "036695815",
#                 "l": "036695815"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::5247984\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::5247984\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 726,
#                 "l": "726"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Ebook Central",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Ebook Central using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 726,
#                 "l": "726"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number 2",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number 2 using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 7608,
#                 "l": "7608"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "034398730",
#                 "l": "034398730"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::4428956\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::4428956\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 7608,
#                 "l": "7608"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "036695816",
#                 "l": "036695816"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::5247985\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::5247985\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 7608,
#                 "l": "7608"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Ebook Central",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Ebook Central using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 7608,
#                 "l": "7608"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number 2",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number 2 using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 8871,
#                 "l": "8871"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "022195855",
#                 "l": "022195855"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::231740\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::231740\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 8871,
#                 "l": "8871"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "023089420",
#                 "l": "023089420"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::231741\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::231741\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 8871,
#                 "l": "8871"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Ebook Central",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Ebook Central using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 8871,
#                 "l": "8871"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number 2",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number 2 using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 17034,
#                 "l": "17034"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "036984692",
#                 "l": "036984692"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::5283177\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::5283177\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 17034,
#                 "l": "17034"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Ebook Central",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Ebook Central using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number 1",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number 1",
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
#           "name": "Record Number 2",
#           "expression": "value",
#           "columnName": "Record Number 2",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": 17034,
#                 "l": "17034"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number 2",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number 2 using expression null"
#   }
# ]"""
# os.startfile('Organize_UXU01_Output_pt8--Ebook_Central_Specific.json')
# messagebox.showinfo(title="Instructions", message="Create text filter on \"ISBN Values 1\" and select each string of IDs individually. Determine which Ebook Central ID is the best match for that BIB, then change \"Record Number\" to \"Ebook Central::\" plus that ID.")
# """[
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "ISBN Value 1",
#           "expression": "value",
#           "columnName": "ISBN Value 1",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "1121224|845138",
#                 "l": "1121224|845138"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::1121224\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::1121224\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "ISBN Value 1",
#           "expression": "value",
#           "columnName": "ISBN Value 1",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "1698569|6165086",
#                 "l": "1698569|6165086"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::1698569\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::1698569\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "ISBN Value 1",
#           "expression": "value",
#           "columnName": "ISBN Value 1",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "3053278|3052071",
#                 "l": "3053278|3052071"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "020430629",
#                 "l": "020430629"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::3052071\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::3052071\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "ISBN Value 1",
#           "expression": "value",
#           "columnName": "ISBN Value 1",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "3053278|3052071",
#                 "l": "3053278|3052071"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "021459401",
#                 "l": "021459401"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::3053278\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::3053278\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "ISBN Value 1",
#           "expression": "value",
#           "columnName": "ISBN Value 1",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "4197994|6163852",
#                 "l": "4197994|6163852"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::4197994\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::4197994\""
#   }
# ]"""
# os.startfile('Organize_UXU01_Output_pt9--Ebook_Central_Specific.json')
# messagebox.showinfo(title="Instructions", message="Create custom filter on \"Record Number\" with the expression \"and(contains(value,\"|\"),contains(value,\"::\"))\". For the BIBs that are true, determine which Ebook Central ID to keep.")
# """[
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number",
#           "expression": "grel:and(contains(value,\"|\"),contains(value,\"::\"))",
#           "columnName": "Record Number",
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
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "031147384",
#                 "l": "031147384"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::4953675\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::4953675\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number",
#           "expression": "grel:and(contains(value,\"|\"),contains(value,\"::\"))",
#           "columnName": "Record Number",
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
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "032986539",
#                 "l": "032986539"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Credo\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Credo\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number",
#           "expression": "grel:and(contains(value,\"|\"),contains(value,\"::\"))",
#           "columnName": "Record Number",
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
#           "name": "BIB Number",
#           "expression": "value",
#           "columnName": "BIB Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "034636879",
#                 "l": "034636879"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::4033722\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::4033722\""
#   }
# ]"""

# #Subsection: Organize UXU60 Output
# messagebox.showinfo(title="Instructions", message="Load Aleph Sequential file with UXU60 info into OpenRefine with column widths 10, 5, 3. Name the project \"UXU60_Cleanup\".")
# os.startfile('Organize_HOL_for_Duplicate_BIB.json')
# TKR_Loop(1,5)
# messagebox.showwarning(title="Removing Non-FSU HOLs", message="Export results now for complete HOL info--next JSON will remove non-FSU HOLs.")
# os.startfile('Finish_Organizing_HOLs.json')
# # UXU01 records without matching HOL are records that have no FSU HOL
# # UXU60 records without matching BIB are records where FSU BIB isn't for an Ebook Central record

# #Subsection: Get List of FSU URLs
# messagebox.showinfo(title="Instructions", message="Load Aleph Sequential file with UXU01 info into OpenRefine with column widths 10, 6, 2 as a project named \"URLs\".")
# messagebox.showwarning(title="Identifying SciTech URLs", message="The Ebook Central specific JSON has steps to identify the URLs with 856$3 indicating that the records are for SciTech titles.")
# os.startfile('Extract_URLs--Ebook_Central_Specific.json')


# #Section: Determine Which Records to Keep
# #Subsection: Match Duplicate BIB Records
# messagebox.showinfo(title="Instructions", message="This JSON continues using the UXU60 OpenRefine project.")
# messagebox.showwarning(title="Cell Cross Project Columns", message="The JSON currently has ID columns for the Ebook Central BIB project hard-coded into it.")
# messagebox.showwarning(title="Fill Down", message="The JSON fills down all the columns, so it needs to know what columns it has.")
# messagebox.showwarning(title="Fill Up and Down Ticklers", message="The JSON fills up and down then blanks down the TKR columns as well, so in addition to needing to know how many to do, a loop needs to be created.")
# #ToDo: Get list of columns to pull from UXU01 OpenRefine project and create loop to load them into this project with the last column being the first JSON object so all the object can use the same column insert index
# os.startfile('Match_Duplicate_Records--Ebook_Central_Specific.json')
# messagebox.showinfo(title="Instructions", message="Set text filter on \"Ebook Central IDs\" to false and create a text filter for \"HOL Number\". For all records that match, select the HOL numbers, change the view to rows, clear the filter on \"Ebook Central IDs\", and change the value of \"Record Number\" to match the URL with \"\"Ebook Central::\"+match(cells[\"Ebook Central BIB URLs\"].value,/https:\\/\\/ebookcentral\\.proquest\\.com\\/lib\\/fsu\\/detail\\.action\\?docID=(\\d*)/)[0])\". Confirm that the record in question doesn't have replacement characters in any of the titles or that all of the titles have TKRs for other platforms; if they do, make the appropriate changes or removals now.")
# """[
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "HOL Number",
#           "expression": "value",
#           "columnName": "HOL Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "110102929",
#                 "l": "110102929"
#               }
#             },
#             {
#               "v": {
#                 "v": "108930129",
#                 "l": "108930129"
#               }
#             },
#             {
#               "v": {
#                 "v": "110016991",
#                 "l": "110016991"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "row-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::\"+match(cells[\"Ebook Central BIB URLs\"].value,/https:\\/\\/ebookcentral\\.proquest\\.com\\/lib\\/fsu\\/detail\\.action\\?docID=(\\d*)/)[0])",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::\"+match(cells[\"Ebook Central BIB URLs\"].value,/https:\\/\\/ebookcentral\\.proquest\\.com\\/lib\\/fsu\\/detail\\.action\\?docID=(\\d*)/)[0])"
#   }
# ]"""
# messagebox.showinfo(title="Instructions", message="Set text filter on \"Replacement Character in Title\" to true and edit the titles as needed to match the 245 fields in the BIBs of origin.")
# """[
#   {
#     "op": "core/mass-edit",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Replacement Character in Title",
#           "expression": "value",
#           "columnName": "Replacement Character in Title",
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
#     "columnName": "Title",
#     "expression": "value",
#     "edits": [
#       {
#         "from": [
#           "A Postcolonial Critique of the Linde et al. v. Arab Bank, PLC â€œTerrorismâ€� Bank Cases"
#         ],
#         "fromBlank": false,
#         "fromError": false,
#         "to": "A Postcolonial Critique of the Linde et al. v. Arab Bank, PLC \"Terrorism\" Bank Cases"
#       }
#     ],
#     "description": "Mass edit cells in column Title"
#   },
#   {
#     "op": "core/mass-edit",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Replacement Character in Title",
#           "expression": "value",
#           "columnName": "Replacement Character in Title",
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
#     "columnName": "Title",
#     "expression": "value",
#     "edits": [
#       {
#         "from": [
#           "Letters of a Sufi scholar: the correspondence of Ê»Abd al-GhanÄ« al-NÄ�bulusÄ« (1641-1731)"
#         ],
#         "fromBlank": false,
#         "fromError": false,
#         "to": "Letters of a Sufi scholar: the correspondence of ʻAbd al-Ghanī al-Nābulusī (1641-1731)"
#       }
#     ],
#     "description": "Mass edit cells in column Title"
#   },
#   {
#     "op": "core/mass-edit",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Replacement Character in Title",
#           "expression": "value",
#           "columnName": "Replacement Character in Title",
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
#     "columnName": "Title",
#     "expression": "value",
#     "edits": [
#       {
#         "from": [
#           "New Mexico and the PimeriÌ�a Alta: the colonial period in the American Southwest"
#         ],
#         "fromBlank": false,
#         "fromError": false,
#         "to": "New Mexico and the Pimería Alta: the colonial period in the American Southwest"
#       }
#     ],
#     "description": "Mass edit cells in column Title"
#   },
#   {
#     "op": "core/mass-edit",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Replacement Character in Title",
#           "expression": "value",
#           "columnName": "Replacement Character in Title",
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
#     "columnName": "Title",
#     "expression": "value",
#     "edits": [
#       {
#         "from": [
#           "â€œRomanticismâ€� â€“ and Byron. (ed=1st ed.)"
#         ],
#         "fromBlank": false,
#         "fromError": false,
#         "to": "“Romanticism” – and Byron. (ed=1st ed.)"
#       }
#     ],
#     "description": "Mass edit cells in column Title"
#   },
#   {
#     "op": "core/mass-edit",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Replacement Character in Title",
#           "expression": "value",
#           "columnName": "Replacement Character in Title",
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
#     "columnName": "Title",
#     "expression": "value",
#     "edits": [
#       {
#         "from": [
#           "Poetry, the geometry of the living substance: four essays on Ã�gnes Nemes Nagy"
#         ],
#         "fromBlank": false,
#         "fromError": false,
#         "to": "Poetry, the geometry of the living substance: four essays on Ágnes Nemes Nagy"
#       }
#     ],
#     "description": "Mass edit cells in column Title"
#   },
#   {
#     "op": "core/mass-edit",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Replacement Character in Title",
#           "expression": "value",
#           "columnName": "Replacement Character in Title",
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
#     "columnName": "Title",
#     "expression": "value",
#     "edits": [
#       {
#         "from": [
#           "Poetry, the Geometry of the Living Substance: Four Essays on Ã�gnes Nemes Nagy. (ed=1st ed.)"
#         ],
#         "fromBlank": false,
#         "fromError": false,
#         "to": "Poetry, the Geometry of the Living Substance: Four Essays on Ágnes Nemes Nagy. (ed=1st ed.)"
#       }
#     ],
#     "description": "Mass edit cells in column Title"
#   },
#   {
#     "op": "core/mass-edit",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Replacement Character in Title",
#           "expression": "value",
#           "columnName": "Replacement Character in Title",
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
#     "columnName": "Title",
#     "expression": "value",
#     "edits": [
#       {
#         "from": [
#           "HÅ�ryÅ«ji reconsidered: [HÅ�ryÅ«ji no saikeutÅ�]"
#         ],
#         "fromBlank": false,
#         "fromError": false,
#         "to": "Hōryūji reconsidered: [Hōryūji no saikeutō]"
#       }
#     ],
#     "description": "Mass edit cells in column Title"
#   },
# ]"""
# messagebox.showinfo(title="Instructions", message="Set filter for blanks on \"Record Number\" to true and crteate text filter on \"TKRs\" and \"Record Number\". For each value in the text filter on \"TKRs\", use filtering by \"Record Number\" to remove the records were all the rows have a tickler for another platform.")
# """[
#   {
#     "op": "core/row-removal",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "TKRs",
#           "expression": "value",
#           "columnName": "TKRs",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "CredoReference",
#                 "l": "CredoReference"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number",
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
#           "expression": "value",
#           "columnName": "Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "4947",
#                 "l": "4947"
#               }
#             },
#             {
#               "v": {
#                 "v": "8184",
#                 "l": "8184"
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
#           "name": "TKRs",
#           "expression": "value",
#           "columnName": "TKRs",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "Oxford Quick Reference",
#                 "l": "Oxford Quick Reference"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number",
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
#   },
#   {
#     "op": "core/row-removal",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "TKRs",
#           "expression": "value",
#           "columnName": "TKRs",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "Oxford Reference Premium",
#                 "l": "Oxford Reference Premium"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number",
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
#   },
#   {
#     "op": "core/row-removal",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "TKRs",
#           "expression": "value",
#           "columnName": "TKRs",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "SageResearchMethods",
#                 "l": "SageResearchMethods"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number",
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
#           "expression": "value",
#           "columnName": "Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "67",
#                 "l": "67"
#               }
#             },
#             {
#               "v": {
#                 "v": "8102",
#                 "l": "8102"
#               }
#             },
#             {
#               "v": {
#                 "v": "4650",
#                 "l": "4650"
#               }
#             },
#             {
#               "v": {
#                 "v": "382",
#                 "l": "382"
#               }
#             },
#             {
#               "v": {
#                 "v": "690",
#                 "l": "690"
#               }
#             },
#             {
#               "v": {
#                 "v": "692",
#                 "l": "692"
#               }
#             },
#             {
#               "v": {
#                 "v": "1866",
#                 "l": "1866"
#               }
#             },
#             {
#               "v": {
#                 "v": "693",
#                 "l": "693"
#               }
#             },
#             {
#               "v": {
#                 "v": "276",
#                 "l": "276"
#               }
#             },
#             {
#               "v": {
#                 "v": "157",
#                 "l": "157"
#               }
#             },
#             {
#               "v": {
#                 "v": "466",
#                 "l": "466"
#               }
#             },
#             {
#               "v": {
#                 "v": "104",
#                 "l": "104"
#               }
#             },
#             {
#               "v": {
#                 "v": "654",
#                 "l": "654"
#               }
#             },
#             {
#               "v": {
#                 "v": "567",
#                 "l": "567"
#               }
#             },
#             {
#               "v": {
#                 "v": "2189",
#                 "l": "2189"
#               }
#             },
#             {
#               "v": {
#                 "v": "338",
#                 "l": "338"
#               }
#             },
#             {
#               "v": {
#                 "v": "724",
#                 "l": "724"
#               }
#             },
#             {
#               "v": {
#                 "v": "725",
#                 "l": "725"
#               }
#             },
#             {
#               "v": {
#                 "v": "2707",
#                 "l": "2707"
#               }
#             },
#             {
#               "v": {
#                 "v": "803",
#                 "l": "803"
#               }
#             },
#             {
#               "v": {
#                 "v": "4207",
#                 "l": "4207"
#               }
#             },
#             {
#               "v": {
#                 "v": "11402",
#                 "l": "11402"
#               }
#             },
#             {
#               "v": {
#                 "v": "4649",
#                 "l": "4649"
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

# #Subsection: Determine Which HOL Records to Keep
# messagebox.showinfo(title="Instructions", message="Create spreadsheet \"Cross-Reference.xlsx\" with columns \"BIB with ACQ\" listing the BIBs with ACQ records attached and \"Ebook Central Owned\" with the Ebook Central IDs of the titles owned on that platform. The BIBs be nine-digit text strings, the IDs should be formatted as text.")
# #Alert: This should be replaced with file "BIB Checked for ACQ" which contains a list of the BIBs checked for ACQs and a Boolean indicating if the BIB has an ACQ; this list has also been updated to reflect moved ACQ records
# messagebox.showwarning(title="Deduping HOLs", message="HOLs with multiple non-unique record numbers have them combined in \"Record Number\" divided by pipes. This situation didn't acutally occur with these titles; there may be a better way to handle it.")
# # For records with 3+ rows, is rerunning "Duplication" against second row as way to see if all but first row match a viable idea?  
# os.startfile('Select_HOL_to_Keep_pt1--Ebook_Central_Specific.json')
# messagebox.showinfo(title="Instructions", message="Create custom filter on \"Record Number\" with \"toString(row.record.toRowIndex-row.record.fromRowIndex)\". Select each value greater than three and, for records where the values of \"Duplication\" are all the same, fill up and down those values.")
# messagebox.showinfo(title="Instructions", message="Create blanks filters on both \"Record Number\" and \"Duplication\" and set them to true. Change the values in \"Duplication\" for these records, using \"Multiple\" when some, but not all, of the HOL in a record have the same BIB or sublibrary.")
# """[
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Duplication",
#           "expression": "value",
#           "columnName": "Duplication",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [],
#           "selectBlank": true,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number",
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
#           "expression": "value",
#           "columnName": "Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "Ebook Central::438603",
#                 "l": "Ebook Central::438603"
#               }
#             },
#             {
#               "v": {
#                 "v": "Ebook Central::1168042",
#                 "l": "Ebook Central::1168042"
#               }
#             },
#             {
#               "v": {
#                 "v": "Ebook Central::647437",
#                 "l": "Ebook Central::647437"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Duplication",
#     "expression": "grel:\"Different BIB, Multiple Sublibrary\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Duplication using expression grel:\"Different BIB, Multiple Sublibrary\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Duplication",
#           "expression": "value",
#           "columnName": "Duplication",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [],
#           "selectBlank": true,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number",
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
#           "expression": "value",
#           "columnName": "Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "Ebook Central::224643",
#                 "l": "Ebook Central::224643"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Duplication",
#     "expression": "grel:\"Multiple BIB, Different Sublibrary\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Duplication using expression grel:\"Multiple BIB, Different Sublibrary\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Duplication",
#           "expression": "value",
#           "columnName": "Duplication",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [],
#           "selectBlank": true,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number",
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
#           "expression": "value",
#           "columnName": "Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "Ebook Central::180253",
#                 "l": "Ebook Central::180253"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Duplication",
#     "expression": "grel:\"Multiple BIB, Same Sublibrary\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Duplication using expression grel:\"Multiple BIB, Same Sublibrary\""
#   }
# ]"""
# messagebox.showwarning(title="Changing \"Record Number\"", message="A method for updating \"Record Number\" for those records changed in the previous step needs to be developed. With Ebook Central, all of the records requiring changes had Ebook Central IDs.")
# messagebox.showinfo(title="Instructions", message="Remove the blanks filter on \"Duplication\". Create text filter on \"HOL Sublibrary\" and select all values but \"FSUER\", then invert. Use \"Transform...\" to change the value of the matching records to \"Only FSUER HOL\".")
# """[
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number",
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
#           "name": "HOL Sublibrary",
#           "expression": "value",
#           "columnName": "HOL Sublibrary",
#           "invert": true,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "FSOAR",
#                 "l": "FSOAR"
#               }
#             },
#             {
#               "v": {
#                 "v": "FSLAW",
#                 "l": "FSLAW"
#               }
#             },
#             {
#               "v": {
#                 "v": "FSUDC",
#                 "l": "FSUDC"
#               }
#             },
#             {
#               "v": {
#                 "v": "FSUPA",
#                 "l": "FSUPA"
#               }
#             },
#             {
#               "v": {
#                 "v": "FSUSC",
#                 "l": "FSUSC"
#               }
#             },
#             {
#               "v": {
#                 "v": "FSUPC",
#                 "l": "FSUPC"
#               }
#             },
#             {
#               "v": {
#                 "v": "FSULN",
#                 "l": "FSULN"
#               }
#             },
#             {
#               "v": {
#                 "v": "FSULC",
#                 "l": "FSULC"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "FSUER HOL",
#     "expression": "grel:\"Only FSUER HOL\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column FSUER HOL using expression grel:\"Only FSUER HOL\""
#   }
# ]"""
# # "Record Number" formats
# ## Ebook Central::<Ebook Central ID> = title matched to an Ebook Central ID
# ## HOL <HOL Number> without ID = HOL is only one for that title
# ## Duplicate <sublibrary code> Sublibrary for BIB <BIB number> = multiple HOLs for same sublibrary on same BIB record found (thoretically, shouldn't be possible) {Same BIB, Same Sublibrary}
# ## BIBs <list of BIB numbers> Match = HOLs for the same sublibrary found on multiple BIB records {Different BIB, Same Sublibrary}
# ## Different Sublibraries for BIB <BIB Number> = HOLs found on same BIB record but for different sublibraries {Same BIB, Different Sublibrary}
# ## BIBs <list of BIB numbers> Match with Different Sublibraries = HOLs for different sublibraries found on different BIB records {Different BIB, Different Sublibrary}
# os.startfile('Select_HOL_to_Keep_pt2--Ebook_Central_Specific.json')
# messagebox.showwarning(title="Removing HOL No Longer in UXU60", message="Some BIB records were found to have multiple HOL from the same sublibrary attached. At this point, I removed those HOL that were no longer in UXU60.")
# """[
#   {
#     "op": "core/fill-down",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "HOL Number",
#           "expression": "grel:or(value==\"110963622\",value==\"110962989\",value==\"110962835\",value==\"108380908\",value==\"105905887\",value==\"110965288\",value==\"110962994\",value==\"110963861\")",
#           "columnName": "HOL Number",
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
#     "columnName": "Record Number",
#     "description": "Fill down cells in column Record Number"
#   },
#   {
#     "op": "core/row-removal",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "HOL Number",
#           "expression": "grel:or(value==\"110963622\",value==\"110962989\",value==\"110962835\",value==\"108380908\",value==\"105905887\",value==\"110965288\",value==\"110962994\",value==\"110963861\")",
#           "columnName": "HOL Number",
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
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Duplication",
#           "expression": "isBlank(value)",
#           "columnName": "Duplication",
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
#           "expression": "grel:toString(row.record.toRowIndex-row.record.fromRowIndex)",
#           "columnName": "Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "1",
#                 "l": "1"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Keep HOL?",
#     "expression": "grel:if(cells[\"Has ACQ?\"].value==\"BIB has ACQ\",\"TRUE: FSUER HOL with ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"),\"TRUE: FSUER HOL for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"))",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Keep HOL? using expression grel:if(cells[\"Has ACQ?\"].value==\"BIB has ACQ\",\"TRUE: FSUER HOL with ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"),\"TRUE: FSUER HOL for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"))"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Duplication",
#           "expression": "value",
#           "columnName": "Duplication",
#           "invert": true,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [],
#           "selectBlank": true,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "Record Number",
#           "expression": "grel:toString(row.record.toRowIndex-row.record.fromRowIndex)",
#           "columnName": "Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "1",
#                 "l": "1"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Duplication",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Duplication using expression null"
#   }
# ]"""
# messagebox.showinfo(title="Instructions", message="Set blanks filter on \"Keep HOL?\" to true. Filter \"FSUER HOL\" to blanks. In this case, we had access to none of those titles on the Ebook Central platform as perpetual access entitlements, so the records were removed.")
# """[
#   {
#     "op": "core/row-removal",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Record Number",
#           "expression": "isBlank(value)",
#           "columnName": "Record Number",
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
#           "name": "FSUER HOL",
#           "expression": "value",
#           "columnName": "FSUER HOL",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [],
#           "selectBlank": true,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "Keep HOL?",
#           "expression": "isBlank(value)",
#           "columnName": "Keep HOL?",
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
# messagebox.showinfo(title="Instructions", message="Keep blanks filters on \"Keep HOL?\" to true. Filter \"Duplication\" to \"Same BIB, Different Sublibrary\" and investigate. In this case, we had access to none of those titles on the Ebook Central platform as perpetual access entitlements, so the records were removed.")
# """[
#   {
#     "op": "core/row-removal",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Keep HOL?",
#           "expression": "isBlank(value)",
#           "columnName": "Keep HOL?",
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
#           "name": "Duplication",
#           "expression": "value",
#           "columnName": "Duplication",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "Same BIB, Different Sublibrary",
#                 "l": "Same BIB, Different Sublibrary"
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
# messagebox.showinfo(title="Instructions", message="Keep blanks filters on \"Keep HOL?\" to true. Evaluate the remaining matching records, determining which HOLs in a record should be kept and changing the value of \"Keep HOL?\" as appropriate For records representing titles that aren't perpetual access entitlements in Ebook Central, remove them.")
# # "Keep HOL?" Formats
# ## Only HOL for record = TRUE: Only HOL for ID <Ebook Central ID> | TRUE: Only HOL for Title [HOL <HOL number>]
# ## FSUER HOL with ACQ being kept = TRUE: FSUER HOL with ACQ for <Ebook Central ID | "Title">
# ## FSUER HOL with ACQ not being kept = FALSE: FSUER HOL with ACQ for <Ebook Central ID | "Title">
# ## FSUER HOL without ACQ to be kept = TRUE: FSUER HOL for <Ebook Central ID | "Title">
# ## FSUER HOL without ACQ not being kept = FALSE: FSUER HOL without ACQ for <Ebook Central ID | "Title">
# ## FSUER HOL believed to have been loaded for URL = FALSE: Probably Loaded for URL for <Ebook Central ID | "Title">
# ## FSUER HOL in record with other HOL/BIBs believed to have been loaded for URL = TRUE: Other FSUER HOL for <Ebook Central ID | "Title"> Probably Loaded for URL
# ## Other sublibrary HOL with ACQ = N/A: Other Sublibrary with ACQ HOL for <Ebook Central ID | "Title">
# ## Other sublibrary HOL without ACQ = N/A: Other Sublibrary HOL for <Ebook Central ID | "Title">
# ## FSUER HOL with ACQ for non-Ebook Central BIB = N/A: Non-Ebook Central Holding with ACQ for <Ebook Central ID | "Title">
# ## FSUER HOL without ACQ for non-Ebook Central BIB = N/A: Non-Ebook Central Holding for <Ebook Central ID | "Title">
# """[
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Keep HOL?",
#           "expression": "isBlank(value)",
#           "columnName": "Keep HOL?",
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
#           "expression": "value",
#           "columnName": "Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "Ebook Central::807421",
#                 "l": "Ebook Central::807421"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Keep HOL?",
#     "expression": "grel:if(cells[\"HOL Number\"].value==\"078299741\",\"TRUE: FSUER HOL for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"),\"FALSE: FSUER HOL without ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"))",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Keep HOL? using expression grel:if(cells[\"HOL Number\"].value==\"078299741\",\"TRUE: FSUER HOL for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"),\"FALSE: FSUER HOL without ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"))"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Keep HOL?",
#           "expression": "isBlank(value)",
#           "columnName": "Keep HOL?",
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
#           "expression": "value",
#           "columnName": "Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "Ebook Central::775000",
#                 "l": "Ebook Central::775000"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "ACQ Test",
#           "expression": "grel:contains(value,\"BIB has ACQ\")",
#           "columnName": "ACQ Test",
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
#     "columnName": "Keep HOL?",
#     "expression": "grel:if(cells[\"HOL Number\"].value==\"078298792\",\"TRUE: FSUER HOL for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"),\"FALSE: FSUER HOL without ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"))",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Keep HOL? using expression grel:if(cells[\"HOL Number\"].value==\"078298792\",\"TRUE: FSUER HOL for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"),\"FALSE: FSUER HOL without ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"))"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Keep HOL?",
#           "expression": "isBlank(value)",
#           "columnName": "Keep HOL?",
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
#           "expression": "value",
#           "columnName": "Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "Ebook Central::775061",
#                 "l": "Ebook Central::775061"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "ACQ Test",
#           "expression": "grel:contains(value,\"BIB has ACQ\")",
#           "columnName": "ACQ Test",
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
#     "columnName": "Keep HOL?",
#     "expression": "grel:if(cells[\"HOL Number\"].value==\"078298975\",\"TRUE: FSUER HOL for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"),\"FALSE: FSUER HOL without ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"))",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Keep HOL? using expression grel:if(cells[\"HOL Number\"].value==\"078298975\",\"TRUE: FSUER HOL for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"),\"FALSE: FSUER HOL without ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"))"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Keep HOL?",
#           "expression": "isBlank(value)",
#           "columnName": "Keep HOL?",
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
#           "expression": "value",
#           "columnName": "Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "Ebook Central::775143",
#                 "l": "Ebook Central::775143"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "ACQ Test",
#           "expression": "grel:contains(value,\"BIB has ACQ\")",
#           "columnName": "ACQ Test",
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
#     "columnName": "Keep HOL?",
#     "expression": "grel:if(cells[\"HOL Number\"].value==\"078298825\",\"TRUE: FSUER HOL for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"),\"FALSE: FSUER HOL without ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"))",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Keep HOL? using expression grel:if(cells[\"HOL Number\"].value==\"078298825\",\"TRUE: FSUER HOL for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"),\"FALSE: FSUER HOL without ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"))"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Keep HOL?",
#           "expression": "isBlank(value)",
#           "columnName": "Keep HOL?",
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
#           "expression": "value",
#           "columnName": "Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "Ebook Central::803163",
#                 "l": "Ebook Central::803163"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "ACQ Test",
#           "expression": "grel:contains(value,\"BIB has ACQ\")",
#           "columnName": "ACQ Test",
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
#     "columnName": "Keep HOL?",
#     "expression": "grel:if(cells[\"HOL Number\"].value==\"078299611\",\"TRUE: FSUER HOL for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"),\"FALSE: FSUER HOL without ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"))",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Keep HOL? using expression grel:if(cells[\"HOL Number\"].value==\"078299611\",\"TRUE: FSUER HOL for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"),\"FALSE: FSUER HOL without ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"))"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Keep HOL?",
#           "expression": "isBlank(value)",
#           "columnName": "Keep HOL?",
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
#           "expression": "value",
#           "columnName": "Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "Ebook Central::807218",
#                 "l": "Ebook Central::807218"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "ACQ Test",
#           "expression": "grel:contains(value,\"BIB has ACQ\")",
#           "columnName": "ACQ Test",
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
#     "columnName": "Keep HOL?",
#     "expression": "grel:if(cells[\"HOL Number\"].value==\"078305768\",\"TRUE: FSUER HOL for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"),\"FALSE: FSUER HOL without ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"))",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Keep HOL? using expression grel:if(cells[\"HOL Number\"].value==\"078305768\",\"TRUE: FSUER HOL for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"),\"FALSE: FSUER HOL without ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"))"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Keep HOL?",
#           "expression": "isBlank(value)",
#           "columnName": "Keep HOL?",
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
#           "expression": "value",
#           "columnName": "Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "Ebook Central::833386",
#                 "l": "Ebook Central::833386"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         },
#         {
#           "type": "list",
#           "name": "ACQ Test",
#           "expression": "grel:contains(value,\"BIB has ACQ\")",
#           "columnName": "ACQ Test",
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
#     "columnName": "Keep HOL?",
#     "expression": "grel:if(cells[\"HOL Number\"].value==\"078399656\",\"TRUE: FSUER HOL for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"),\"FALSE: FSUER HOL without ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"))",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Keep HOL? using expression grel:if(cells[\"HOL Number\"].value==\"078399656\",\"TRUE: FSUER HOL for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"),\"FALSE: FSUER HOL without ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"))"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Keep HOL?",
#           "expression": "isBlank(value)",
#           "columnName": "Keep HOL?",
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
#           "expression": "value",
#           "columnName": "Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "Ebook Central::3413974",
#                 "l": "Ebook Central::3413974"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Keep HOL?",
#     "expression": "grel:if(cells[\"HOL Number\"].value==\"100637045\",\"TRUE: FSUER HOL for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"),if(cells[\"HOL Number\"].value==\"109803232\",\"FALSE: FSUER HOL without ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"),\"N/A: Other Sublibrary with ACQ HOL for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\")))",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Keep HOL? using expression grel:if(cells[\"HOL Number\"].value==\"100637045\",\"TRUE: FSUER HOL for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"),if(cells[\"HOL Number\"].value==\"109803232\",\"FALSE: FSUER HOL without ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"),\"N/A: Other Sublibrary with ACQ HOL for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\")))"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Keep HOL?",
#           "expression": "isBlank(value)",
#           "columnName": "Keep HOL?",
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
#           "expression": "value",
#           "columnName": "Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "Ebook Central::1636475",
#                 "l": "Ebook Central::1636475"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Keep HOL?",
#     "expression": "grel:if(cells[\"HOL Number\"].value==\"102834458\",\"TRUE: FSUER HOL with ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"),if(cells[\"HOL Number\"].value==\"102774020\",\"FALSE: FSUER HOL with ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"),\"FALSE: Probably Loaded for URL for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\")))",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Keep HOL? using expression grel:if(cells[\"HOL Number\"].value==\"102834458\",\"TRUE: FSUER HOL with ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"),if(cells[\"HOL Number\"].value==\"102774020\",\"FALSE: FSUER HOL with ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"),\"FALSE: Probably Loaded for URL for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\")))"
#   },
#   {
#     "op": "core/fill-down",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Title",
#           "expression": "grel:contains(value,\"Key writers on art\")",
#           "columnName": "Title",
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
#     "columnName": "Record Number",
#     "description": "Fill down cells in column Record Number"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Title",
#           "expression": "grel:contains(value,\"Key writers on art\")",
#           "columnName": "Title",
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
#     "columnName": "Record Number",
#     "expression": "grel:if(cells[\"BIB Number\"].value==\"032080848\",\"Ebook Central::240426\",value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:if(cells[\"BIB Number\"].value==\"032080848\",\"Ebook Central::240426\",value)"
#   },
#   {
#     "op": "core/blank-down",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Title",
#           "expression": "grel:contains(value,\"Key writers on art\")",
#           "columnName": "Title",
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
#       "mode": "row-based"
#     },
#     "columnName": "Record Number",
#     "description": "Blank down cells in column Record Number"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Title",
#           "expression": "grel:contains(value,\"Key writers on art\")",
#           "columnName": "Title",
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
#     "columnName": "FSUER HOL",
#     "expression": "grel:\"Only FSUER HOL\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column FSUER HOL using expression grel:\"Only FSUER HOL\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Title",
#           "expression": "grel:contains(value,\"Key writers on art\")",
#           "columnName": "Title",
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
#     "columnName": "Duplication",
#     "expression": "grel:\"Different BIB, Same Sublibrary\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Duplication using expression grel:\"Different BIB, Same Sublibrary\""
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Title",
#           "expression": "grel:contains(value,\"Key writers on art\")",
#           "columnName": "Title",
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
#     "columnName": "ACQ Test",
#     "expression": "grel:cells[\"Has ACQ?\"].value",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column ACQ Test using expression grel:cells[\"Has ACQ?\"].value"
#   },
#   {
#     "op": "core/multivalued-cell-join",
#     "columnName": "ACQ Test",
#     "keyColumnName": "Record Number",
#     "separator": "|",
#     "description": "Join multi-valued cells in column ACQ Test"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Title",
#           "expression": "grel:contains(value,\"Key writers on art\")",
#           "columnName": "Title",
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
#     "columnName": "Keep HOL?",
#     "expression": "grel:if(cells[\"Has ACQ?\"].value==\"BIB has ACQ\",\"TRUE: FSUER HOL with ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"),if(cells[\"Has ACQ?\"].value==\"No ACQ for BIB\",\"FALSE: FSUER HOL without ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"),\"ERROR\"))",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Keep HOL? using expression grel:if(cells[\"Has ACQ?\"].value==\"BIB has ACQ\",\"TRUE: FSUER HOL with ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"),if(cells[\"Has ACQ?\"].value==\"No ACQ for BIB\",\"FALSE: FSUER HOL without ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"),\"ERROR\"))"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Keep HOL?",
#           "expression": "isBlank(value)",
#           "columnName": "Keep HOL?",
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
#           "expression": "value",
#           "columnName": "Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "Ebook Central::3115036",
#                 "l": "Ebook Central::3115036"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Keep HOL?",
#     "expression": "grel:if(cells[\"HOL Number\"].value==\"108522833\",\"TRUE: FSUER HOL with ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"),\"FALSE: FSUER HOL with ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"))",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Keep HOL? using expression grel:if(cells[\"HOL Number\"].value==\"108522833\",\"TRUE: FSUER HOL with ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"),\"FALSE: FSUER HOL with ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"))"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Keep HOL?",
#           "expression": "isBlank(value)",
#           "columnName": "Keep HOL?",
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
#           "expression": "value",
#           "columnName": "Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "Ebook Central::4863103",
#                 "l": "Ebook Central::4863103"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Keep HOL?",
#     "expression": "grel:if(cells[\"HOL Number\"].value==\"108522887\",\"TRUE: FSUER HOL with ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"),\"FALSE: FSUER HOL with ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"))",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Keep HOL? using expression grel:if(cells[\"HOL Number\"].value==\"108522887\",\"TRUE: FSUER HOL with ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"),\"FALSE: FSUER HOL with ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"))"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Keep HOL?",
#           "expression": "isBlank(value)",
#           "columnName": "Keep HOL?",
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
#           "expression": "value",
#           "columnName": "Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "Ebook Central::4942173",
#                 "l": "Ebook Central::4942173"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Keep HOL?",
#     "expression": "grel:if(cells[\"HOL Number\"].value==\"108522917\",\"TRUE: FSUER HOL with ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"),\"FALSE: FSUER HOL with ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"))",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Keep HOL? using expression grel:if(cells[\"HOL Number\"].value==\"108522917\",\"TRUE: FSUER HOL with ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"),\"FALSE: FSUER HOL with ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"))"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
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
#                 "v": "Ebook Central::1769040",
#                 "l": "Ebook Central::1769040"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Keep HOL?",
#     "expression": "null",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Keep HOL? using expression null"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Keep HOL?",
#           "expression": "isBlank(value)",
#           "columnName": "Keep HOL?",
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
#           "expression": "value",
#           "columnName": "Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "Ebook Central::1650574",
#                 "l": "Ebook Central::1650574"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Keep HOL?",
#     "expression": "grel:if(cells[\"HOL Number\"].value==\"108356271\",\"TRUE: FSUER HOL with ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"),\"FALSE: FSUER HOL with ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"))",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Keep HOL? using expression grel:if(cells[\"HOL Number\"].value==\"108356271\",\"TRUE: FSUER HOL with ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"),\"FALSE: FSUER HOL with ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"))"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Keep HOL?",
#           "expression": "isBlank(value)",
#           "columnName": "Keep HOL?",
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
#           "expression": "value",
#           "columnName": "Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "Ebook Central::3570368",
#                 "l": "Ebook Central::3570368"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Keep HOL?",
#     "expression": "grel:if(cells[\"HOL Number\"].value==\"102758835\",\"TRUE: FSUER HOL with ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"),\"FALSE: FSUER HOL with ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"))",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Keep HOL? using expression grel:if(cells[\"HOL Number\"].value==\"102758835\",\"TRUE: FSUER HOL with ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"),\"FALSE: FSUER HOL with ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"))"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Keep HOL?",
#           "expression": "isBlank(value)",
#           "columnName": "Keep HOL?",
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
#     "columnName": "Has ACQ?",
#     "expression": "grel:if(cells[\"BIB Number\"].value==\"036810110\",\"No ACQ for BIB\",value)",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Has ACQ? using expression grel:if(cells[\"BIB Number\"].value==\"036810110\",\"No ACQ for BIB\",value)"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "BIB Number",
#           "expression": "grel:or(value==\"036810112\",value==\"036810110\",value==\"037228798\")",
#           "columnName": "BIB Number",
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
#       "mode": "row-based"
#     },
#     "columnName": "Record Number",
#     "expression": "grel:\"Ebook Central::1769040\"",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::1769040\""
#   },
#   {
#     "op": "core/row-reorder",
#     "mode": "record-based",
#     "sorting": {
#       "criteria": [
#         {
#           "valueType": "string",
#           "column": "Record Number",
#           "blankPosition": 2,
#           "errorPosition": 1,
#           "reverse": false,
#           "caseSensitive": false
#         }
#       ]
#     },
#     "description": "Reorder rows"
#   },
#   {
#     "op": "core/blank-down",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Keep HOL?",
#           "expression": "isBlank(value)",
#           "columnName": "Keep HOL?",
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
#       "mode": "row-based"
#     },
#     "columnName": "Record Number",
#     "description": "Blank down cells in column Record Number"
#   },
#   {
#     "op": "core/text-transform",
#     "engineConfig": {
#       "facets": [
#         {
#           "type": "list",
#           "name": "Keep HOL?",
#           "expression": "isBlank(value)",
#           "columnName": "Keep HOL?",
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
#           "expression": "value",
#           "columnName": "Record Number",
#           "invert": false,
#           "omitBlank": false,
#           "omitError": false,
#           "selection": [
#             {
#               "v": {
#                 "v": "Ebook Central::1769040",
#                 "l": "Ebook Central::1769040"
#               }
#             }
#           ],
#           "selectBlank": false,
#           "selectError": false
#         }
#       ],
#       "mode": "record-based"
#     },
#     "columnName": "Keep HOL?",
#     "expression": "grel:if(cells[\"HOL Number\"].value==\"108930129\",\"TRUE: FSUER HOL with ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"),\"FALSE: FSUER HOL without ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"))",
#     "onError": "keep-original",
#     "repeat": false,
#     "repeatCount": 10,
#     "description": "Text transform on cells in column Keep HOL? using expression grel:if(cells[\"HOL Number\"].value==\"108930129\",\"TRUE: FSUER HOL with ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"),\"FALSE: FSUER HOL without ACQ for \"+if(contains(row.record.cells[\"Record Number\"].value[0],\"::\"),\"ID \"+substring(row.record.cells[\"Record Number\"].value[0],indexOf(row.record.cells[\"Record Number\"].value[0],\"::\")+2),\"Title\"))"
#   }
# ]"""

# # Ebook Central::371984 purchased on two platforms later migrated to Ebook Central


# #Section: Create Update Files For Records to Remain
# #Subsection: Identify Perpetual Access Entitlements
# os.startfile('Identify_Perpetual_Access_Entitlements_pt1--Ebook_Central_Specific.json')
# messagebox.showinfo(title="Instructions", message="Generate a list of the propriatrary IDs and titles for all perpetual access entitlements where the IDs are in the column \"ID\" and the titles are in the column \"Title\". Save as a CSV named \"Entitlements\" and upload to OpenRefine.")
# messagebox.showinfo(title="Instructions", message="Apply the following JSON in the \"Entitlements csv\" project.")
# os.startfile('Identify_Perpetual_Access_Entitlements_pt2--Ebook_Central_Specific.json')

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
