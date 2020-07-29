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
#Alert: The title cleaning in Match_Duplicate_Records--Ebook_Central_Specific.json and subsequent JSONs should be moved here
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
messagebox.showinfo(title="Instructions", message="Manually check records that have items in a potential \"Temp Title 3\". If the titles are matches, null the values in all \"Title Check\" columns.")
#ToDo: Get list of columns that will need to be moved over to UXU60 OpenRefine project

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
messagebox.showinfo(title="Instructions", message="Add text filter to \"Replacement Character in Title\" and edit the titles to remove the replacement characters.")
os.startfile('Match_Duplicate_Records_pt2--Ebook_Central_Specific.json')
messagebox.showinfo(title="Instructions", message="Create custom text filteron column \"INDX Ebook Central\" with \"toString(startsWith(value,\"*\"))\" and set to true. For all titles in the matching records, manually determine the appropriate ID and change the value in \"INDX Ebook Central\" to that ID.")
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
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "INDX Ebook Central",
          "expression": "grel:toString(startsWith(value,\"*\"))",
          "columnName": "INDX Ebook Central",
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
          "name": "HOL Number",
          "expression": "value",
          "columnName": "HOL Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "077392679",
                "l": "077392679"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "INDX Ebook Central",
    "expression": "grel:\"3052071\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column INDX Ebook Central using expression grel:\"3052071\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "INDX Ebook Central",
          "expression": "grel:toString(startsWith(value,\"*\"))",
          "columnName": "INDX Ebook Central",
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
          "name": "HOL Number",
          "expression": "value",
          "columnName": "HOL Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "077465248",
                "l": "077465248"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "INDX Ebook Central",
    "expression": "grel:\"3053278\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column INDX Ebook Central using expression grel:\"3053278\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "INDX Ebook Central",
          "expression": "grel:toString(startsWith(value,\"*\"))",
          "columnName": "INDX Ebook Central",
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
          "name": "HOL Number",
          "expression": "value",
          "columnName": "HOL Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "099570882",
                "l": "099570882"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "INDX Ebook Central",
    "expression": "grel:\"1121224\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column INDX Ebook Central using expression grel:\"1121224\""
  },
  {
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "INDX Ebook Central",
          "expression": "grel:toString(startsWith(value,\"*\"))",
          "columnName": "INDX Ebook Central",
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
          "name": "HOL Number",
          "expression": "value",
          "columnName": "HOL Number",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": "100419984",
                "l": "100419984"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "INDX Ebook Central",
    "expression": "grel:\"1698569\"",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column INDX Ebook Central using expression grel:\"1698569\""
  }
]"""

#Subsection: Determine Which HOL Records to Keep
#Alert: These JSONs contain extensive after-the-fact checking that the title matching didn't match unlike titles or match differnt editions or volumes of the same title--this should be moved earlier in the process
messagebox.showinfo(title="Instructions", message="Create spreadsheet \"Cross-Reference.xlsx\" with columns \"BIB with ACQ\" listing the BIBs with ACQ records attached and \"Ebook Central Owned\" with the Ebook Central IDs of the titles owned on that platform. The BIBs be nine-digit text strings, the IDs should be formatted as text.")
messagebox.showwarning(title="Ebook Central and TKRs", message="The second step in this JSON is for reordering columns--that makes it specific to Ebook Central in the column names and the number of TKR columns.")
messagebox.showwarning(title="FSU Sublibraries", message="HOL in sublibraries other than FSUER are removed in the JSON below. This requires selecting all sublibraries other than FSUER.")
messagebox.showwarning(title="Exclusion via TKR", message="The TKRs not matching Ebook Central used to remove records with no Ebook Central HOL are hard coded into the JSON.")
os.startfile('Select_HOL_to_Keep_pt1--Ebook_Central_Specific.json')

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