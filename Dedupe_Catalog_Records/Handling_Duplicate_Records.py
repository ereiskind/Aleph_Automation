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
messagebox.showwarning(title="Ebook Central", message="Following instructions are very specific to Ebook Central.")
messagebox.showinfo(title="Instructions", message="Download the OpenRefine project into Excel. Dedupe \"ISBN 1\" and copy into LibCentral's title match feature. Save the ISBN and ID columns from the title match output as \"ISBNs and eBook Central IDs.xlsx\". Upload the worksheet into OpenRefine, removing the file extension from the project name.")

#Subsection: Organize UXU01 Output
messagebox.showinfo(title="Instructions", message="Load Aleph Sequential file with UXU01 info into OpenRefine with column widths 10, 6, 2. Name the project \"UXU01_Cleanup\".")
messagebox.showwarning(title="Creating Title", message="The step to create the title column won't work unless there's a 245$a, 245$b, 245$n, and 250$a column. There's a column reorder in the JSON that calls for all four columns.")
messagebox.showwarning(title="Ebook Central", message="The following JSON is for Ebook Central--the domain search regexes are hard coded. On a related note, any URLs from those domains not fitting the regexes are excluded.")
messagebox.showwarning(title="Credo", message="Credo IDs that are only letters don't get transfered to the \"001 ID\" column.")
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
messagebox.showinfo(title="Instructions", message="Perform clustering on column \"URL Domain\" to change domain names into the platforms they represent. \"Change_Domain_Names_to_Platform_Names.json\" can help with this.")
"""[
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "URL Domain",
    "expression": "value",
    "edits": [
      {
        "from": [
          "ebookcentral.proquest.com"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Ebook Central"
      }
    ],
    "description": "Mass edit cells in column URL Domain"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "URL Domain",
    "expression": "value",
    "edits": [
      {
        "from": [
          "lib.myilibrary.com"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "MyiLibrary"
      }
    ],
    "description": "Mass edit cells in column URL Domain"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "URL Domain",
    "expression": "value",
    "edits": [
      {
        "from": [
          "site.ebrary.com"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Ebrary"
      }
    ],
    "description": "Mass edit cells in column URL Domain"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "URL Domain",
    "expression": "value",
    "edits": [
      {
        "from": [
          "ucf.eblib.com"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Ebook Library"
      }
    ],
    "description": "Mass edit cells in column URL Domain"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "URL Domain",
    "expression": "value",
    "edits": [
      {
        "from": [
          "www.myilibrary.com"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "MyiLibrary"
      }
    ],
    "description": "Mass edit cells in column URL Domain"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "URL Domain",
    "expression": "value",
    "edits": [
      {
        "from": [
          "dx.doi.org"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "DOI"
      }
    ],
    "description": "Mass edit cells in column URL Domain"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "URL Domain",
    "expression": "value",
    "edits": [
      {
        "from": [
          "doi.org"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "DOI"
      }
    ],
    "description": "Mass edit cells in column URL Domain"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "URL Domain",
    "expression": "value",
    "edits": [
      {
        "from": [
          "fgcu.eblib.com"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Ebook Library"
      }
    ],
    "description": "Mass edit cells in column URL Domain"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "URL Domain",
    "expression": "value",
    "edits": [
      {
        "from": [
          "fsu.eblib.com"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Ebook Library"
      }
    ],
    "description": "Mass edit cells in column URL Domain"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "URL Domain",
    "expression": "value",
    "edits": [
      {
        "from": [
          "public.eblib.com"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Ebook Library"
      }
    ],
    "description": "Mass edit cells in column URL Domain"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "URL Domain",
    "expression": "value",
    "edits": [
      {
        "from": [
          "usf.eblib.com"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Ebook Library"
      }
    ],
    "description": "Mass edit cells in column URL Domain"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "URL Domain",
    "expression": "value",
    "edits": [
      {
        "from": [
          "www.famu.eblib.com"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Ebook Library"
      }
    ],
    "description": "Mass edit cells in column URL Domain"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "URL Domain",
    "expression": "value",
    "edits": [
      {
        "from": [
          "www.FIU.eblib.com"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Ebook Library"
      }
    ],
    "description": "Mass edit cells in column URL Domain"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "URL Domain",
    "expression": "value",
    "edits": [
      {
        "from": [
          "www.fsu.eblib.com"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Ebook Library"
      }
    ],
    "description": "Mass edit cells in column URL Domain"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "URL Domain",
    "expression": "value",
    "edits": [
      {
        "from": [
          "www.ucf.eblib.com"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Ebook Library"
      }
    ],
    "description": "Mass edit cells in column URL Domain"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "URL Domain",
    "expression": "value",
    "edits": [
      {
        "from": [
          "www.UCF.eblib.com"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Ebook Library"
      }
    ],
    "description": "Mass edit cells in column URL Domain"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "URL Domain",
    "expression": "value",
    "edits": [
      {
        "from": [
          "www.UFL.eblib.com"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Ebook Library"
      }
    ],
    "description": "Mass edit cells in column URL Domain"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "URL Domain",
    "expression": "value",
    "edits": [
      {
        "from": [
          "www.usf.eblib.com"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Ebook Library"
      }
    ],
    "description": "Mass edit cells in column URL Domain"
  }
]"""
messagebox.showwarning(title="Regex Only URLs", message="The only URLs pulled out for their IDs are the ones that match the regexes.")
messagebox.showinfo(title="Instructions", message="Use text facets to change the values in \"001 ID Source\" and \"Unofficial 001 ID Source\" into the names of the platforms/sources they represent. \"Change_001_Source_Abbreviations.json\" can help with this.")
"""[
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "001 ID Source",
    "expression": "value",
    "edits": [
      {
        "from": [
          "Au-PeEL"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Ebook Library"
      }
    ],
    "description": "Mass edit cells in column 001 ID Source"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "001 ID Source",
    "expression": "value",
    "edits": [
      {
        "from": [
          "CaONFJC"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "MyiLibrary"
      }
    ],
    "description": "Mass edit cells in column 001 ID Source"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "001 ID Source",
    "expression": "value",
    "edits": [
      {
        "from": [
          "CaPaEBR"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Ebrary"
      }
    ],
    "description": "Mass edit cells in column 001 ID Source"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "001 ID Source",
    "expression": "value",
    "edits": [
      {
        "from": [
          "DE-He213"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Springer-Verlag"
      }
    ],
    "description": "Mass edit cells in column 001 ID Source"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "001 ID Source",
    "expression": "value",
    "edits": [
      {
        "from": [
          "MiAaPQ"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ProQuest"
      }
    ],
    "description": "Mass edit cells in column 001 ID Source"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "001 ID Source",
    "expression": "value",
    "edits": [
      {
        "from": [
          "NhCcYBP"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "YBP"
      }
    ],
    "description": "Mass edit cells in column 001 ID Source"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "001 ID Source",
    "expression": "value",
    "edits": [
      {
        "from": [
          "OCoLC"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "OCLC"
      }
    ],
    "description": "Mass edit cells in column 001 ID Source"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "001 ID Source",
    "expression": "value",
    "edits": [
      {
        "from": [
          "SFPDA_MiAaPQ"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ProQuest"
      }
    ],
    "description": "Mass edit cells in column 001 ID Source"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "001 ID Source",
    "expression": "value",
    "edits": [
      {
        "from": [
          "YBPUID"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "YBP"
      }
    ],
    "description": "Mass edit cells in column 001 ID Source"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "Unofficial 001 ID Source",
    "expression": "value",
    "edits": [
      {
        "from": [
          "MIL"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "MyiLibrary"
      }
    ],
    "description": "Mass edit cells in column Unofficial 001 ID Source"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "Unofficial 001 ID Source",
    "expression": "value",
    "edits": [
      {
        "from": [
          "EBR"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Ebrary"
      }
    ],
    "description": "Mass edit cells in column Unofficial 001 ID Source"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "Unofficial 001 ID Source",
    "expression": "value",
    "edits": [
      {
        "from": [
          "EBL"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Ebook Library"
      }
    ],
    "description": "Mass edit cells in column Unofficial 001 ID Source"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "Unofficial 001 ID Source",
    "expression": "value",
    "edits": [
      {
        "from": [
          "EBC"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Ebook Central"
      }
    ],
    "description": "Mass edit cells in column Unofficial 001 ID Source"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "001 ID Source",
    "expression": "value",
    "edits": [
      {
        "from": [
          "AU-PeEL"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Ebook Library"
      }
    ],
    "description": "Mass edit cells in column 001 ID Source"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "001 ID Source",
    "expression": "value",
    "edits": [
      {
        "from": [
          "CaBNVSL"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "SIAM"
      }
    ],
    "description": "Mass edit cells in column 001 ID Source"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "001 ID Source",
    "expression": "value",
    "edits": [
      {
        "from": [
          "CaBNvSL"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "SIAM"
      }
    ],
    "description": "Mass edit cells in column 001 ID Source"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "001 ID Source",
    "expression": "value",
    "edits": [
      {
        "from": [
          "DcWaAPA"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "APA"
      }
    ],
    "description": "Mass edit cells in column 001 ID Source"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "001 ID Source",
    "expression": "value",
    "edits": [
      {
        "from": [
          "DNLM"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "US Med Library"
      }
    ],
    "description": "Mass edit cells in column 001 ID Source"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "001 ID Source",
    "expression": "value",
    "edits": [
      {
        "from": [
          "FANhCcYBP"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "YBP"
      }
    ],
    "description": "Mass edit cells in column 001 ID Source"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "001 ID Source",
    "expression": "value",
    "edits": [
      {
        "from": [
          "FR-PaOEC"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "OECD"
      }
    ],
    "description": "Mass edit cells in column 001 ID Source"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "001 ID Source",
    "expression": "value",
    "edits": [
      {
        "from": [
          "IN-ChSCO"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Scope e-Knowedge Center"
      }
    ],
    "description": "Mass edit cells in column 001 ID Source"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "001 ID Source",
    "expression": "value",
    "edits": [
      {
        "from": [
          "MiFhGG"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Gale"
      }
    ],
    "description": "Mass edit cells in column 001 ID Source"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "001 ID Source",
    "expression": "value",
    "edits": [
      {
        "from": [
          "StDuBDS"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Bibliographic Data Services"
      }
    ],
    "description": "Mass edit cells in column 001 ID Source"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "001 ID Source",
    "expression": "value",
    "edits": [
      {
        "from": [
          "UtOrBLW"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Backstage Library Works"
      }
    ],
    "description": "Mass edit cells in column 001 ID Source"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "001 ID Source",
    "expression": "value",
    "edits": [
      {
        "from": [
          "VaAlASP"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Alexander Street Press"
      }
    ],
    "description": "Mass edit cells in column 001 ID Source"
  },
  {
    "op": "core/row-removal",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "001 ID Source",
          "expression": "value",
          "columnName": "001 ID Source",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "FU",
                "l": "FU"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "description": "Remove rows"
  },
  {
    "op": "core/row-removal",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "001 ID Source",
          "expression": "value",
          "columnName": "001 ID Source",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "FTS",
                "l": "FTS"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "description": "Remove rows"
  },
  {
    "op": "core/row-removal",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "001 ID Source",
          "expression": "value",
          "columnName": "001 ID Source",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "FIOLAS",
                "l": "FIOLAS"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "description": "Remove rows"
  },
  {
    "op": "core/row-removal",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "001 ID Source",
          "expression": "value",
          "columnName": "001 ID Source",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "CEL",
                "l": "CEL"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "description": "Remove rows"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Unofficial 001 ID Source",
          "expression": "value",
          "columnName": "Unofficial 001 ID Source",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "OCN",
                "l": "OCN"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "Unofficial 001 ID Source",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Unofficial 001 ID Source using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Unofficial 001 ID Source",
          "expression": "value",
          "columnName": "Unofficial 001 ID Source",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "CIS",
                "l": "CIS"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "001 ID",
    "expression": "grel:cells[\"Unofficial 001 ID Source\"].value+value",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column 001 ID using expression grel:cells[\"Unofficial 001 ID Source\"].value+value"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Unofficial 001 ID Source",
          "expression": "value",
          "columnName": "Unofficial 001 ID Source",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "CIS",
                "l": "CIS"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "Unofficial 001 ID Source",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Unofficial 001 ID Source using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Unofficial 001 ID Source",
          "expression": "value",
          "columnName": "Unofficial 001 ID Source",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "APA",
                "l": "APA"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "Unofficial 001 ID Source",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Unofficial 001 ID Source using expression null"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "Unofficial 001 ID Source",
    "expression": "value",
    "edits": [
      {
        "from": [
          "EBS"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "EBSCO"
      }
    ],
    "description": "Mass edit cells in column Unofficial 001 ID Source"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Unofficial 001 ID Source",
          "expression": "value",
          "columnName": "Unofficial 001 ID Source",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "EDZ",
                "l": "EDZ"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "Unofficial 001 ID Source",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Unofficial 001 ID Source using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Unofficial 001 ID Source",
          "expression": "value",
          "columnName": "Unofficial 001 ID Source",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "GTP",
                "l": "GTP"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "001 ID",
    "expression": "grel:cells[\"Unofficial 001 ID Source\"].value+value",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column 001 ID using expression grel:cells[\"Unofficial 001 ID Source\"].value+value"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Unofficial 001 ID Source",
          "expression": "value",
          "columnName": "Unofficial 001 ID Source",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "GTP",
                "l": "GTP"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "Unofficial 001 ID Source",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Unofficial 001 ID Source using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "001 ID Source",
          "expression": "value",
          "columnName": "001 ID Source",
          "invert": true,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "Backstage Library Works",
                "l": "Backstage Library Works"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        },
        {
          "type": "list",
          "name": "Unofficial 001 ID Source",
          "expression": "value",
          "columnName": "Unofficial 001 ID Source",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "OROUK",
                "l": "OROUK"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "001 ID Source",
    "expression": "grel:\"Backstage Library Works\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column 001 ID Source using expression grel:\"Backstage Library Works\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "001 ID Source",
          "expression": "value",
          "columnName": "001 ID Source",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "Backstage Library Works",
                "l": "Backstage Library Works"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        },
        {
          "type": "list",
          "name": "Unofficial 001 ID Source",
          "expression": "value",
          "columnName": "Unofficial 001 ID Source",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [],
          "selectBlank": true,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "001 ID Source",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column 001 ID Source using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Unofficial 001 ID Source",
          "expression": "value",
          "columnName": "Unofficial 001 ID Source",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "OROUK",
                "l": "OROUK"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Unofficial 001 ID Source",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Unofficial 001 ID Source using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Unofficial 001 ID Source",
          "expression": "value",
          "columnName": "Unofficial 001 ID Source",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "SLC",
                "l": "SLC"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "001 ID",
    "expression": "grel:cells[\"Unofficial 001 ID Source\"].value+value",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column 001 ID using expression grel:cells[\"Unofficial 001 ID Source\"].value+value"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Unofficial 001 ID Source",
          "expression": "value",
          "columnName": "Unofficial 001 ID Source",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "SLC",
                "l": "SLC"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "Unofficial 001 ID Source",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Unofficial 001 ID Source using expression null"
  },
  {
    "op": "core/row-removal",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Unofficial 001 ID Source",
          "expression": "value",
          "columnName": "Unofficial 001 ID Source",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "FIMED",
                "l": "FIMED"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "description": "Remove rows"
  }
]"""
messagebox.showwarning(title="YBP", message="\"YBP-long\" 001 IDs are identified as those at least 10 digits long and beginning with \"999\".")
os.startfile('Organize_UXU01_Output_pt2--Ebook_Central_Specific.json')
messagebox.showinfo(title="Instructions", message="Create custom facet on \"001 ID Source\" with \"contains(value,\"|\")\" and switch view to rows. For each row, determine which value in the column \"001 ID Source\" to keep.")
"""[
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "001 ID Source",
          "expression": "grel:contains(value,\"|\")",
          "columnName": "001 ID Source",
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
      "mode": "row-based"
    },
    "columnName": "001 ID Source",
    "expression": "value",
    "edits": [
      {
        "from": [
          "ProQuest|Ebook Central"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Ebook Central"
      }
    ],
    "description": "Mass edit cells in column 001 ID Source"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "001 ID Source",
          "expression": "grel:contains(value,\"|\")",
          "columnName": "001 ID Source",
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
      "mode": "row-based"
    },
    "columnName": "001 ID Source",
    "expression": "value",
    "edits": [
      {
        "from": [
          "ProQuest|Ebrary"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Ebrary"
      }
    ],
    "description": "Mass edit cells in column 001 ID Source"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "001 ID Source",
          "expression": "grel:contains(value,\"|\")",
          "columnName": "001 ID Source",
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
      "mode": "row-based"
    },
    "columnName": "001 ID Source",
    "expression": "value",
    "edits": [
      {
        "from": [
          "YBP|Ebook Library"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Ebook Library"
      }
    ],
    "description": "Mass edit cells in column 001 ID Source"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "001 ID Source",
          "expression": "grel:contains(value,\"|\")",
          "columnName": "001 ID Source",
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
      "mode": "row-based"
    },
    "columnName": "001 ID Source",
    "expression": "value",
    "edits": [
      {
        "from": [
          "YBP|Ebrary"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Ebrary"
      }
    ],
    "description": "Mass edit cells in column 001 ID Source"
  }
]"""
messagebox.showwarning(title="MyiLibrary", message="The following JSON Specifically contains a step for seperating the MyiLibrary ID source identifiers for the IDs from URLs and 035/599 fields.")
os.startfile('Organize_UXU01_Output_pt3--Ebook_Central_Specific.json')
messagebox.showinfo(title="Instructions", message="Investigate ISBNs with lengths other than 10 or 13, then clean up \"ISBN Types\" via clustering.")
"""[
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(e-book)",
          "(ebook) :",
          "(ebook)",
          "(eBook)",
          "ebook",
          "(E-book)",
          "(Ebook)",
          "(e-book",
          "E-book",
          "Ebook",
          "e-book",
          "(e-Book)",
          "(e.book)",
          "(ebook )",
          "(ebook}"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "eISBN"
      },
      {
        "from": [
          "(epub)",
          "(ePub)",
          "(EPUB)",
          "epub",
          "ePub",
          "(ePUB)",
          "(Epub)",
          "(e-pub)",
          "EPUB",
          "(E-PUB)",
          "(e-PUB)",
          "(epub.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "EPUB eISBN"
      },
      {
        "from": [
          "(pbk. : alk. paper)",
          "(pbk : alk. paper)",
          "(pbk. ;;alk. paper)",
          "(pbk. alk. paper)",
          "(pbk. :;alk. paper)",
          "(pbk alk. paper)",
          "(pbk. : al;k. paper)",
          "(pbk.: alk. paper)",
          "(pbk. : alk paper)",
          "(pbk. alk paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "PB ISBN"
      },
      {
        "from": [
          "(PDF ebook)",
          "(PDF ebook) :",
          "(ebook pdf)",
          "(e-book ;;PDF)",
          "(ebook (pdf))",
          "(e-book : PDF)",
          "(ebook PDF)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "PDF eISBN"
      },
      {
        "from": [
          "(hardcover : alk. paper)",
          "(hardcover alk. paper)",
          "(hardcover ;;alk. paper)",
          "(hardcover : alk. paper) :",
          "hardcover : alk. paper",
          "(hardcover: alk. paper)",
          "(Hardcover : alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN"
      },
      {
        "from": [
          "(hc : alk. paper)",
          "(hc. : alk. paper)",
          "(HC : alk. paper)",
          "(hc ;;alk. paper)",
          "(hc. alk. paper)",
          "(hc: alk. paper)",
          "(hc : alk. paper) :"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN"
      },
      {
        "from": [
          "(paperback : alkaline paper)",
          "(paperback ;;alkaline paper)",
          "paperback ;;alkaline paper",
          "(paperback. : alkaline paper)",
          "(paperback alkaline paper)",
          "(paperback: alkaline paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN"
      },
      {
        "from": [
          "(hbk. : alk. paper)",
          "(hbk : alk. paper)",
          "(hbk. alk. paper)",
          "(hbk alk. paper)",
          "(hbk. ;;alk. paper)",
          "(hbk.: alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN"
      },
      {
        "from": [
          "(ePub ebook)",
          "(ePub ebook) :",
          "(ebook epub)",
          "ePub ebook",
          "(e-book (epub))",
          "(ePub eBook)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "EPUB eISBN"
      },
      {
        "from": [
          "(hbk.)",
          "(hbk)",
          "(hbk.) :",
          "(hbk. )",
          "(Hbk.)",
          "hbk."
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN"
      },
      {
        "from": [
          "(alk. paper)",
          "(paper : alk. paper)",
          "(paper alk. paper)",
          "( alk. paper)",
          "(Paper : alk. paper)",
          "(alk. paper) :"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      },
      {
        "from": [
          "(cloth)",
          "(Cloth)",
          "cloth",
          "(cloth) :",
          "(cloth.)",
          "Cloth"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      },
      {
        "from": [
          "(cloth : alk. paper)",
          "(cloth ;;alk. paper)",
          "(cloth alk. paper)",
          "(cloth :;alk. paper)",
          "cloth : alk. paper",
          "(Cloth : alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      },
      {
        "from": [
          "(pbk.)",
          "(pbk.) :",
          "(pbk)",
          "pbk.",
          "(PBK.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      },
      {
        "from": [
          "(pdf)",
          "(PDF)",
          "pdf",
          "(pdf.)",
          "( pdf)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "PDF eISBN"
      },
      {
        "from": [
          "(mobi)",
          "(Mobi)",
          "mobi",
          "( mobi)",
          "(MOBI)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Mobi eISBN"
      },
      {
        "from": [
          "(ebk.)",
          "(ebk)",
          "(e-bk.)",
          "ebk",
          "(e-bk)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "eISBN"
      },
      {
        "from": [
          "(cl : alk. paper)",
          "(cl. : alk. paper)",
          "(cl ;;alk. paper)",
          "(cl alk. paper)",
          "(cl. ;;alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      },
      {
        "from": [
          "(set : alk. paper)",
          "((set) : alk. paper)",
          "(Set : alk. paper)",
          "(set ;;alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN [set]"
      },
      {
        "from": [
          "(cloth : alkaline paper)",
          "(cloth ;;alkaline paper)",
          "cloth : alkaline paper",
          "(cloth alkaline paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      },
      {
        "from": [
          "(pb : alk. paper)",
          "(PB : alk. paper)",
          "(pb ;;alk. paper)",
          "(pb alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "PB ISBN"
      },
      {
        "from": [
          "(hardback : alk. paper)",
          "(hardback alk. paper)",
          "(hardback ;;alk. paper)",
          "(hardback :;alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN"
      },
      {
        "from": [
          "Print version:",
          "Print version",
          "Print version :",
          "Print Version:"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      },
      {
        "from": [
          "(electronic bk.)",
          "electronic bk.",
          "(electronic bk.) :",
          "(electronic bk)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "eISBN"
      },
      {
        "from": [
          "(hardcover : alkaline paper)",
          "hardcover ;;alkaline paper",
          "(hardcover ;;alkaline paper)",
          "hardcover; alkaline paper"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN"
      },
      {
        "from": [
          "(paper)",
          "(Paper)",
          "(paper) :",
          "Paper"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      },
      {
        "from": [
          "ebook version :",
          "Ebook version",
          "Ebook version :",
          "ebook version"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "eISBN"
      },
      {
        "from": [
          "(hb : alk. paper)",
          "(HB : alk. paper)",
          "(hb ;;alk. paper)",
          "hb : alk. paper"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN"
      },
      {
        "from": [
          "(hardcover : acid-free paper)",
          "(hardcover ;;acid-free paper)",
          "hardcover ;;acid-free paper"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN"
      },
      {
        "from": [
          "(ePDF)",
          "(epdf)",
          "(e-PDF)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "PDF eISBN"
      },
      {
        "from": [
          "(electronic bk. : EPUB)",
          "(electronic bk. : ePub)",
          "(electronic bk. : epub)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "EPUB eISBN"
      },
      {
        "from": [
          "(Kindle)",
          "(kindle)",
          "kindle"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Kindle eISBN"
      },
      {
        "from": [
          "(v. 1 : alk. paper)",
          "v. 1 : alk. paper",
          "(v. 1. : alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN [vol. 1]"
      },
      {
        "from": [
          "(mobipocket)",
          "( mobipocket)",
          "(MobiPocket)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Mobi eISBN"
      },
      {
        "from": [
          "(paperback : alk. paper)",
          "(paperback :alk. paper)",
          "(paperback ;;alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "PB ISBN"
      },
      {
        "from": [
          "(hc.)",
          "(hc)",
          "(HC)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN"
      },
      {
        "from": [
          "(Kindle ebook) :",
          "(Kindle ebook)",
          "(kindle eBook)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Kindle eISBN"
      },
      {
        "from": [
          "(acid-free paper)",
          "(paper : acid-free paper)",
          "(paper acid-free paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      },
      {
        "from": [
          "(e-ISBN)",
          "(eISBN)",
          "e-ISBN"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "eISBN"
      },
      {
        "from": [
          "(pbk. : v. 1)",
          "(v. 1 : pbk.)",
          "(v. 1 pbk.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "PB ISBN [vol. 1]"
      },
      {
        "from": [
          "(ebk - PDF)",
          "(ebk. : PDF)",
          "(ebk. - PDF)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "PDF eISBN"
      },
      {
        "from": [
          "(hardback : acid-free paper)",
          "(hardback :acid-free paper)",
          "(hardback acid-free paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN"
      },
      {
        "from": [
          "(hardcover)",
          "hardcover",
          "(Hardcover)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN"
      },
      {
        "from": [
          "(ebk - ePUB)",
          "(ebk. : ePUB)",
          "(ebk. - ePUB)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "EPUB eISBN"
      },
      {
        "from": [
          "(paperback)",
          "paperback",
          "(Paperback)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "PB ISBN"
      },
      {
        "from": [
          "(v. 2 : alk. paper)",
          "v. 2 : alk. paper",
          "(v. 2. : alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN [vol. 2]"
      },
      {
        "from": [
          "Online version:",
          "Online version :",
          "Online version"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "eISBN"
      },
      {
        "from": [
          "(pb)",
          "(pb.)",
          "(PB)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "PB ISBN"
      },
      {
        "from": [
          ":",
          "()"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "CHECK"
      },
      {
        "from": [
          "(hardcover ; set)",
          "(set : hardcover)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN [set]"
      },
      {
        "from": [
          "hardcover;alkaline paper",
          "(hardcover;alkaline paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN"
      },
      {
        "from": [
          "(International edition)",
          "(international edition)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "CHECK"
      },
      {
        "from": [
          "(hardback : alkaline paper)",
          "(hardback ;;alkaline paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN"
      },
      {
        "from": [
          "(web PDF)",
          "(web pdf)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "PDF eISBN"
      },
      {
        "from": [
          "alkaline paper",
          "(alkaline paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      },
      {
        "from": [
          "(cloth : acid-free paper)",
          "(cloth acid-free paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      },
      {
        "from": [
          "(uelectronic book)",
          "uelectronic book"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "eISBN"
      },
      {
        "from": [
          "(Wiley online library)",
          "(Wiley Online Library)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Wiley eISBN"
      },
      {
        "from": [
          "(ebk : alk. paper)",
          "(ebk. : alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "CHECK"
      },
      {
        "from": [
          "(master e-book)",
          "(Master e-book)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "eISBN"
      },
      {
        "from": [
          "set : hardcover : alk. paper",
          "(set : hardcover : alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN [set]"
      },
      {
        "from": [
          "(consumer e-edition)",
          "consumer e-edition"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "eISBN"
      },
      {
        "from": [
          "(pbk. : v. 2)",
          "(v. 2 pbk.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "PB ISBN [vol. 2]"
      },
      {
        "from": [
          "(eMobi)",
          "(emobi)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Mobi eISBN"
      },
      {
        "from": [
          "(cased)",
          "cased"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "CHECK [set]"
      },
      {
        "from": [
          "(eb)",
          "(EB)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "eISBN"
      },
      {
        "from": [
          "(set hardcopy : alk. paper)",
          "(set : hardcopy : alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN [set]"
      },
      {
        "from": [
          "(vol. 1)",
          "vol. 1"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "CHECK [vol. 1]"
      },
      {
        "from": [
          "(electronic bk. ;;oBook)",
          "(electronic bk. : oBook)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "eISBN"
      },
      {
        "from": [
          "(ProQuest)",
          "ProQuest"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ProQuest CHECK"
      },
      {
        "from": [
          "(hbk. : set)",
          "hbk. : set"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN [set]"
      },
      {
        "from": [
          "(book)",
          "(Book)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "CHECK"
      },
      {
        "from": [
          "(pbk. edition : alk. paper)",
          "(pbk. edition alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "PB ISBN"
      },
      {
        "from": [
          "electronic book",
          "(electronic book)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "eISBN"
      },
      {
        "from": [
          "(bound)",
          "bound"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      },
      {
        "from": [
          "(print)",
          "print"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      },
      {
        "from": [
          "(hb)",
          "(HB)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN"
      },
      {
        "from": [
          "paperback;alkaline paper",
          "(paperback;alkaline paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "PB ISBN"
      },
      {
        "from": [
          "(St. Martin's)",
          "(St. Martins)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "St. Martin's CHECK"
      },
      {
        "from": [
          "(electronic bk. : Adobe Reader)",
          "(electronic bk. ;;Adobe Reader)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "PDF eISBN"
      },
      {
        "from": [
          "(paperback;acid-free paper)",
          "paperback;acid-free paper"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "PB ISBN"
      },
      {
        "from": [
          "hardcover;acid-free paper",
          "(hardcover;acid-free paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN"
      },
      {
        "from": [
          "(vol. 2)",
          "vol. 2"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "CHECK [vol. 2]"
      },
      {
        "from": [
          "(hbk. : acid-free paper)",
          "(hbk : acid-free paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN"
      },
      {
        "from": [
          "Electronic version:",
          "electronic version"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "eISBN"
      },
      {
        "from": [
          "(electronic)",
          "electronic"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "eISBN"
      },
      {
        "from": [
          "electronic publication",
          "(electronic publication)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "eISBN"
      },
      {
        "from": [
          "(set : acid-free paper)",
          "(set ;;acid-free paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN [set]"
      },
      {
        "from": [
          "(Mobipocket ebook)",
          "(Mobipocket ebook) :"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Mobi eISBN"
      },
      {
        "from": [
          "(cloth edition : alk. paper)",
          "(cloth edition alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      },
      {
        "from": [
          "(Mobipocket/Kindle)",
          "(mobipocket/kindle)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Mobi/Kindle eISBN"
      },
      {
        "from": [
          "(oBook)",
          "(obook)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "eISBN"
      },
      {
        "from": [
          "(pbk. ; set)",
          "(set pbk.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "PB ISBN [set]"
      },
      {
        "from": [
          "(institutional ebook)",
          "(ebook ;;Institutional)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "eISBN"
      },
      {
        "from": [
          "(ebook : alk. paper)",
          "(e-book : alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "CHECK"
      },
      {
        "from": [
          "(electronic bk. : PDF)",
          "(electronic bk. : pdf)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "PDF eISBN"
      },
      {
        "from": [
          "( international ed.)",
          "(international ed.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "CHECK"
      },
      {
        "from": [
          "(pbk. : acid free paper)",
          "(pbk. : acid free paper))"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "PB ISBN"
      },
      {
        "from": [
          "(vol. 2 : alk. paper)",
          "((vol 2) : alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN [vol. 2]"
      },
      {
        "from": [
          "(Adobe PDF)",
          "Adobe PDF"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "PDF eISBN"
      },
      {
        "from": [
          "(WebPDF)",
          "(webPDF)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "PDF eISBN"
      },
      {
        "from": [
          "(vol. 1 : alk. paper)",
          "((vol 1) : alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN [vol. 2]"
      },
      {
        "from": [
          "(St. Martin's Press)",
          "(St Martin's Press)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "St. Martin's CHECK"
      },
      {
        "from": [
          "((vol 3) : alk. paper)",
          "(vol. 3 : alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN [vol. 3]"
      },
      {
        "from": [
          "(print & perpetual access)",
          "print & perpetual access"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN + eISBN CHECK"
      },
      {
        "from": [
          "(online)",
          "online"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "eISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(hardback)",
          "hardback",
          "(Hardback)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN"
      },
      {
        "from": [
          "(pbk. : acid-free paper)",
          "(pbk. ;;acid-free paper)",
          "(pbk. acid-free paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "PB ISBN"
      },
      {
        "from": [
          "EPUB eISBN",
          "(e-ISBN; ePUB)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "EPUB eISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(softcover)",
          "(soft cover)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "PB ISBN"
      },
      {
        "from": [
          "set;alkaline paper",
          "set ;;alkaline paper"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN [set]"
      },
      {
        "from": [
          "electronic book;Mobipocket",
          "(electronic book ;;Mobipocket)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Mobi eISBN"
      },
      {
        "from": [
          "(v. 1)",
          "(v.1)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "CHECK [vol. 1]"
      },
      {
        "from": [
          "(v. 2)",
          "(v.2)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "CHECK [vol. 2]"
      },
      {
        "from": [
          "(hard copy : alk. paper)",
          "(hardcopy : alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      },
      {
        "from": [
          "(softcover : alk. paper)",
          "(soft cover : alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "PB ISBN"
      },
      {
        "from": [
          "print;alkaline paper",
          "(print ;;alkaline paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "Print version: Biltekoff, Charlotte, 1970-",
          "Print version: Erazo, Juliet S., 1970-",
          "Print version: Faudree, Paja, 1977-",
          "Print version: Langland, Victoria.",
          "Print version: Vazquez, Alexandra T., 1976-",
          "Print version: Mihas, Elena.",
          "Print version: Numerof, Rita E.",
          "Print version: Polgar, Stephen.",
          "Print version:Beaulieu, Elise M.",
          "Print version:|Selvin, Al."
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      },
      {
        "from": [
          "(hard cover : alk. paper)",
          "(hardccover : alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN"
      },
      {
        "from": [
          "(hardback); Print version:",
          "(hardback : print ed.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "020$a",
          "(e)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "eISBN"
      },
      {
        "from": [
          "020$z",
          "776$z"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      },
      {
        "from": [
          "(e book)",
          "e-bbok"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "eISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(hard back : alk. paper)",
          "hardback;alkaline paper"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN"
      },
      {
        "from": [
          "Mobi/Kindle eISBN",
          "(Mobi/Kindle)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Mobi/Kindle eISBN"
      },
      {
        "from": [
          "Print verion:",
          "Print verison:"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      },
      {
        "from": [
          "(hardbound : alk. paper)",
          "(hardbound)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN"
      },
      {
        "from": [
          "(paperbound : alk. paper)",
          "(paper binding : alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "ISBN Type",
          "expression": "value",
          "columnName": "ISBN Type",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "(hardcover ;;v. 1 ;;acid-free paper)",
                "l": "(hardcover ;;v. 1 ;;acid-free paper)"
              }
            },
            {
              "v": {
                "v": "(vol. 1 : hardcover : alk. paper)",
                "l": "(vol. 1 : hardcover : alk. paper)"
              }
            },
            {
              "v": {
                "v": "(vol. 1;hardcover)",
                "l": "(vol. 1;hardcover)"
              }
            },
            {
              "v": {
                "v": "(v. 1 : hardcover)",
                "l": "(v. 1 : hardcover)"
              }
            },
            {
              "v": {
                "v": "(v. 1 ;;hardcover ;;alk. paper)",
                "l": "(v. 1 ;;hardcover ;;alk. paper)"
              }
            },
            {
              "v": {
                "v": "(v. 1 : hbk)",
                "l": "(v. 1 : hbk)"
              }
            },
            {
              "v": {
                "v": "(v. 1 hardcopy : alk. paper)",
                "l": "(v. 1 hardcopy : alk. paper)"
              }
            },
            {
              "v": {
                "v": "(hb: vol. 1: alk. paper)",
                "l": "(hb: vol. 1: alk. paper)"
              }
            },
            {
              "v": {
                "v": "(HB : v. 1)",
                "l": "(HB : v. 1)"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        },
        {
          "type": "list",
          "name": "ISBN Type",
          "expression": "grel:toString(contains(value,\"1\"))",
          "columnName": "ISBN Type",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "true",
                "l": "true"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "grel:\"HB ISBN [vol. 1]\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column ISBN Type using expression grel:\"HB ISBN [vol. 1]\""
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "ISBN Type",
          "expression": "grel:toString(contains(value,\"1\"))",
          "columnName": "ISBN Type",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "true",
                "l": "true"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(hardcover 23 x 15,5 : alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "ISBN Type",
          "expression": "grel:toString(contains(value,\"1\"))",
          "columnName": "ISBN Type",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "true",
                "l": "true"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(23 x 15,5 cm : alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "ISBN Type",
          "expression": "value",
          "columnName": "ISBN Type",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "volume 1;alkaline paper",
                "l": "volume 1;alkaline paper"
              }
            },
            {
              "v": {
                "v": "(v. 1 : acid-free paper)",
                "l": "(v. 1 : acid-free paper)"
              }
            },
            {
              "v": {
                "v": "(v. 1 : cloth : alk. paper)",
                "l": "(v. 1 : cloth : alk. paper)"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        },
        {
          "type": "list",
          "name": "ISBN Type",
          "expression": "grel:toString(contains(value,\"1\"))",
          "columnName": "ISBN Type",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "true",
                "l": "true"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "grel:\"ISBN [vol. 1]\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column ISBN Type using expression grel:\"ISBN [vol. 1]\""
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "ISBN Type",
          "expression": "grel:toString(contains(value,\"1\"))",
          "columnName": "ISBN Type",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "true",
                "l": "true"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(volume 1)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "CHECK [vol. 1]"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "ISBN Type",
          "expression": "grel:toString(contains(value,\"1\"))",
          "columnName": "ISBN Type",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "true",
                "l": "true"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(v. 1 ebook)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "eISBN [vol. 1]"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "ISBN Type",
          "expression": "value",
          "columnName": "ISBN Type",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "(v. 2 ;;hardcover ;;alk. paper)",
                "l": "(v. 2 ;;hardcover ;;alk. paper)"
              }
            },
            {
              "v": {
                "v": "(vol. 2;hardcover)",
                "l": "(vol. 2;hardcover)"
              }
            },
            {
              "v": {
                "v": "(vol. 2 : hardcover : alk. paper)",
                "l": "(vol. 2 : hardcover : alk. paper)"
              }
            },
            {
              "v": {
                "v": "(v. 2 : acid-free paper)",
                "l": "(v. 2 : acid-free paper)"
              }
            },
            {
              "v": {
                "v": "(HB : v. 2)",
                "l": "(HB : v. 2)"
              }
            },
            {
              "v": {
                "v": "(hb: vol. 2: alk. paper)",
                "l": "(hb: vol. 2: alk. paper)"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        },
        {
          "type": "list",
          "name": "ISBN Type",
          "expression": "grel:toString(contains(value,\"2\"))",
          "columnName": "ISBN Type",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "true",
                "l": "true"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "grel:\"HB ISBN [vol. 2]\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column ISBN Type using expression grel:\"HB ISBN [vol. 2]\""
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "ISBN Type",
          "expression": "grel:toString(contains(value,\"2\"))",
          "columnName": "ISBN Type",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "true",
                "l": "true"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "($200.00 : alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "ISBN Type",
          "expression": "value",
          "columnName": "ISBN Type",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "(v. 2 ebook)",
                "l": "(v. 2 ebook)"
              }
            },
            {
              "v": {
                "v": "(electronic bk. : v. 2)",
                "l": "(electronic bk. : v. 2)"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        },
        {
          "type": "list",
          "name": "ISBN Type",
          "expression": "grel:toString(contains(value,\"2\"))",
          "columnName": "ISBN Type",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "true",
                "l": "true"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "grel:\"eISBN [vol. 2]\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column ISBN Type using expression grel:\"eISBN [vol. 2]\""
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "ISBN Type",
          "expression": "grel:toString(contains(value,\"2\"))",
          "columnName": "ISBN Type",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "true",
                "l": "true"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(volume 2)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "CHECK [vol. 2]"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "ISBN Type",
          "expression": "grel:toString(contains(value,\"2\"))",
          "columnName": "ISBN Type",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "true",
                "l": "true"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(v. 2 : hardcover)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN [vol. 2]"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "ISBN Type",
          "expression": "grel:toString(contains(value,\"2\"))",
          "columnName": "ISBN Type",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "true",
                "l": "true"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(v. 2 hardcopy : alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN [vol. 2]"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "ISBN Type",
          "expression": "grel:toString(contains(value,\"2\"))",
          "columnName": "ISBN Type",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "true",
                "l": "true"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "volume 2;alkaline paper"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN [vol. 2]"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "ISBN Type",
          "expression": "grel:toString(contains(value,\"2\"))",
          "columnName": "ISBN Type",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "true",
                "l": "true"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(2 volume set)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "CHECK [set]"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "ISBN Type",
          "expression": "grel:toString(contains(value,\"2\"))",
          "columnName": "ISBN Type",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "true",
                "l": "true"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(2 vol. set : hardcover : alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN [set]"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "ISBN Type",
          "expression": "grel:toString(contains(value,\"3\"))",
          "columnName": "ISBN Type",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "true",
                "l": "true"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(vol. 3 : hardcover : alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN [vol. 3]"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "ISBN Type",
          "expression": "grel:toString(contains(value,\"3\"))",
          "columnName": "ISBN Type",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "true",
                "l": "true"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(v. 3 : acid-free paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN [vol. 3]"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "ISBN Type",
          "expression": "grel:toString(contains(value,\"3\"))",
          "columnName": "ISBN Type",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "true",
                "l": "true"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(v. 3)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "CHECK [vol. 3]"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "ISBN Type",
          "expression": "grel:toString(contains(value,\"3\"))",
          "columnName": "ISBN Type",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "true",
                "l": "true"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(vol. 3)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "CHECK [vol. 3]"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "ISBN Type",
          "expression": "grel:toString(contains(value,\"4\"))",
          "columnName": "ISBN Type",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "true",
                "l": "true"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(v. 4 ;;hardback)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN [vol. 4]"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "ISBN Type",
          "expression": "grel:toString(contains(value,\"4\"))",
          "columnName": "ISBN Type",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "true",
                "l": "true"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(v. 4)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "CHECK [vol. 4]"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "ISBN Type",
          "expression": "grel:toString(contains(value,\"5\"))",
          "columnName": "ISBN Type",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "true",
                "l": "true"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(v. 5)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "CHECK [vol. 5]"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "ISBN Type",
          "expression": "grel:toString(contains(value,\"6\"))",
          "columnName": "ISBN Type",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "true",
                "l": "true"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(hbk. : 6 vol. set)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN [set]"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "ISBN Type",
          "expression": "grel:toString(contains(value,\"6\"))",
          "columnName": "ISBN Type",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "true",
                "l": "true"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(v. 6)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "CHECK [vol. 6]"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "ISBN + eISBN CHECK"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN + eISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(vol. l)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "CHECK [vol. 1]"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "ISBN Type",
          "expression": "grel:toString(contains(value,\"CHECK\"))",
          "columnName": "ISBN Type",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "true",
                "l": "true"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        },
        {
          "type": "list",
          "name": "ISBN Subfield",
          "expression": "value",
          "columnName": "ISBN Subfield",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "020$a",
                "l": "020$a"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "grel:replace(value,\"CHECK\",\"eISBN\")",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column ISBN Type using expression grel:replace(value,\"CHECK\",\"eISBN\")"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "ISBN Type",
          "expression": "grel:toString(contains(value,\"CHECK\"))",
          "columnName": "ISBN Type",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "true",
                "l": "true"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        },
        {
          "type": "list",
          "name": "ISBN Subfield",
          "expression": "value",
          "columnName": "ISBN Subfield",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "020$z",
                "l": "020$z"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "grel:replace(value,\"CHECK\",\"ISBN\")",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column ISBN Type using expression grel:replace(value,\"CHECK\",\"ISBN\")"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(hard)",
          "(hard cover)",
          "(harcover)",
          "(hard : alk)",
          "(hard copy)",
          "qhardcover",
          "(hardover)",
          "dqhardback"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN"
      },
      {
        "from": [
          "(hard)",
          "(hard cover)",
          "(hard : alk)",
          "(hard : alk. paper)",
          "(hard copy)",
          "qhardcover",
          "(hardover)",
          "dqhardback"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN"
      },
      {
        "from": [
          "(hard)",
          "(hard cover)",
          "(hard copy)",
          "qhardcover",
          "(hardover)",
          "dqhardback"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN"
      },
      {
        "from": [
          "(hard)",
          "qhardcover",
          "(hardover)",
          "dqhardback"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN"
      },
      {
        "from": [
          "(hard cover)",
          "(hard : alk)",
          "(hard : alk. paper)",
          "(hard copy)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN"
      },
      {
        "from": [
          "(epdfs)",
          "(updf)",
          "(webready PDF)",
          "(eBook-PDF)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "PDF eISBN"
      },
      {
        "from": [
          "(hard cover)",
          "(harcover)",
          "qhardcover",
          "(hardover)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN"
      },
      {
        "from": [
          "(print ed.)",
          "(print-ISBN)",
          "(print0",
          "Print versio:"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      },
      {
        "from": [
          "(hard)",
          "(hard cover)",
          "qhardcover",
          "(hardover)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN"
      },
      {
        "from": [
          "(hc : acid-free paper)",
          "(hard cover : acid-free paper)",
          "(hardcopy : acid-free paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN"
      },
      {
        "from": [
          "(hard cover)",
          "qhardcover",
          "(hardover)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN"
      },
      {
        "from": [
          "qhardcover",
          "(hardover)",
          "dqhardback"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN"
      },
      {
        "from": [
          "(print-ISBN)",
          "(print0",
          "Print versio:"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      },
      {
        "from": [
          "PDF eISBN",
          "(epdfs)",
          "(updf)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "PDF eISBN"
      },
      {
        "from": [
          "(hard cover)",
          "(harcover)",
          "qhardcover"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN"
      },
      {
        "from": [
          "Mobi eISBN",
          "(eMobil)",
          "(mobi/.prc)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Mobi eISBN"
      },
      {
        "from": [
          "PDF eISBN",
          "(updf)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "PDF eISBN"
      },
      {
        "from": [
          "(hard cover)",
          "qhardcover"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN"
      },
      {
        "from": [
          "qhardcover",
          "dqhardback"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN"
      },
      {
        "from": [
          "(pdf : alk. paper)",
          "(ebook pdf : alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "PDF eISBN"
      },
      {
        "from": [
          "(print : alk. paper)",
          "(print : acid-free paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      },
      {
        "from": [
          "(set ebook)",
          "(consumer ebook)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "eISBN"
      },
      {
        "from": [
          "(hard : alk)",
          "(hard : alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN"
      },
      {
        "from": [
          "(paperwork)",
          "(paper/ws)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      },
      {
        "from": [
          "(spiral bound)",
          "(softbound)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      },
      {
        "from": [
          "(paper/cd-rom)",
          "(cloth/cd-rom)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN + CD"
      },
      {
        "from": [
          "(Macmillan)",
          "(Macmillan Press)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Macmillan CHECK"
      },
      {
        "from": [
          "(trade pbk.)",
          "(series pbk.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "PB ISBN"
      },
      {
        "from": [
          "qhardcover",
          "(hardover)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN"
      },
      {
        "from": [
          "Wiley eISBN",
          "(Wiley E-Text)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Wiley eISBN"
      },
      {
        "from": [
          "Printed edition:",
          "Print versio:"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      },
      {
        "from": [
          "(papeback)",
          "(alk. : paperback)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "PB ISBN"
      },
      {
        "from": [
          "Mobi eISBN",
          "(mobi/.prc)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Mobi eISBN"
      },
      {
        "from": [
          "(hd.bd.)",
          "(hdbk.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN"
      },
      {
        "from": [
          "(hard cover)",
          "(hard copy)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(epub : alk. paper)",
          "(ebook epub : alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "CHECK"
      },
      {
        "from": [
          "(Trade Paper)",
          "(acid free paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      },
      {
        "from": [
          "(clothbound : alk. paper)",
          "(Netherlands : alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      },
      {
        "from": [
          "(ebook edition)",
          "(e-book ISBN)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "eISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "paperback;lk. paper",
          "paperbackback"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "PB ISBN"
      },
      {
        "from": [
          "Mobi eISBN",
          "electronic publication, mobi & electronic book"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Mobi eISBN"
      },
      {
        "from": [
          "(Institutum Historicum Societatis Iesu)",
          "(instructor's materials)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "CHECK"
      },
      {
        "from": [
          "(series cased)",
          "(slipcase set)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "CHECK [set]"
      },
      {
        "from": [
          "(MyiLibrary)",
          "(MyiLibrary - Multi-user)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "MyiLibrary eISBN"
      },
      {
        "from": [
          "EPUB eISBN",
          "electronic book;EPUB"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "EPUB eISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(CRC Press)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "CRC Press ISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(Dance Books)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Dance Books ISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(eb : alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "CHECK"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(electronic bk. : Mobipocket)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Mobi eISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(electronic : alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "CHECK"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(electronic bk.;Adobe Reader)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "PDF eISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(electronic book;set)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "eISBN [set]"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(eMobi ebook) :"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Mobi eISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(laminated cased cover)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN [set]"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(library edition)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "CHECK"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(main edition)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "CHECK"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(McGraw-Hill e-ISBN)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "(McGraw-Hill eISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(McGraw-Hill)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "McGraw-Hill CHECK"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(McGraw-Hill eISBN"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "McGraw-Hill eISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(NetLibrary e-ISBN)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "NetLibrary eISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(obk : alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "CHECK"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(Master)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "CHECK"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(Ohmsha)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "CHECK"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(paper/cd-rom : acid free paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN + CD"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(paper/dvd)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN + DVD"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(paper/website)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN + eISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(pbk./website)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "PB ISBN + eISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(ppr : alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(Proquest Ebook Central)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Ebook Central eISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(PsychiatryOnline)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "PsychiatryOnline eISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(set)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "CHECK [set]"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(Springer e-ISBN)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Springer eISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(Springer) (alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Springer ISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(United States)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "CHECK"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(US)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "CHECK"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(variant on dustjacket)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(VitalBook ebook)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "VitalBook eISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(Woodhead Pub. : book)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Woodhead Pub. ISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(Woodhead Pub. : e-book)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Woodhead Pub. eISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(xml)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "eISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "Also issued in print:"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "kindle edition"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Kindle eISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "q"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(cloth ed. : alk. paper)",
          "(cloth : alkalihe paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      },
      {
        "from": [
          "(electronic format)",
          "[electronic resource]"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "eISBN"
      },
      {
        "from": [
          "(pbk. : alkaline paper)",
          "(pbk. : alk.paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "PB ISBN"
      },
      {
        "from": [
          "(special sale ed. : alk. paper)",
          "(standard ed. : alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(adobe ebook)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "PDF eISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "Adobe electronic book"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "PDF eISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "Electronic reproduction of (manifestation):"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "eISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "hardback;acid-free paper"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "ISBN Type",
          "expression": "value",
          "columnName": "ISBN Type",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "cloth;alk. paper",
                "l": "cloth;alk. paper"
              }
            },
            {
              "v": {
                "v": "hardcover;alkaline paper;paperback",
                "l": "hardcover;alkaline paper;paperback"
              }
            },
            {
              "v": {
                "v": "(cl.)",
                "l": "(cl.)"
              }
            },
            {
              "v": {
                "v": "(cloth); Print version:",
                "l": "(cloth); Print version:"
              }
            },
            {
              "v": {
                "v": "(book : alk. paper)",
                "l": "(book : alk. paper)"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "grel:\"ISBN\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column ISBN Type using expression grel:\"ISBN\""
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(Amazon ebook)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Kindle eISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(CD-ROM)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "CD"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(CD)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "CD"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(computer optical disc) :"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "CD"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "ISBN Type",
          "expression": "value",
          "columnName": "ISBN Type",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "(HTML ebook) :",
                "l": "(HTML ebook) :"
              }
            },
            {
              "v": {
                "v": "(ebook ;;Individual)",
                "l": "(ebook ;;Individual)"
              }
            },
            {
              "v": {
                "v": "(e-ISB)",
                "l": "(e-ISB)"
              }
            },
            {
              "v": {
                "v": "(elecronic bk.)",
                "l": "(elecronic bk.)"
              }
            },
            {
              "v": {
                "v": "(Online Component)",
                "l": "(Online Component)"
              }
            },
            {
              "v": {
                "v": "(non-library e-book)",
                "l": "(non-library e-book)"
              }
            },
            {
              "v": {
                "v": "(ekb)",
                "l": "(ekb)"
              }
            },
            {
              "v": {
                "v": "(online resource) :",
                "l": "(online resource) :"
              }
            },
            {
              "v": {
                "v": "(electronic copy)",
                "l": "(electronic copy)"
              }
            },
            {
              "v": {
                "v": "(ed. electrÃ³nica)",
                "l": "(ed. electrÃ³nica)"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "grel:\"eISBN\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column ISBN Type using expression grel:\"eISBN\""
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(Association for Supervision and Curriculum Development : electronic bk.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Association for Supervision and Curriculum Development eISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(CourseSmart)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "CourseSmart eISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(companion website)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "eISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(cloth/website)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN + eISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(CD-ROM pack)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "CD [set]"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "ISBN Type",
          "expression": "value",
          "columnName": "ISBN Type",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "(br.)",
                "l": "(br.)"
              }
            },
            {
              "v": {
                "v": "(Book, Other)",
                "l": "(Book, Other)"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "grel:\"eISBN\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column ISBN Type using expression grel:\"eISBN\""
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(binder)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(alk. : cloth)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(pbk.); (hardback)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(U.S. : alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(hb: set : alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN [set]"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "ISBN Type",
          "expression": "value",
          "columnName": "ISBN Type",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "(hard cover; sewn : alk. paper)",
                "l": "(hard cover; sewn : alk. paper)"
              }
            },
            {
              "v": {
                "v": "(hbk. : alkaline paper)",
                "l": "(hbk. : alkaline paper)"
              }
            },
            {
              "v": {
                "v": "(hdbk. : alk. paper)",
                "l": "(hdbk. : alk. paper)"
              }
            },
            {
              "v": {
                "v": "(hardcover ;;print)",
                "l": "(hardcover ;;print)"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "grel:\"HB ISBN\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column ISBN Type using expression grel:\"HB ISBN\""
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(Kindle/mobipocket)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Mobi/Kindle eISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(Set hbk: alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "HB ISBN [set]"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "ISBN Type",
          "expression": "value",
          "columnName": "ISBN Type",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "(pbk. ed. : alk. paper)",
                "l": "(pbk. ed. : alk. paper)"
              }
            },
            {
              "v": {
                "v": "(softback : alk. paper)",
                "l": "(softback : alk. paper)"
              }
            },
            {
              "v": {
                "v": "(pbk. format : alk. paper)",
                "l": "(pbk. format : alk. paper)"
              }
            },
            {
              "v": {
                "v": "(paperback : acid-free paper)",
                "l": "(paperback : acid-free paper)"
              }
            },
            {
              "v": {
                "v": "(pbk. : age-resistant paper)",
                "l": "(pbk. : age-resistant paper)"
              }
            },
            {
              "v": {
                "v": "(pbk-ISBN)",
                "l": "(pbk-ISBN)"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "grel:\"PB ISBN\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column ISBN Type using expression grel:\"PB ISBN\""
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(Oxford University Press) :"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Oxford UP CHECK"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(sc : alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(case : alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN [set]"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(casebound)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN [set]"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(Higher Education Press) (alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Higher Education Press ISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(jacketed ;;alk. paper)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "value",
    "edits": [
      {
        "from": [
          "(IOS)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "eISBN"
      }
    ],
    "description": "Mass edit cells in column ISBN Type"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "ISBN Type",
          "expression": "grel:toString(contains(value,\"CHECK\"))",
          "columnName": "ISBN Type",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "true",
                "l": "true"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        },
        {
          "type": "list",
          "name": "ISBN Subfield",
          "expression": "value",
          "columnName": "ISBN Subfield",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "020$a",
                "l": "020$a"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "grel:replace(value,\"CHECK\",\"eISBN\")",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column ISBN Type using expression grel:replace(value,\"CHECK\",\"eISBN\")"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "ISBN Type",
          "expression": "grel:toString(contains(value,\"CHECK\"))",
          "columnName": "ISBN Type",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "true",
                "l": "true"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        },
        {
          "type": "list",
          "name": "ISBN Subfield",
          "expression": "value",
          "columnName": "ISBN Subfield",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "020$z",
                "l": "020$z"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "ISBN Type",
    "expression": "grel:replace(value,\"CHECK\",\"ISBN\")",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column ISBN Type using expression grel:replace(value,\"CHECK\",\"ISBN\")"
  }
]"""
messagebox.showwarning(title="Duplicate Dedupe Column Blank Down", message="The process for blanking down then removing rows with duplicate ISBNs for the record is done twice because the first time doesn't catch all the duplicates; the reason for this is unknown.")
messagebox.showwarning(title="Ebook Central", message="Non-Ebook Central ID sources that didn't have duplicate IDs have their columns removed in this JSON.")
messagebox.showwarning(title="Ebook Central", message="The following JSON contains hard coded fill up and down then blank down instructions--in actuality, a loop knowing the names of the columns created needs to create that part of the JSON.")
#ToDo: figure out how to constructo loop for fill up and down then blank down hard coded into the pt4 JSON
messagebox.showwarning(title="Exact Match via Ebook Central Columns", message="The \"Exact Match via Ebook Central ID\" column was created because there weren't any BIBs with multiple Ebook Central IDs.")
os.startfile('Organize_UXU01_Output_pt4--Ebook_Central_Specific.json')
#Alert: This seems to not include BIBs that don't have FSU 856 fields--is this a problem?
messagebox.showinfo(title="Instructions", message="Perform clustering on \"Temp Title 2\".")
"""[
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "volume 2,)",
          "volume 2 /)",
          "volume 2)",
          "volume 2,) ",
          "volume 2 :)",
          "volume 2) "
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 2"
      },
      {
        "from": [
          "volume 1,)",
          "volume 1,) ",
          "volume 1 /)",
          "volume 1 :)",
          "[volume 1]) ",
          "volume 1 /) "
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 1"
      },
      {
        "from": [
          "1st Ed.)",
          "[1st Ed.].)",
          "1st Ed,)",
          "1st [ed.].)",
          "1st. Ed.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 1"
      },
      {
        "from": [
          "second Edition.)",
          "second Edition /)",
          "second Edition)",
          "[second Edition])",
          "second Edition. /)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 2"
      },
      {
        "from": [
          "[new Ed.].)",
          "new Ed.)",
          "[new Ed.] /)",
          "[new Ed.])",
          "[new] Ed.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed rev"
      },
      {
        "from": [
          "2nd Ed., Rev.)",
          "2nd Rev. Ed.)",
          "2nd Ed. Rev.)",
          "rev. 2nd Ed.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 2 rev"
      },
      {
        "from": [
          "volume Ii /)",
          "volume Ii,)",
          "volume Ii)",
          "volume Ii,) "
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 51"
      },
      {
        "from": [
          "2nd Ed.)",
          "2nd Ed. /)",
          "2nd. Ed.)",
          "[2nd Ed.].)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 2"
      },
      {
        "from": [
          "volume 3)",
          "volume 3,) ",
          "volume 3 /)",
          "volume 3,)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 3"
      },
      {
        "from": [
          "fourth Edition.)",
          "fourth Edition /)",
          "fourth Edition)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 4"
      },
      {
        "from": [
          "1st [edition].)",
          "1st Edition)",
          "1st Edition.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 1"
      },
      {
        "from": [
          "rev. And Updated Ed.)",
          "[rev. And Updated Ed.])",
          "[rev. And Updated Ed.].)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed rev"
      },
      {
        "from": [
          "2nd Ed., Rev. And Expanded.)",
          "2nd Ed., Rev. And Expanded /)",
          "2nd Ed., Rev. And Expanded)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 2 rev"
      },
      {
        "from": [
          "volume I,)",
          "volume I)",
          "volume I) "
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 1"
      },
      {
        "from": [
          "3rd Ed.)",
          "3rd Ed. /)",
          "[3rd Ed.].)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 3"
      },
      {
        "from": [
          "5th Ed.)",
          "5th Ed. /)",
          "[5th] Ed.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 5"
      },
      {
        "from": [
          "12th Ed.)",
          "12th Ed. /)",
          "[12th Ed.].)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 12"
      },
      {
        "from": [
          "first Edition.)",
          "first Edition)",
          "first [edition].)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 1"
      },
      {
        "from": [
          "revised And Expanded Second Edition.)",
          "second Edition, Revised And Expanded.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed rev"
      },
      {
        "from": [
          "rev. And Expanded Ed.)",
          "rev. And Expanded Ed. /)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed rev"
      },
      {
        "from": [
          "ninth Edition.)",
          "ninth Edition /)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 9"
      },
      {
        "from": [
          "rev. Ed.)",
          "rev. Ed. /)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed rev"
      },
      {
        "from": [
          "5th Ed. Rev.)",
          "5th Ed., Rev.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 5 rev"
      },
      {
        "from": [
          "volume Nine /)",
          "volume Nine,)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 9"
      },
      {
        "from": [
          "3rd Ed., Rev. And Updated.)",
          "rev. And Updated 3rd Ed.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 3 rev"
      },
      {
        "from": [
          "part 2 /)",
          "part 2,)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 2"
      },
      {
        "from": [
          "updated And Expanded Edition.)",
          "updated And Expanded [edition].)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed rev"
      },
      {
        "from": [
          "1 [edition].)",
          "1 Edition.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 1"
      },
      {
        "from": [
          "third Edition.)",
          "third Edition /)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 3"
      },
      {
        "from": [
          "eighth Edition.)",
          "eighth Edition /)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 8"
      },
      {
        "from": [
          "volume 4)",
          "volume 4,)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 4"
      },
      {
        "from": [
          "1st Rev. Ed.)",
          "1st Ed., Rev.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 1 rev"
      },
      {
        "from": [
          "seventh Edition.)",
          "seventh Edition /)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 7"
      },
      {
        "from": [
          "[enhanced Credo Edition])",
          "[enhanced Credo Edition].)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": ""
      },
      {
        "from": [
          "fifth Edition.)",
          "fifth Edition /)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 5"
      },
      {
        "from": [
          "2014 /)",
          "2014)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "2014  ed"
      },
      {
        "from": [
          "sixth Edition.)",
          "sixth Edition /)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 6"
      },
      {
        "from": [
          "ii)",
          "ii,)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "CHECK 2"
      },
      {
        "from": [
          "volume 37 /)",
          "volume 37)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 37"
      },
      {
        "from": [
          "revised And Updated [edition].)",
          "revised And Updated Edition.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed rev"
      },
      {
        "from": [
          "vol. 2 /)",
          "vol. 2,)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 2"
      },
      {
        "from": [
          "revised Edition.)",
          "revised Edition /)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed rev"
      },
      {
        "from": [
          "volume Two,)",
          "volume Two /)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 2"
      },
      {
        "from": [
          "4th Ed.)",
          "4th Ed. /)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 4"
      },
      {
        "from": [
          "volume 5)",
          "volume 5,)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 5"
      },
      {
        "from": [
          "2nd Edition.)",
          "2nd Edition /)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 2"
      },
      {
        "from": [
          "7th Ed.)",
          "7th Ed. /)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 7"
      },
      {
        "from": [
          "english Ed.)",
          "[english Ed.].)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": ""
      },
      {
        "from": [
          "part B) ",
          "part B,) "
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "part B"
      },
      {
        "from": [
          "first U.S. Edition.)",
          "first Us Edition.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "first U.S. Edition.)"
      },
      {
        "from": [
          "updated Ed.)",
          "[updated Ed.].)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed rev"
      },
      {
        "from": [
          "[pbk. Ed., 1998])",
          "[pbk. Ed., 1998].)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": ""
      },
      {
        "from": [
          "volume 29 /)",
          "volume 29 :)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 29"
      },
      {
        "from": [
          "11th Ed. /)",
          "11th Ed.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 11"
      },
      {
        "from": [
          "6th Ed.)",
          "6th Ed. /)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 6"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "ed 5",
          "5 Ed.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 5"
      },
      {
        "from": [
          "vol 1",
          "vol. 1,)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 1"
      },
      {
        "from": [
          "ed 1",
          "1. Ed.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 1"
      },
      {
        "from": [
          "vol 3",
          "vol. 3)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 3"
      },
      {
        "from": [
          "vol 29",
          "vol. 29 /)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 29"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Temp Title 2",
          "expression": "value",
          "columnName": "Temp Title 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "20th Edition.)",
                "l": "20th Edition.)"
              }
            },
            {
              "v": {
                "v": "3rd Ed., Oxford Pbk Ed. /)",
                "l": "3rd Ed., Oxford Pbk Ed. /)"
              }
            },
            {
              "v": {
                "v": "10th Edition.)",
                "l": "10th Edition.)"
              }
            },
            {
              "v": {
                "v": "11th Ed., A New And Enlarged Ed. / By Sarah Corbin Robert [and Others].)",
                "l": "11th Ed., A New And Enlarged Ed. / By Sarah Corbin Robert [and Others].)"
              }
            },
            {
              "v": {
                "v": "18th Ed.)",
                "l": "18th Ed.)"
              }
            },
            {
              "v": {
                "v": "4th Edition.)",
                "l": "4th Edition.)"
              }
            },
            {
              "v": {
                "v": "7th Edition.)",
                "l": "7th Edition.)"
              }
            },
            {
              "v": {
                "v": "21st Edition.)",
                "l": "21st Edition.)"
              }
            },
            {
              "v": {
                "v": "9th Ed.)",
                "l": "9th Ed.)"
              }
            },
            {
              "v": {
                "v": "50th Edition.)",
                "l": "50th Edition.)"
              }
            },
            {
              "v": {
                "v": "8th Ed.)",
                "l": "8th Ed.)"
              }
            },
            {
              "v": {
                "v": "2nd Ed. 2018.)",
                "l": "2nd Ed. 2018.)"
              }
            },
            {
              "v": {
                "v": "3rd Edition.)",
                "l": "3rd Edition.)"
              }
            },
            {
              "v": {
                "v": "4th Ed. [kindle Ed.])",
                "l": "4th Ed. [kindle Ed.])"
              }
            },
            {
              "v": {
                "v": "15th Ed.)",
                "l": "15th Ed.)"
              }
            },
            {
              "v": {
                "v": "16th Ed.)",
                "l": "16th Ed.)"
              }
            },
            {
              "v": {
                "v": "13th Ed.)",
                "l": "13th Ed.)"
              }
            },
            {
              "v": {
                "v": "10th Ed.)",
                "l": "10th Ed.)"
              }
            },
            {
              "v": {
                "v": "34th Ed.)",
                "l": "34th Ed.)"
              }
            },
            {
              "v": {
                "v": "1st Ed. 2017.)",
                "l": "1st Ed. 2017.)"
              }
            },
            {
              "v": {
                "v": "17th Ed.)",
                "l": "17th Ed.)"
              }
            },
            {
              "v": {
                "v": "51st Edition.)",
                "l": "51st Edition.)"
              }
            },
            {
              "v": {
                "v": "22nd Edition.)",
                "l": "22nd Edition.)"
              }
            },
            {
              "v": {
                "v": "2nd Ed., Pbk. Ed.)",
                "l": "2nd Ed., Pbk. Ed.)"
              }
            },
            {
              "v": {
                "v": "4th Ed., 2012 2013 Update.)",
                "l": "4th Ed., 2012 2013 Update.)"
              }
            },
            {
              "v": {
                "v": "25th Edition.)",
                "l": "25th Edition.)"
              }
            },
            {
              "v": {
                "v": "1st Ed ; Foreword By Vicki L. Ruiz.)",
                "l": "1st Ed ; Foreword By Vicki L. Ruiz.)"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        },
        {
          "type": "list",
          "name": "Temp Title 2",
          "expression": "grel:length(find(value,/\\d+\\w{2} (E|e)d/))>0",
          "columnName": "Temp Title 2",
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
    "columnName": "Temp Title 2",
    "expression": "grel:\"ed \"+find(value,/\\d+/)[0]",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Temp Title 2 using expression grel:\"ed \"+find(value,/\\d+/)[0]"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Temp Title 2",
          "expression": "grel:length(find(value,/\\d+\\w{2} (E|e)d/))>0",
          "columnName": "Temp Title 2",
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
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "rev. 4th Ed.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 4 rev"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Temp Title 2",
          "expression": "grel:length(find(value,/\\d+\\w{2} (E|e)d/))>0",
          "columnName": "Temp Title 2",
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
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "rev. & Updated 3rd Ed.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 3 rev"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Temp Title 2",
          "expression": "grel:length(find(value,/\\d+\\w{2} (E|e)d/))>0",
          "columnName": "Temp Title 2",
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
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "fully Revised 2nd Ed.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 2 rev"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Temp Title 2",
          "expression": "grel:length(find(value,/\\d+\\w{2} (E|e)d/))>0",
          "columnName": "Temp Title 2",
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
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "completely Rev. And Updated, 3rd Ed.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 3 rev"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Temp Title 2",
          "expression": "grel:length(find(value,/\\d+\\w{2} (E|e)d/))>0",
          "columnName": "Temp Title 2",
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
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "6th Ed., [rev. And Expanded].)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 6 rev"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Temp Title 2",
          "expression": "grel:length(find(value,/\\d+\\w{2} (E|e)d/))>0",
          "columnName": "Temp Title 2",
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
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "4th Ed., Rev. And Expanded.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 4 rev"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Temp Title 2",
          "expression": "grel:length(find(value,/\\d+\\w{2} (E|e)d/))>0",
          "columnName": "Temp Title 2",
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
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "3rd Ed., Rev. And Expanded.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 3 rev"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Temp Title 2",
          "expression": "grel:length(find(value,/\\d+\\w{2} (E|e)d/))>0",
          "columnName": "Temp Title 2",
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
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "3rd Ed. Rev.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 3 rev"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Temp Title 2",
          "expression": "grel:length(find(value,/\\d+\\w{2} (E|e)d/))>0",
          "columnName": "Temp Title 2",
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
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "3rd Ed. Rev. And Updated Work.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 3 rev"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Temp Title 2",
          "expression": "grel:length(find(value,/\\d+\\w{2} (E|e)d/))>0",
          "columnName": "Temp Title 2",
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
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "2nd Ed., Updated And Expanded.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 2 rev"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Temp Title 2",
          "expression": "grel:length(find(value,/\\d+\\w{2} (E|e)d/))>0",
          "columnName": "Temp Title 2",
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
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "2nd Ed., New Ed.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 2 rev"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Temp Title 2",
          "expression": "grel:length(find(value,/\\d+\\w{2} (E|e)d/))>0",
          "columnName": "Temp Title 2",
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
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "2nd Ed., Rev. And Updated.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 2 rev"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Temp Title 2",
          "expression": "grel:length(find(value,/\\d+\\w{2} (E|e)d/))>0",
          "columnName": "Temp Title 2",
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
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "all New 5th Ed.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 5"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Temp Title 2",
          "expression": "grel:length(find(value,/\\d+\\w{2} (E|e)d/))>0",
          "columnName": "Temp Title 2",
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
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "all New 4th Ed.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 4"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Temp Title 2",
          "expression": "grel:length(find(value,/\\d+\\w{2} (E|e)d/))>0",
          "columnName": "Temp Title 2",
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
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "3rd Ed. ; Thirtieth Anniversary Ed. With A New Introduction.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 3"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Temp Title 2",
          "expression": "grel:length(find(value,/\\d+\\w{2} (E|e)d/))>0",
          "columnName": "Temp Title 2",
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
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "2nd Ed., Rev. 10th Anniversary Ed.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 2 rev"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Temp Title 2",
          "expression": "grel:length(find(value,/\\d+\\w{2} (E|e)d/))>0",
          "columnName": "Temp Title 2",
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
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "[147th Ed.] /)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 147"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Temp Title 2",
          "expression": "grel:length(find(value,/\\d+\\w{2} (E|e)d/))>0",
          "columnName": "Temp Title 2",
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
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "2004 Ed.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "2004 ed"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Temp Title 2",
          "expression": "grel:length(find(value,/\\d+\\w{2} (E|e)d/))>0",
          "columnName": "Temp Title 2",
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
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "2011 Edition.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "2011 ed"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Temp Title 2",
          "expression": "grel:length(find(value,/\\d+\\w{2} (E|e)d/))>0",
          "columnName": "Temp Title 2",
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
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "2012 Ed.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "2012 ed"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Temp Title 2",
          "expression": "grel:length(find(value,/\\d+\\w{2} (E|e)d/))>0",
          "columnName": "Temp Title 2",
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
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "2014 Edition.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "2014 ed"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Temp Title 2",
          "expression": "grel:startsWith(value,\"vol.\")",
          "columnName": "Temp Title 2",
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
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "vol. 23 /)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 23"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Temp Title 2",
          "expression": "grel:startsWith(value,\"vol.\")",
          "columnName": "Temp Title 2",
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
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "vol. 26 :)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 26"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Temp Title 2",
          "expression": "grel:startsWith(value,\"vol.\")",
          "columnName": "Temp Title 2",
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
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "vol. 31 /)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 31"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Temp Title 2",
          "expression": "grel:startsWith(value,\"vol.\")",
          "columnName": "Temp Title 2",
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
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "vol. 62)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 62"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Temp Title 2",
          "expression": "grel:startsWith(value,\"vol.\")",
          "columnName": "Temp Title 2",
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
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "vol. 73)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 73"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Temp Title 2",
          "expression": "grel:startsWith(value,\"vol.\")",
          "columnName": "Temp Title 2",
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
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "vol. Iv)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 4"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Temp Title 2",
          "expression": "grel:startsWith(value,\"vol.\")",
          "columnName": "Temp Title 2",
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
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "vol.2b,) "
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 2B"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Temp Title 2",
          "expression": "grel:length(find(value,/volume \\d+ /))>0",
          "columnName": "Temp Title 2",
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
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "volume 1 3 :)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 1-3"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Temp Title 2",
          "expression": "grel:length(find(value,/volume \\d+ /))>0",
          "columnName": "Temp Title 2",
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
    "columnName": "Temp Title 2",
    "expression": "grel:\"vol \"+split(value,\" \")[1]",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Temp Title 2 using expression grel:\"vol \"+split(value,\" \")[1]"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Temp Title 2",
          "expression": "grel:length(find(value,/volume \\d+/))>0",
          "columnName": "Temp Title 2",
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
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "volume 33, Number 2,)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 33"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Temp Title 2",
          "expression": "grel:length(find(value,/volume \\d+/))>0",
          "columnName": "Temp Title 2",
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
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "volume 31,)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 31"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Temp Title 2",
          "expression": "grel:length(find(value,/volume \\d+/))>0",
          "columnName": "Temp Title 2",
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
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "volume 6)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 6"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Temp Title 2",
          "expression": "grel:length(find(value,/volume \\d+/))>0",
          "columnName": "Temp Title 2",
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
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "volume 7,)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 7"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Temp Title 2",
          "expression": "grel:length(find(value,/volume \\d+/))>0",
          "columnName": "Temp Title 2",
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
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "volume 6a) "
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 6a"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Temp Title 2",
          "expression": "grel:length(find(value,/volume \\d+/))>0",
          "columnName": "Temp Title 2",
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
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "volume 6b) "
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 6b"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "[pbk. Ed., 1997])"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": ""
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "3e [ed.] /)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 3"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "7th Rev. Ed.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 7 rev"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "edition 15.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 15"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "eighth Edition, Entirely Revised And Reset.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 8 rev"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "expanded Ed.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed rev"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "extended And Revised Edition.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed rev"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "extended Edition.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed rev"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "fifth Editon.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 5"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "fifty First Edition.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 51"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "fifty Second Edition.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 52"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "fisrt Edition.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 1"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "fourth Edition, 2012 2013 Update.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 4"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "fourth Edition, Dsm 5 Chapter Update.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 4"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "fully Rev. And Expanded Ed.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed rev"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "new Ed., Rev. And Expanded.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed rev"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "new Edition.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed rev"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "new Paperback Edition.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed rev"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "new Rev. Ed.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed rev"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "rev. And Updated)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed rev"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "rev. Ed. Upd. With A New Preface.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed rev"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "rev. Ed. With A New Preface.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed rev"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "rev. English Ed.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed rev"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "rev.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed rev"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "revised And Expanded Edition.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed rev"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "second Edition, Completely Revised And Updated.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 2 rev"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "second Edition, Corrected 7th Printing)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 2 rev"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "sixth Edition, 2016.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 6"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "tenth Edition.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 10"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "third Edition, 2015.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 3"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "twenty First Edition.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 21"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "updated Ed. With A New Preface /)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed rev"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "updated Edition.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed rev"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "volume Eight ,)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 8"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "volume Four,)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 4"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "volume One,)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 1"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "volume Three /) "
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 3"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "volume Vii,)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 7"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "volume Xx /)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 20"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Temp Title 2",
          "expression": "value",
          "columnName": "Temp Title 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "1st Mariner Books Ed.)",
                "l": "1st Mariner Books Ed.)"
              }
            },
            {
              "v": {
                "v": "standard Text Ed.)",
                "l": "standard Text Ed.)"
              }
            },
            {
              "v": {
                "v": "first Texas A&m University Press Edition.)",
                "l": "first Texas A&m University Press Edition.)"
              }
            },
            {
              "v": {
                "v": "1st Houghton Mifflin Pbk. Ed.)",
                "l": "1st Houghton Mifflin Pbk. Ed.)"
              }
            },
            {
              "v": {
                "v": "comprehensive Ed.)",
                "l": "comprehensive Ed.)"
              }
            },
            {
              "v": {
                "v": "samuel French Acting Edition.)",
                "l": "samuel French Acting Edition.)"
              }
            },
            {
              "v": {
                "v": "english Language Edition.)",
                "l": "english Language Edition.)"
              }
            },
            {
              "v": {
                "v": "1st Electronic Reading Ed.)",
                "l": "1st Electronic Reading Ed.)"
              }
            },
            {
              "v": {
                "v": "first Wings Press Edition.)",
                "l": "first Wings Press Edition.)"
              }
            },
            {
              "v": {
                "v": "1st Pbk. Ed.)",
                "l": "1st Pbk. Ed.)"
              }
            },
            {
              "v": {
                "v": "first Harvard University Press Edition.)",
                "l": "first Harvard University Press Edition.)"
              }
            },
            {
              "v": {
                "v": "1st Da Capo Press Ed.)",
                "l": "1st Da Capo Press Ed.)"
              }
            },
            {
              "v": {
                "v": "desktop Ed.)",
                "l": "desktop Ed.)"
              }
            },
            {
              "v": {
                "v": "oxford University Press Pbk.)",
                "l": "oxford University Press Pbk.)"
              }
            },
            {
              "v": {
                "v": "annotated Ed.)",
                "l": "annotated Ed.)"
              }
            },
            {
              "v": {
                "v": "critical Edition.)",
                "l": "critical Edition.)"
              }
            },
            {
              "v": {
                "v": "english Language Ed.)",
                "l": "english Language Ed.)"
              }
            },
            {
              "v": {
                "v": "taylor & Francis E Library Ed.)",
                "l": "taylor & Francis E Library Ed.)"
              }
            },
            {
              "v": {
                "v": "paperback Edition.)",
                "l": "paperback Edition.)"
              }
            },
            {
              "v": {
                "v": "first U.S. Edition.)",
                "l": "first U.S. Edition.)"
              }
            },
            {
              "v": {
                "v": "concise Pbk. Ed.)",
                "l": "concise Pbk. Ed.)"
              }
            },
            {
              "v": {
                "v": "digital Ed.)",
                "l": "digital Ed.)"
              }
            },
            {
              "v": {
                "v": "american Ed.)",
                "l": "american Ed.)"
              }
            },
            {
              "v": {
                "v": "1st English Ed.)",
                "l": "1st English Ed.)"
              }
            },
            {
              "v": {
                "v": "first Mariner Books Edition.)",
                "l": "first Mariner Books Edition.)"
              }
            },
            {
              "v": {
                "v": "1st Paperback Ed.)",
                "l": "1st Paperback Ed.)"
              }
            },
            {
              "v": {
                "v": "first Tcg Edition.)",
                "l": "first Tcg Edition.)"
              }
            },
            {
              "v": {
                "v": "online Only Edition.)",
                "l": "online Only Edition.)"
              }
            },
            {
              "v": {
                "v": "1a. Ed. Virtual.)",
                "l": "1a. Ed. Virtual.)"
              }
            },
            {
              "v": {
                "v": "dover Ed.)",
                "l": "dover Ed.)"
              }
            },
            {
              "v": {
                "v": "first American Edition.)",
                "l": "first American Edition.)"
              }
            },
            {
              "v": {
                "v": "del Rey Trade Pbk. Ed.)",
                "l": "del Rey Trade Pbk. Ed.)"
              }
            },
            {
              "v": {
                "v": "dover Edition.)",
                "l": "dover Edition.)"
              }
            },
            {
              "v": {
                "v": "english Edition.)",
                "l": "english Edition.)"
              }
            },
            {
              "v": {
                "v": "first Simon & Schuster Hardcover Edition.)",
                "l": "first Simon & Schuster Hardcover Edition.)"
              }
            },
            {
              "v": {
                "v": "1st Counterpoint Pbk. Ed.)",
                "l": "1st Counterpoint Pbk. Ed.)"
              }
            },
            {
              "v": {
                "v": "first Scribner Hardcover Edition.)",
                "l": "first Scribner Hardcover Edition.)"
              }
            },
            {
              "v": {
                "v": "1st Da Capo Press Pbk. Ed.)",
                "l": "1st Da Capo Press Pbk. Ed.)"
              }
            },
            {
              "v": {
                "v": "first Scribner Trade Paperback Edition.)",
                "l": "first Scribner Trade Paperback Edition.)"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Temp Title 2 using expression null"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "[update].)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "rev ed"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "1. Auflage.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 1"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "1)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 1"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "1st.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 1"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "1std.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 1"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "2,)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 2"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "2016 /) "
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 2016"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "28) "
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 28"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "20th Ann. Ed.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "20 ann ed"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "20th Anniversary Ed.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "20 ann ed"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "25th Anniversary Ed.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "25 ann ed"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "7th U.S. Ed.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 7"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "94th Annual Ed.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 94"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "abridged And Updated Ed.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed rev"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "annotated Script Edition.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": ""
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "band 16,)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 16"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "band Viii, Faszikel 2,)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 8"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "band Viii, Vierundzwanaigster Gesang,)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 8"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "band Viii,)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 8"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "bicentennial Ed.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "bicentennial ed"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "centenary Ed.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "centenary ed"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "centenary Edition.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "centenary ed"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "CHECK 2"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 2"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "first Report)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 1"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "grade 2)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 2"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "iii,)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 3"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "index To Volumes I Xx /)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 1-20"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "number 34 /)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 34"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "one /)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 1"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "part 3,)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 3"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "part A) "
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 1"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "part B"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 2"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "part I,)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 1"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "pbk. Ed.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": ""
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "phase I Report /)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 1"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "phase Ii Report /)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 2"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "report 1)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 1"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "report 2  C4isr)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 2"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "rev. And Expanded 10th Anniversary Ed. /)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "10 ann ed rev"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "rev. Ed., [10th Anniversary Ed.])"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "10 ann ed rev"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "revised And Expanded 10th Anniversary Ed.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "10 ann ed rev"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "twenty Fifth Anniversary Edition.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "25 ann ed"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "textkritische Ausg.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": ""
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "volume Five, Part One,)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 5-1"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "volume Five, Part Two,)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 5-2"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "volume Four, Part 2,)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 4-2"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "volume Seven, Part 1,)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 7-1"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "volume Seven, Part 2,)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 7-2"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "volume Six, Part Two,)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 6-2"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Temp Title 2",
    "expression": "value",
    "edits": [
      {
        "from": [
          "[tome 2.3, Livres Ii Iv])"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 2-3"
      }
    ],
    "description": "Mass edit cells in column Temp Title 2"
  }
]"""
messagebox.showinfo(title="Instructions", message="Perform clustering on \"Temp Title 3\".")
"""[
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "Temp Title 3",
    "expression": "value",
    "edits": [
      {
        "from": [
          "1st Ed.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 1"
      }
    ],
    "description": "Mass edit cells in column Temp Title 3"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "Temp Title 3",
    "expression": "value",
    "edits": [
      {
        "from": [
          "24th Edition.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 24"
      }
    ],
    "description": "Mass edit cells in column Temp Title 3"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "Temp Title 3",
    "expression": "value",
    "edits": [
      {
        "from": [
          "2nd Ed.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 2"
      }
    ],
    "description": "Mass edit cells in column Temp Title 3"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "Temp Title 3",
    "expression": "value",
    "edits": [
      {
        "from": [
          "digital First Edition.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": ""
      }
    ],
    "description": "Mass edit cells in column Temp Title 3"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "Temp Title 3",
    "expression": "value",
    "edits": [
      {
        "from": [
          "english Edition.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": ""
      }
    ],
    "description": "Mass edit cells in column Temp Title 3"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "Temp Title 3",
    "expression": "value",
    "edits": [
      {
        "from": [
          "first Edition.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 1"
      }
    ],
    "description": "Mass edit cells in column Temp Title 3"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "Temp Title 3",
    "expression": "value",
    "edits": [
      {
        "from": [
          "second Edition.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 2"
      }
    ],
    "description": "Mass edit cells in column Temp Title 3"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "Temp Title 3",
    "expression": "value",
    "edits": [
      {
        "from": [
          "third Edition.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "ed 3"
      }
    ],
    "description": "Mass edit cells in column Temp Title 3"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "Temp Title 3",
    "expression": "value",
    "edits": [
      {
        "from": [
          "2011 2012 Ed.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "2011-2012 ed"
      }
    ],
    "description": "Mass edit cells in column Temp Title 3"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "Temp Title 3",
    "expression": "value",
    "edits": [
      {
        "from": [
          "1)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 1"
      }
    ],
    "description": "Mass edit cells in column Temp Title 3"
  },
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [],
      "mode": "record-based"
    },
    "columnName": "Temp Title 3",
    "expression": "value",
    "edits": [
      {
        "from": [
          "2)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "vol 2"
      }
    ],
    "description": "Mass edit cells in column Temp Title 3"
  }
]"""
os.startfile('Organize_UXU01_Output_pt5--Ebook_Central_Specific.json')
messagebox.showinfo(title="Instructions", message="Create a filter for blanks on \"Inexact Title Record Number\" and set it to true. If the titles in the record don't match, change the values in \"Inexact Title Record Number\" with \"toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)\".")
"""[
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Inexact Title Record Number",
          "expression": "isBlank(value)",
          "columnName": "Inexact Title Record Number",
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
          "name": "Inexact Title Record Number",
          "expression": "value",
          "columnName": "Inexact Title Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "10182",
                "l": "10182"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Inexact Title Record Number",
    "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Inexact Title Record Number",
          "expression": "isBlank(value)",
          "columnName": "Inexact Title Record Number",
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
          "name": "Inexact Title Record Number",
          "expression": "value",
          "columnName": "Inexact Title Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "10665",
                "l": "10665"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Inexact Title Record Number",
    "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Inexact Title Record Number",
          "expression": "isBlank(value)",
          "columnName": "Inexact Title Record Number",
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
          "name": "Inexact Title Record Number",
          "expression": "value",
          "columnName": "Inexact Title Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "11148",
                "l": "11148"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Inexact Title Record Number",
    "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Inexact Title Record Number",
          "expression": "isBlank(value)",
          "columnName": "Inexact Title Record Number",
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
          "name": "Inexact Title Record Number",
          "expression": "value",
          "columnName": "Inexact Title Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "1119",
                "l": "1119"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Inexact Title Record Number",
    "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Inexact Title Record Number",
          "expression": "isBlank(value)",
          "columnName": "Inexact Title Record Number",
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
          "name": "Inexact Title Record Number",
          "expression": "value",
          "columnName": "Inexact Title Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "11203",
                "l": "11203"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Inexact Title Record Number",
    "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Inexact Title Record Number",
          "expression": "isBlank(value)",
          "columnName": "Inexact Title Record Number",
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
          "name": "Inexact Title Record Number",
          "expression": "value",
          "columnName": "Inexact Title Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "11211",
                "l": "11211"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Inexact Title Record Number",
    "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Inexact Title Record Number",
          "expression": "isBlank(value)",
          "columnName": "Inexact Title Record Number",
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
          "name": "Inexact Title Record Number",
          "expression": "value",
          "columnName": "Inexact Title Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "1158",
                "l": "1158"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Inexact Title Record Number",
    "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Inexact Title Record Number",
          "expression": "isBlank(value)",
          "columnName": "Inexact Title Record Number",
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
          "name": "Inexact Title Record Number",
          "expression": "value",
          "columnName": "Inexact Title Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "12343",
                "l": "12343"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Inexact Title Record Number",
    "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Inexact Title Record Number",
          "expression": "isBlank(value)",
          "columnName": "Inexact Title Record Number",
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
          "name": "Inexact Title Record Number",
          "expression": "value",
          "columnName": "Inexact Title Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "2253",
                "l": "2253"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Inexact Title Record Number",
    "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Inexact Title Record Number",
          "expression": "isBlank(value)",
          "columnName": "Inexact Title Record Number",
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
          "name": "Inexact Title Record Number",
          "expression": "value",
          "columnName": "Inexact Title Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "238",
                "l": "238"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Inexact Title Record Number",
    "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Inexact Title Record Number",
          "expression": "isBlank(value)",
          "columnName": "Inexact Title Record Number",
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
          "name": "Inexact Title Record Number",
          "expression": "value",
          "columnName": "Inexact Title Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "253",
                "l": "253"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Inexact Title Record Number",
    "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Inexact Title Record Number",
          "expression": "isBlank(value)",
          "columnName": "Inexact Title Record Number",
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
          "name": "Inexact Title Record Number",
          "expression": "value",
          "columnName": "Inexact Title Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "2589",
                "l": "2589"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Inexact Title Record Number",
    "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Inexact Title Record Number",
          "expression": "isBlank(value)",
          "columnName": "Inexact Title Record Number",
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
          "name": "Inexact Title Record Number",
          "expression": "value",
          "columnName": "Inexact Title Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "263",
                "l": "263"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Inexact Title Record Number",
    "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Inexact Title Record Number",
          "expression": "isBlank(value)",
          "columnName": "Inexact Title Record Number",
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
          "name": "Inexact Title Record Number",
          "expression": "value",
          "columnName": "Inexact Title Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "282",
                "l": "282"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Inexact Title Record Number",
    "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Inexact Title Record Number",
          "expression": "isBlank(value)",
          "columnName": "Inexact Title Record Number",
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
          "name": "Inexact Title Record Number",
          "expression": "value",
          "columnName": "Inexact Title Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "3675",
                "l": "3675"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Inexact Title Record Number",
    "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Inexact Title Record Number",
          "expression": "isBlank(value)",
          "columnName": "Inexact Title Record Number",
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
          "name": "Inexact Title Record Number",
          "expression": "value",
          "columnName": "Inexact Title Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "456",
                "l": "456"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Inexact Title Record Number",
    "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Inexact Title Record Number",
          "expression": "isBlank(value)",
          "columnName": "Inexact Title Record Number",
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
          "name": "Inexact Title Record Number",
          "expression": "value",
          "columnName": "Inexact Title Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "7394",
                "l": "7394"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Inexact Title Record Number",
    "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Inexact Title Record Number",
          "expression": "isBlank(value)",
          "columnName": "Inexact Title Record Number",
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
          "name": "Inexact Title Record Number",
          "expression": "value",
          "columnName": "Inexact Title Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "8105",
                "l": "8105"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Inexact Title Record Number",
    "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Inexact Title Record Number",
          "expression": "isBlank(value)",
          "columnName": "Inexact Title Record Number",
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
          "name": "Inexact Title Record Number",
          "expression": "value",
          "columnName": "Inexact Title Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "8528",
                "l": "8528"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Inexact Title Record Number",
    "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Inexact Title Record Number",
          "expression": "isBlank(value)",
          "columnName": "Inexact Title Record Number",
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
          "name": "Inexact Title Record Number",
          "expression": "value",
          "columnName": "Inexact Title Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "8932",
                "l": "8932"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Inexact Title Record Number",
    "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Inexact Title Record Number",
          "expression": "isBlank(value)",
          "columnName": "Inexact Title Record Number",
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
          "name": "Inexact Title Record Number",
          "expression": "value",
          "columnName": "Inexact Title Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "8984",
                "l": "8984"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Inexact Title Record Number",
    "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Inexact Title Record Number",
          "expression": "isBlank(value)",
          "columnName": "Inexact Title Record Number",
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
          "name": "Inexact Title Record Number",
          "expression": "value",
          "columnName": "Inexact Title Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "9993",
                "l": "9993"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Inexact Title Record Number",
    "expression": "grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Inexact Title Record Number using expression grel:toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)"
  }
]"""
os.startfile('Organize_UXU01_Output_pt6--Ebook_Central_Specific.json')
messagebox.showinfo(title="Instructions", message="Create a filter for blanks on \"No Subtitle Record Number\" and set it to true. If the titles in the record don't match, change the values in \"No Subtitle Record Number\" with \"toString(row.record.index)+\"-\"+toString(row.index-row.record.fromRowIndex)\".")
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
          "name": "No Subtitle Record Number",
          "expression": "value",
          "columnName": "No Subtitle Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "10917",
                "l": "10917"
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
  },
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
          "name": "No Subtitle Record Number",
          "expression": "value",
          "columnName": "No Subtitle Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "1356",
                "l": "1356"
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
  },
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
          "name": "No Subtitle Record Number",
          "expression": "value",
          "columnName": "No Subtitle Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "1890",
                "l": "1890"
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
  },
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
          "name": "No Subtitle Record Number",
          "expression": "value",
          "columnName": "No Subtitle Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "1951",
                "l": "1951"
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
  },
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
          "name": "No Subtitle Record Number",
          "expression": "value",
          "columnName": "No Subtitle Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "2217",
                "l": "2217"
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
  },
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
          "name": "No Subtitle Record Number",
          "expression": "value",
          "columnName": "No Subtitle Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "234",
                "l": "234"
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
  },
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
          "name": "No Subtitle Record Number",
          "expression": "value",
          "columnName": "No Subtitle Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "249",
                "l": "249"
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
  },
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
          "name": "No Subtitle Record Number",
          "expression": "value",
          "columnName": "No Subtitle Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "2511",
                "l": "2511"
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
  },
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
          "name": "No Subtitle Record Number",
          "expression": "value",
          "columnName": "No Subtitle Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "278",
                "l": "278"
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
  },
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
          "name": "No Subtitle Record Number",
          "expression": "value",
          "columnName": "No Subtitle Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "3191",
                "l": "3191"
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
  },
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
          "name": "No Subtitle Record Number",
          "expression": "value",
          "columnName": "No Subtitle Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "3287",
                "l": "3287"
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
  },
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
          "name": "No Subtitle Record Number",
          "expression": "value",
          "columnName": "No Subtitle Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "4281",
                "l": "4281"
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
  },
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
          "name": "No Subtitle Record Number",
          "expression": "value",
          "columnName": "No Subtitle Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "4498",
                "l": "4498"
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
  },
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
          "name": "No Subtitle Record Number",
          "expression": "value",
          "columnName": "No Subtitle Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "4616",
                "l": "4616"
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
  },
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
          "name": "No Subtitle Record Number",
          "expression": "value",
          "columnName": "No Subtitle Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "4731",
                "l": "4731"
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
  },
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
          "name": "No Subtitle Record Number",
          "expression": "value",
          "columnName": "No Subtitle Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "4767",
                "l": "4767"
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
  },
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
          "name": "No Subtitle Record Number",
          "expression": "value",
          "columnName": "No Subtitle Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "5896",
                "l": "5896"
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
  },
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
          "name": "No Subtitle Record Number",
          "expression": "value",
          "columnName": "No Subtitle Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "6267",
                "l": "6267"
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
  },
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
          "name": "No Subtitle Record Number",
          "expression": "value",
          "columnName": "No Subtitle Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "6945",
                "l": "6945"
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
  },
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
          "name": "No Subtitle Record Number",
          "expression": "value",
          "columnName": "No Subtitle Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "7750",
                "l": "7750"
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
  },
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
          "name": "No Subtitle Record Number",
          "expression": "value",
          "columnName": "No Subtitle Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "8747",
                "l": "8747"
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
  },
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
          "name": "No Subtitle Record Number",
          "expression": "value",
          "columnName": "No Subtitle Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "9390",
                "l": "9390"
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
  },
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
          "name": "No Subtitle Record Number",
          "expression": "value",
          "columnName": "No Subtitle Record Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "9395",
                "l": "9395"
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
#ToDo: Get list of columns that will need to be moved over to UXU60 OpenRefine project--the pivot happens in the following JSON
os.startfile('Organize_UXU01_Output_pt7--Ebook_Central_Specific.json')
messagebox.showinfo(title="Instructions", message="In record view, create a filter for blanks on \"Record Number 1\" and set it to false. Create a text filter on both \"Record Number 1\" and \"Record Number 2\".")
messagebox.showinfo(title="Instructions", message="Selct \"false\" on the blanks filter for \"Record Number 1\". For the records that match, determine which propriatary ID matches the title and change all values in \"Record Number\" with the propriatary ID to that number.")
"""[
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 1",
          "expression": "value",
          "columnName": "Record Number 1",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "false",
                "l": "false"
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
                "v": "030808190",
                "l": "030808190"
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
    "expression": "grel:if(startsWith(toString(value),\"Ebook Central\"),substring(value,0,indexOf(value,\"::\")+2)+\"951321\",value)",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:if(startsWith(toString(value),\"Ebook Central\"),substring(value,0,indexOf(value,\"::\")+2)+\"951321\",value)"
  }
]"""
messagebox.showinfo(title="Instructions", message="Select each number in the \"Record Number 2\" text filter on at a time. Determine which BIBs have a given propriatary ID, change the value of \"Record Number\" to that ID by filtering on \"BIB Number\", then remove the BIB filter and null \"Ebook Central\" and then null \"Record Number 2\".")
"""[
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
        },
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "value",
          "columnName": "Record Number 1",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "false",
                "l": "false"
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
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "BIB Number",
          "expression": "value",
          "columnName": "BIB Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "030808190",
                "l": "030808190"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        },
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "value",
          "columnName": "Record Number 1",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "false",
                "l": "false"
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
    "expression": "grel:\"Ebook Central::951321\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::951321\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 3303,
                "l": "3303"
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
                "v": "020372573",
                "l": "020372573"
              }
            },
            {
              "v": {
                "v": "030829337",
                "l": "030829337"
              }
            },
            {
              "v": {
                "v": "036694721",
                "l": "036694721"
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
    "expression": "grel:\"Ebook Central::371984\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::371984\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 3303,
                "l": "3303"
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
                "v": "022485946",
                "l": "022485946"
              }
            },
            {
              "v": {
                "v": "036719919",
                "l": "036719919"
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
    "expression": "grel:\"Ebook Central::993561\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::993561\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 3303,
                "l": "3303"
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
                "v": "031038180",
                "l": "031038180"
              }
            },
            {
              "v": {
                "v": "036720121",
                "l": "036720121"
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
    "expression": "grel:\"Ebook Central::1083660\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::1083660\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 3303,
                "l": "3303"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Ebook Central",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Ebook Central using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 3303,
                "l": "3303"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Record Number 2",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number 2 using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 4804,
                "l": "4804"
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
                "v": "035303187",
                "l": "035303187"
              }
            },
            {
              "v": {
                "v": "036719727",
                "l": "036719727"
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
    "expression": "grel:\"Ebook Central::918160\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::918160\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 4804,
                "l": "4804"
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
                "v": "036719767",
                "l": "036719767"
              }
            },
            {
              "v": {
                "v": "035303192",
                "l": "035303192"
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
    "expression": "grel:\"Ebook Central::947601\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::947601\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 4804,
                "l": "4804"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Ebook Central",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Ebook Central using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 4804,
                "l": "4804"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Record Number 2",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number 2 using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 10325,
                "l": "10325"
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
                "v": "037183163",
                "l": "037183163"
              }
            },
            {
              "v": {
                "v": "035303308",
                "l": "035303308"
              }
            },
            {
              "v": {
                "v": "035032697",
                "l": "035032697"
              }
            },
            {
              "v": {
                "v": "037183125",
                "l": "037183125"
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
    "expression": "grel:\"Ebook Central::1882091\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::1882091\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 10325,
                "l": "10325"
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
                "v": "035303309",
                "l": "035303309"
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
    "expression": "grel:\"Ebook Central::1794093\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::1794093\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 10325,
                "l": "10325"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Ebook Central",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Ebook Central using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 10325,
                "l": "10325"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Record Number 2",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number 2 using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 10208,
                "l": "10208"
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
                "v": "035302892",
                "l": "035302892"
              }
            },
            {
              "v": {
                "v": "036695744",
                "l": "036695744"
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
    "expression": "grel:\"Ebook Central::487648\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::487648\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 10208,
                "l": "10208"
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
                "v": "037183151",
                "l": "037183151"
              }
            },
            {
              "v": {
                "v": "034592084",
                "l": "034592084"
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
    "expression": "grel:\"Ebook Central::1840834\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::1840834\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 10208,
                "l": "10208"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Ebook Central",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Ebook Central using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 10208,
                "l": "10208"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Record Number 2",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number 2 using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 2248,
                "l": "2248"
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
                "v": "025126910",
                "l": "025126910"
              }
            },
            {
              "v": {
                "v": "036695934",
                "l": "036695934"
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
    "expression": "grel:\"Ebook Central::4657614\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::4657614\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 2248,
                "l": "2248"
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
                "v": "032013136",
                "l": "032013136"
              }
            },
            {
              "v": {
                "v": "036695965",
                "l": "036695965"
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
    "expression": "grel:\"Ebook Central::4960447\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::4960447\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 2248,
                "l": "2248"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Ebook Central",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Ebook Central using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 2248,
                "l": "2248"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Record Number 2",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number 2 using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 3613,
                "l": "3613"
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
                "v": "036695101",
                "l": "036695101"
              }
            },
            {
              "v": {
                "v": "032598854",
                "l": "032598854"
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
    "expression": "grel:\"Ebook Central::615908\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::615908\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 3613,
                "l": "3613"
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
                "v": "036695100",
                "l": "036695100"
              }
            },
            {
              "v": {
                "v": "032598855",
                "l": "032598855"
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
    "expression": "grel:\"Ebook Central::615902\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::615902\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 3613,
                "l": "3613"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Ebook Central",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Ebook Central using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 3613,
                "l": "3613"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Record Number 2",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number 2 using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 5805,
                "l": "5805"
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
                "v": "036719259",
                "l": "036719259"
              }
            },
            {
              "v": {
                "v": "032080849",
                "l": "032080849"
              }
            },
            {
              "v": {
                "v": "032080848",
                "l": "032080848"
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
    "expression": "grel:\"Ebook Central::240427\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::240427\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 5805,
                "l": "5805"
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
                "v": "036719258",
                "l": "036719258"
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
    "expression": "grel:\"Ebook Central::240426\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::240426\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 5805,
                "l": "5805"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Ebook Central",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Ebook Central using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 5805,
                "l": "5805"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Record Number 2",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number 2 using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 6999,
                "l": "6999"
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
                "v": "036719534",
                "l": "036719534"
              }
            },
            {
              "v": {
                "v": "034157131",
                "l": "034157131"
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
    "expression": "grel:\"Ebook Central::728546\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::728546\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 6999,
                "l": "6999"
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
                "v": "036719533",
                "l": "036719533"
              }
            },
            {
              "v": {
                "v": "034157132",
                "l": "034157132"
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
    "expression": "grel:\"Ebook Central::728471\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::728471\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 6999,
                "l": "6999"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Ebook Central",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Ebook Central using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 6999,
                "l": "6999"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Record Number 2",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number 2 using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 7895,
                "l": "7895"
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
                "v": "036695699",
                "l": "036695699"
              }
            },
            {
              "v": {
                "v": "023804958",
                "l": "023804958"
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
    "expression": "grel:\"Ebook Central::874224\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::874224\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 7895,
                "l": "7895"
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
                "v": "034796376",
                "l": "034796376"
              }
            },
            {
              "v": {
                "v": "030808190",
                "l": "030808190"
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
    "expression": "grel:\"Ebook Central::951321\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::951321\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 7895,
                "l": "7895"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Ebook Central",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Ebook Central using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 7895,
                "l": "7895"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Record Number 2",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number 2 using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 2134,
                "l": "2134"
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
                "v": "037183193",
                "l": "037183193"
              }
            },
            {
              "v": {
                "v": "033325517",
                "l": "033325517"
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
    "expression": "grel:\"Ebook Central::1895824\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::1895824\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 2134,
                "l": "2134"
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
                "v": "036855676",
                "l": "036855676"
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
    "expression": "grel:\"Ebook Central::4455265\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::4455265\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 2134,
                "l": "2134"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Ebook Central",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Ebook Central using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 2134,
                "l": "2134"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Record Number 2",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number 2 using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 8944,
                "l": "8944"
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
                "v": "037183598",
                "l": "037183598"
              }
            },
            {
              "v": {
                "v": "034650631",
                "l": "034650631"
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
    "expression": "grel:\"Ebook Central::4523847\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::4523847\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 8944,
                "l": "8944"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Ebook Central",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Ebook Central using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 8944,
                "l": "8944"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Record Number 2",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number 2 using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 9471,
                "l": "9471"
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
                "v": "037026615",
                "l": "037026615"
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
    "expression": "grel:\"Ebook Central::5824668\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::5824668\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 9471,
                "l": "9471"
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
                "v": "037497728",
                "l": "037497728"
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
    "expression": "grel:\"Ebook Central::5878292\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::5878292\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 9471,
                "l": "9471"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Ebook Central",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Ebook Central using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 9471,
                "l": "9471"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Record Number 2",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number 2 using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 8997,
                "l": "8997"
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
                "v": "036810109",
                "l": "036810109"
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
    "expression": "grel:\"Ebook Central::1808781\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::1808781\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 8997,
                "l": "8997"
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
                "v": "036848159",
                "l": "036848159"
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
    "expression": "grel:\"Ebook Central::4940426\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::4940426\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 8997,
                "l": "8997"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Ebook Central",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Ebook Central using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 8997,
                "l": "8997"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Record Number 2",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number 2 using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 8671,
                "l": "8671"
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
                "v": "036810107",
                "l": "036810107"
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
    "expression": "grel:\"Ebook Central::4741076\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::4741076\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 8671,
                "l": "8671"
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
                "v": "036810113",
                "l": "036810113"
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
    "expression": "grel:\"Ebook Central::1931604\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::1931604\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 8671,
                "l": "8671"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Ebook Central",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Ebook Central using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 8671,
                "l": "8671"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Record Number 2",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number 2 using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 2749,
                "l": "2749"
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
                "v": "037182928",
                "l": "037182928"
              }
            },
            {
              "v": {
                "v": "033802155",
                "l": "033802155"
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
    "expression": "grel:\"Ebook Central::1652169\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::1652169\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 2749,
                "l": "2749"
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
                "v": "033254284",
                "l": "033254284"
              }
            },
            {
              "v": {
                "v": "037202570",
                "l": "037202570"
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
    "expression": "grel:\"Ebook Central::270457\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::270457\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 2749,
                "l": "2749"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Ebook Central",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Ebook Central using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 2749,
                "l": "2749"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Record Number 2",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number 2 using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 748,
                "l": "748"
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
                "v": "037182824",
                "l": "037182824"
              }
            },
            {
              "v": {
                "v": "033118104",
                "l": "033118104"
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
    "expression": "grel:\"Ebook Central::1584082\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::1584082\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 748,
                "l": "748"
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
                "v": "037182725",
                "l": "037182725"
              }
            },
            {
              "v": {
                "v": "033118119",
                "l": "033118119"
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
    "expression": "grel:\"Ebook Central::1378784\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::1378784\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 748,
                "l": "748"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Ebook Central",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Ebook Central using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 748,
                "l": "748"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Record Number 2",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number 2 using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 10894,
                "l": "10894"
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
                "v": "034208538",
                "l": "034208538"
              }
            },
            {
              "v": {
                "v": "034592122",
                "l": "034592122"
              }
            },
            {
              "v": {
                "v": "037183295",
                "l": "037183295"
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
    "expression": "grel:\"Ebook Central::2194890\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::2194890\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 10894,
                "l": "10894"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Ebook Central",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Ebook Central using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 10894,
                "l": "10894"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Record Number 2",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number 2 using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 1711,
                "l": "1711"
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
                "v": "036810110",
                "l": "036810110"
              }
            },
            {
              "v": {
                "v": "037228798",
                "l": "037228798"
              }
            },
            {
              "v": {
                "v": "036810112",
                "l": "036810112"
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
    "expression": "grel:\"Ebook Central::1769040\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::1769040\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 1711,
                "l": "1711"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Ebook Central",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Ebook Central using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 1711,
                "l": "1711"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Record Number 2",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number 2 using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 10963,
                "l": "10963"
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
                "v": "034636858",
                "l": "034636858"
              }
            },
            {
              "v": {
                "v": "037183301",
                "l": "037183301"
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
    "expression": "grel:\"Ebook Central::3035208\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::3035208\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 10963,
                "l": "10963"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Ebook Central",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Ebook Central using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 10963,
                "l": "10963"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Record Number 2",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number 2 using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 1181,
                "l": "1181"
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
                "v": "036695787",
                "l": "036695787"
              }
            },
            {
              "v": {
                "v": "035303347",
                "l": "035303347"
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
    "expression": "grel:\"Ebook Central::2056249\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::2056249\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 1181,
                "l": "1181"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Ebook Central",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Ebook Central using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 1181,
                "l": "1181"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Record Number 2",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number 2 using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 4125,
                "l": "4125"
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
                "v": "021325065",
                "l": "021325065"
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
    "expression": "grel:\"Ebook Central::3375635\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::3375635\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 4125,
                "l": "4125"
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
                "v": "021560792",
                "l": "021560792"
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
    "expression": "grel:\"Ebook Central::3375698\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::3375698\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 4125,
                "l": "4125"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Ebook Central",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Ebook Central using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 4125,
                "l": "4125"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Record Number 2",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number 2 using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 726,
                "l": "726"
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
                "v": "035303349",
                "l": "035303349"
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
    "expression": "grel:\"Ebook Central::4416046\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::4416046\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 726,
                "l": "726"
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
                "v": "036695815",
                "l": "036695815"
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
    "expression": "grel:\"Ebook Central::5247984\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::5247984\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 726,
                "l": "726"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Ebook Central",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Ebook Central using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 726,
                "l": "726"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Record Number 2",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number 2 using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 7608,
                "l": "7608"
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
                "v": "034398730",
                "l": "034398730"
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
    "expression": "grel:\"Ebook Central::4428956\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::4428956\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 7608,
                "l": "7608"
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
                "v": "036695816",
                "l": "036695816"
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
    "expression": "grel:\"Ebook Central::5247985\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::5247985\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 7608,
                "l": "7608"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Ebook Central",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Ebook Central using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 7608,
                "l": "7608"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Record Number 2",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number 2 using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 8871,
                "l": "8871"
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
                "v": "022195855",
                "l": "022195855"
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
    "expression": "grel:\"Ebook Central::231740\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::231740\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 8871,
                "l": "8871"
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
                "v": "023089420",
                "l": "023089420"
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
    "expression": "grel:\"Ebook Central::231741\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::231741\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 8871,
                "l": "8871"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Ebook Central",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Ebook Central using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 8871,
                "l": "8871"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Record Number 2",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number 2 using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 17034,
                "l": "17034"
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
                "v": "036984692",
                "l": "036984692"
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
    "expression": "grel:\"Ebook Central::5283177\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::5283177\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 17034,
                "l": "17034"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Ebook Central",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Ebook Central using expression null"
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number 1",
          "expression": "isBlank(value)",
          "columnName": "Record Number 1",
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
          "name": "Record Number 2",
          "expression": "value",
          "columnName": "Record Number 2",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": 17034,
                "l": "17034"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Record Number 2",
    "expression": "null",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number 2 using expression null"
  }
]"""
os.startfile('Organize_UXU01_Output_pt8--Ebook_Central_Specific.json')
messagebox.showinfo(title="Instructions", message="Create text filter on \"ISBN Values 1\" and select each string of IDs individually. Determine which Ebook Central ID is the best match for that BIB, then change \"Record Number\" to \"Ebook Central::\" plus that ID.")
"""[
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "ISBN Value 1",
          "expression": "value",
          "columnName": "ISBN Value 1",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "1121224|845138",
                "l": "1121224|845138"
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
    "expression": "grel:\"Ebook Central::1121224\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::1121224\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "ISBN Value 1",
          "expression": "value",
          "columnName": "ISBN Value 1",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "1698569|6165086",
                "l": "1698569|6165086"
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
    "expression": "grel:\"Ebook Central::1698569\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::1698569\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "ISBN Value 1",
          "expression": "value",
          "columnName": "ISBN Value 1",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "3053278|3052071",
                "l": "3053278|3052071"
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
                "v": "020430629",
                "l": "020430629"
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
    "expression": "grel:\"Ebook Central::3052071\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::3052071\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "ISBN Value 1",
          "expression": "value",
          "columnName": "ISBN Value 1",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "3053278|3052071",
                "l": "3053278|3052071"
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
                "v": "021459401",
                "l": "021459401"
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
    "expression": "grel:\"Ebook Central::3053278\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::3053278\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "ISBN Value 1",
          "expression": "value",
          "columnName": "ISBN Value 1",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "4197994|6163852",
                "l": "4197994|6163852"
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
    "expression": "grel:\"Ebook Central::4197994\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::4197994\""
  }
]"""
os.startfile('Organize_UXU01_Output_pt9--Ebook_Central_Specific.json')
messagebox.showinfo(title="Instructions", message="Create custom filter on \"Record Number\" with the expression \"and(contains(value,\"|\"),contains(value,\"::\"))\". For the BIBs that are true, determine which Ebook Central ID to keep.")
"""[
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number",
          "expression": "grel:and(contains(value,\"|\"),contains(value,\"::\"))",
          "columnName": "Record Number",
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
                "v": "031147384",
                "l": "031147384"
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
    "expression": "grel:\"Ebook Central::4953675\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::4953675\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number",
          "expression": "grel:and(contains(value,\"|\"),contains(value,\"::\"))",
          "columnName": "Record Number",
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
                "v": "032986539",
                "l": "032986539"
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
    "expression": "grel:\"Credo\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Credo\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number",
          "expression": "grel:and(contains(value,\"|\"),contains(value,\"::\"))",
          "columnName": "Record Number",
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
messagebox.showwarning(title="Fill Down", message="The JSON fills down all the columns, so it needs to know what columns it has.")
messagebox.showwarning(title="Fill Up and Down Ticklers", message="The JSON fills up and down then blanks down the TKR columns as well, so in addition to needing to know how many to do, a loop needs to be created.")
#ToDo: Get list of columns to pull from UXU01 OpenRefine project and create loop to load them into this project with the last column being the first JSON object so all the object can use the same column insert index
os.startfile('Match_Duplicate_Records--Ebook_Central_Specific.json')
messagebox.showinfo(title="Instructions", message="Set text filter on \"Ebook Central IDs\" to false and create a text filter for \"HOL Number\". For all records that match, select the HOL numbers, change the view to rows, clear the filter on \"Ebook Central IDs\", and change the value of \"Record Number\" to match the URL with \"\"Ebook Central::\"+match(cells[\"Ebook Central BIB URLs\"].value,/https:\\/\\/ebookcentral\\.proquest\\.com\\/lib\\/fsu\\/detail\\.action\\?docID=(\\d*)/)[0])\". Confirm that the record in question doesn't have replacement characters in any of the titles or that all of the titles have TKRs for other platforms; if they do, make the appropriate changes or removals now.")
"""[
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "HOL Number",
          "expression": "value",
          "columnName": "HOL Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "110102929",
                "l": "110102929"
              }
            },
            {
              "v": {
                "v": "108930129",
                "l": "108930129"
              }
            },
            {
              "v": {
                "v": "110016991",
                "l": "110016991"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "Record Number",
    "expression": "grel:\"Ebook Central::\"+match(cells[\"Ebook Central BIB URLs\"].value,/https:\\/\\/ebookcentral\\.proquest\\.com\\/lib\\/fsu\\/detail\\.action\\?docID=(\\d*)/)[0])",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Record Number using expression grel:\"Ebook Central::\"+match(cells[\"Ebook Central BIB URLs\"].value,/https:\\/\\/ebookcentral\\.proquest\\.com\\/lib\\/fsu\\/detail\\.action\\?docID=(\\d*)/)[0])"
  }
]"""
messagebox.showinfo(title="Instructions", message="Set text filter on \"Replacement Character in Title\" to true and edit the titles as needed to match the 245 fields in the BIBs of origin.")
"""[
  {
    "op": "core/mass-edit",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Replacement Character in Title",
          "expression": "value",
          "columnName": "Replacement Character in Title",
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
          "A Postcolonial Critique of the Linde et al. v. Arab Bank, PLC â€œTerrorismâ€� Bank Cases"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "A Postcolonial Critique of the Linde et al. v. Arab Bank, PLC \"Terrorism\" Bank Cases"
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
          "name": "Replacement Character in Title",
          "expression": "value",
          "columnName": "Replacement Character in Title",
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
          "Letters of a Sufi scholar: the correspondence of Ê»Abd al-GhanÄ« al-NÄ�bulusÄ« (1641-1731)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Letters of a Sufi scholar: the correspondence of ʻAbd al-Ghanī al-Nābulusī (1641-1731)"
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
          "name": "Replacement Character in Title",
          "expression": "value",
          "columnName": "Replacement Character in Title",
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
          "New Mexico and the PimeriÌ�a Alta: the colonial period in the American Southwest"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "New Mexico and the Pimería Alta: the colonial period in the American Southwest"
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
          "name": "Replacement Character in Title",
          "expression": "value",
          "columnName": "Replacement Character in Title",
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
          "â€œRomanticismâ€� â€“ and Byron. (ed=1st ed.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "“Romanticism” – and Byron. (ed=1st ed.)"
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
          "name": "Replacement Character in Title",
          "expression": "value",
          "columnName": "Replacement Character in Title",
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
          "Poetry, the geometry of the living substance: four essays on Ã�gnes Nemes Nagy"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Poetry, the geometry of the living substance: four essays on Ágnes Nemes Nagy"
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
          "name": "Replacement Character in Title",
          "expression": "value",
          "columnName": "Replacement Character in Title",
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
          "Poetry, the Geometry of the Living Substance: Four Essays on Ã�gnes Nemes Nagy. (ed=1st ed.)"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Poetry, the Geometry of the Living Substance: Four Essays on Ágnes Nemes Nagy. (ed=1st ed.)"
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
          "name": "Replacement Character in Title",
          "expression": "value",
          "columnName": "Replacement Character in Title",
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
          "HÅ�ryÅ«ji reconsidered: [HÅ�ryÅ«ji no saikeutÅ�]"
        ],
        "fromBlank": false,
        "fromError": false,
        "to": "Hōryūji reconsidered: [Hōryūji no saikeutō]"
      }
    ],
    "description": "Mass edit cells in column Title"
  },
]"""
messagebox.showinfo(title="Instructions", message="Set filter for blanks on \"Record Number\" to true and crteate text filter on \"TKRs\" and \"Record Number\". For each value in the text filter on \"TKRs\", use filtering by \"Record Number\" to remove the records were all the rows have a tickler for another platform.")
"""[
  {
    "op": "core/row-removal",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "TKRs",
          "expression": "value",
          "columnName": "TKRs",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "CredoReference",
                "l": "CredoReference"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        },
        {
          "type": "list",
          "name": "Record Number",
          "expression": "isBlank(value)",
          "columnName": "Record Number",
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
                "v": "4947",
                "l": "4947"
              }
            },
            {
              "v": {
                "v": "8184",
                "l": "8184"
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
  },
  {
    "op": "core/row-removal",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "TKRs",
          "expression": "value",
          "columnName": "TKRs",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "Oxford Quick Reference",
                "l": "Oxford Quick Reference"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        },
        {
          "type": "list",
          "name": "Record Number",
          "expression": "isBlank(value)",
          "columnName": "Record Number",
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
    "description": "Remove rows"
  },
  {
    "op": "core/row-removal",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "TKRs",
          "expression": "value",
          "columnName": "TKRs",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "Oxford Reference Premium",
                "l": "Oxford Reference Premium"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        },
        {
          "type": "list",
          "name": "Record Number",
          "expression": "isBlank(value)",
          "columnName": "Record Number",
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
    "description": "Remove rows"
  },
  {
    "op": "core/row-removal",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "TKRs",
          "expression": "value",
          "columnName": "TKRs",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "SageResearchMethods",
                "l": "SageResearchMethods"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        },
        {
          "type": "list",
          "name": "Record Number",
          "expression": "isBlank(value)",
          "columnName": "Record Number",
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
                "v": "67",
                "l": "67"
              }
            },
            {
              "v": {
                "v": "8102",
                "l": "8102"
              }
            },
            {
              "v": {
                "v": "4650",
                "l": "4650"
              }
            },
            {
              "v": {
                "v": "382",
                "l": "382"
              }
            },
            {
              "v": {
                "v": "690",
                "l": "690"
              }
            },
            {
              "v": {
                "v": "692",
                "l": "692"
              }
            },
            {
              "v": {
                "v": "1866",
                "l": "1866"
              }
            },
            {
              "v": {
                "v": "693",
                "l": "693"
              }
            },
            {
              "v": {
                "v": "276",
                "l": "276"
              }
            },
            {
              "v": {
                "v": "157",
                "l": "157"
              }
            },
            {
              "v": {
                "v": "466",
                "l": "466"
              }
            },
            {
              "v": {
                "v": "104",
                "l": "104"
              }
            },
            {
              "v": {
                "v": "654",
                "l": "654"
              }
            },
            {
              "v": {
                "v": "567",
                "l": "567"
              }
            },
            {
              "v": {
                "v": "2189",
                "l": "2189"
              }
            },
            {
              "v": {
                "v": "338",
                "l": "338"
              }
            },
            {
              "v": {
                "v": "724",
                "l": "724"
              }
            },
            {
              "v": {
                "v": "725",
                "l": "725"
              }
            },
            {
              "v": {
                "v": "2707",
                "l": "2707"
              }
            },
            {
              "v": {
                "v": "803",
                "l": "803"
              }
            },
            {
              "v": {
                "v": "4207",
                "l": "4207"
              }
            },
            {
              "v": {
                "v": "11402",
                "l": "11402"
              }
            },
            {
              "v": {
                "v": "4649",
                "l": "4649"
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

#Subsection: Determine Which HOL Records to Keep
messagebox.showinfo(title="Instructions", message="Create spreadsheet \"Cross-Reference.xlsx\" with columns \"BIB with ACQ\" listing the BIBs with ACQ records attached and \"Ebook Central Owned\" with the Ebook Central IDs of the titles owned on that platform. The BIBs be nine-digit text strings, the IDs should be formatted as text.")
messagebox.showwarning(title="Deduping HOLs", message="HOLs with multiple non-unique record numbers have them combined in \"Record Number\" divided by pipes. This situation didn't acutally occur with these titles; there may be a better way to handle it.")
os.startfile('Select_HOL_to_Keep_pt1--Ebook_Central_Specific.json')
messagebox.showinfo(title="Instructions", message="Create custom filter on \"Record Number\" with \"toString(row.record.toRowIndex-row.record.fromRowIndex)\". Select each value greater than three and, for records where the values of \"Duplication\" are all the same, fill up and down those values.")
messagebox.showinfo(title="Instructions", message="Create blanks filters on both \"Record Number\" and \"Duplication\" and set them to true. Change the values in \"Duplication\" for these records, using \"Multiple\" when some, but not all, of the HOL in a record have the same BIB or sublibrary.")
"""[
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Duplication",
          "expression": "value",
          "columnName": "Duplication",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [],
          "selectBlank": true,
          "selectError": false
        },
        {
          "type": "list",
          "name": "Record Number",
          "expression": "isBlank(value)",
          "columnName": "Record Number",
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
                "v": "Ebook Central::438603",
                "l": "Ebook Central::438603"
              }
            },
            {
              "v": {
                "v": "Ebook Central::1168042",
                "l": "Ebook Central::1168042"
              }
            },
            {
              "v": {
                "v": "Ebook Central::647437",
                "l": "Ebook Central::647437"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Duplication",
    "expression": "grel:\"Different BIB, Multiple Sublibrary\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Duplication using expression grel:\"Different BIB, Multiple Sublibrary\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Duplication",
          "expression": "value",
          "columnName": "Duplication",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [],
          "selectBlank": true,
          "selectError": false
        },
        {
          "type": "list",
          "name": "Record Number",
          "expression": "isBlank(value)",
          "columnName": "Record Number",
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
                "v": "Ebook Central::224643",
                "l": "Ebook Central::224643"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Duplication",
    "expression": "grel:\"Multiple BIB, Different Sublibrary\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Duplication using expression grel:\"Multiple BIB, Different Sublibrary\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Duplication",
          "expression": "value",
          "columnName": "Duplication",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [],
          "selectBlank": true,
          "selectError": false
        },
        {
          "type": "list",
          "name": "Record Number",
          "expression": "isBlank(value)",
          "columnName": "Record Number",
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
                "v": "Ebook Central::180253",
                "l": "Ebook Central::180253"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "record-based"
    },
    "columnName": "Duplication",
    "expression": "grel:\"Multiple BIB, Same Sublibrary\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column Duplication using expression grel:\"Multiple BIB, Same Sublibrary\""
  }
]"""
messagebox.showwarning(title="Changing \"Record Number\"", message="A method for updating \"Record Number\" for those records changed in the previous step needs to be developed. With Ebook Central, all of the records requiring changes had Ebook Central IDs.")
messagebox.showinfo(title="Instructions", message="Remove the blanks filter on \"Duplication\". Create text filter on \"HOL Sublibrary\" and select all values but \"FSUER\", then invert. Use \"Transform...\" to change the value of the matching records to \"Only FSUER HOL\".")
"""[
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "Record Number",
          "expression": "isBlank(value)",
          "columnName": "Record Number",
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
          "name": "HOL Sublibrary",
          "expression": "value",
          "columnName": "HOL Sublibrary",
          "invert": true,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "FSOAR",
                "l": "FSOAR"
              }
            },
            {
              "v": {
                "v": "FSLAW",
                "l": "FSLAW"
              }
            },
            {
              "v": {
                "v": "FSUDC",
                "l": "FSUDC"
              }
            },
            {
              "v": {
                "v": "FSUPA",
                "l": "FSUPA"
              }
            },
            {
              "v": {
                "v": "FSUSC",
                "l": "FSUSC"
              }
            },
            {
              "v": {
                "v": "FSUPC",
                "l": "FSUPC"
              }
            },
            {
              "v": {
                "v": "FSULN",
                "l": "FSULN"
              }
            },
            {
              "v": {
                "v": "FSULC",
                "l": "FSULC"
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
# "Record Number" formats
## Ebook Central::<Ebook Central ID> = title matched to an Ebook Central ID
## HOL <HOL Number> without ID = HOL is only one for that title
## Duplicate <sublibrary code> Sublibrary for BIB <BIB number> = multiple HOLs for same sublibrary on same BIB record found (thoretically, shouldn't be possible) {Same BIB, Same Sublibrary}
## BIBs <list of BIB numbers> Match = HOLs for the same sublibrary found on multiple BIB records {Different BIB, Same Sublibrary}
## Different Sublibraries for BIB <BIB Number> = HOLs found on same BIB record but for different sublibraries {Same BIB, Different Sublibrary}
## BIBs <list of BIB numbers> Match with Different Sublibraries = HOLs for different sublibraries found on different BIB records {Different BIB, Different Sublibrary}
os.startfile('Select_HOL_to_Keep_pt2--Ebook_Central_Specific.json')





messagebox.showinfo(title="Instructions", message="Set a blank filter on \"Title Check 1\" to false, then download the results to Excel. If the titles can be confirmed as matches, delete from the spreadsheet. Consider titles that have no edition info and titles that are first editions as matches.")
messagebox.showinfo(title="Instructions", message="Upload that Excel worksheet to OpenRefine as \"Title Mismatches\".")
messagebox.showwarning(title="Evlauating in Excel", message="The evaluating is done in Excel to avoid editing individual cells, which isn't captured by the extract functionality. When this title matching gets moved to the more appropriate place earlier in the process, it probably won't be needed.")
os.startfile('Select_HOL_to_Keep_pt3--Ebook_Central_Specific.json')
messagebox.showinfo(title="Instructions", message="On column \"Keep HOL?\" create custom facet \"toString(or(startsWith(value,\"TRUE\"),startsWith(value,\"FALSE\")))\".")
messagebox.showinfo(title="Instructions", message="On column \"HOL Test\" create custom facet \"toString(and(contains(value,\"No ACQ for BIB\"),contains(value,\"BIB has ACQ\")))\".")
# Multiple HOL where all have ACQ

#ToDo: Make INDX forst column
#ToDo: Do checks on which row in each record to keep
#ToDo: Final format--Records by Ebook Central ID with BIB and HOL combinations


#Section: Create Update Files For Records to Remain
#Subsection: If New 856$u Needed, Supply It

#Subsection: If TKR Needed, Supply It


#Section: Remove Unneeded Records
#Subsection: If Other HOLs Attached to BIB, Delete FSUER HOL

#Subsection: If FSUER HOL is Only HOL, Delete HOL and BIB