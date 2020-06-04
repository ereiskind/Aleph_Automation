# Process for handling having multiple records for a given owned title in UXU01 and possibly UXU60

import os
from tkinter import messagebox

#Section: Determine What BIBs Have ACQ Records
#Subsection: Collect all possible BIB numbers for the platform/collection in question

#Subsection: Send those BIBs to cataloging to have them check which ones have ACQ records attached


#Section: Collect BIB Information
#Subsection: Pull Info from Aleph
# For BIBs, print-03 Aleph sequential of 856 fields
# For BIBs, manage-70 for BIB-to-HOL
# For HOLs, print-03 Aleph sequential of TKR, LKR, STA

#Subsection: Organize Aleph Output
# before JSON launch: tkinter.messagebox.showwarning(title=None, message=None, **options) that JSON is for Ebook Central


#Section: Determine Which Records to Keep
#Subsection: Match Duplicate BIB Records

#Subsection: Determine Which BIB Records to Keep


#Section: Create Update Files For Records to Remain
#Subsection: If New 856$u Needed, Supply It

#Subsection: If TKR Needed, Supply It


#Section: Remove Unneeded Records
#Subsection: If Other HOLs Attached to BIB, Delete FSUER HOL

#Subsection: If FSUER HOL is Only HOL, Delete HOL and BIB