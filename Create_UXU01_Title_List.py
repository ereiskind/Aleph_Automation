# Generate JSONs to turn UXU01 MARC record in OpenRefine into a title list

import os
import re
import sys
import json
from tkinter import *
from tkinter import ttk

#Section: GUI Template
# For now, decision making GUIs will be generated at the point of need
#ToDo: figure out how to create tkinter variables in a class
#ToDo: determine best way to get GUI variables from class in another module into a script
"""
root_window = Tk()
ttk.Label(root_window, text="something").pack()
something=True
checkbox = ttk.Checkbutton(root_window, text="something", variable=something, onvalue=True, offvalue=False)
checkbox.pack()
root_window.mainloop()
"""


#Section: Functions for Creating the UXU01 Title List
def Paste_Text_Facet_Choices_into_Text_Editor():
    """This uses the default text editor for multi-line input.
    
    VS Code's terminal doen't support the multiline input function sys.stdin.readlines(), so this function allows for multiline input into programs run within VS Code. When the GUI is created, this will be replaced with the text widget.
    """
    os.startfile('Text_Facet_Choices.txt')
    input("Press any key to continue once the file has been saved and closed.")
    TextFacetChoices = []
    
    with open('Text_Facet_Choices.txt', 'r') as InputFile:
        for line in iter(InputFile.readline, ""): #ToDo: determine why iter was used here
            if line.startswith("(blank)"):
                continue # This will keep the line with "(blank)" from being added to the list
            TextFacetChoices.append(line.split("\t")[0]) # This takes only the part of the line before the tab--the tab, the number of occurances, and the newline are removed
        # The lines below are for clearing the file
        InputFile.close()
    
    ClearingFile = open('Text_Facet_Choices.txt', 'w')
    ClearingFile.write("")
    ClearingFile.close
    return TextFacetChoices


def How_Many_Times_Subfields_Appear(ColumnSubfield, ColumnList):
    """This counts the number of subfields and the number of subfields with field numbers.

    The function accepts a subfield formatted for a regex and the list of subfields from OpenRefine and returns a tuple of how many times the subfield is in the list and how many times the subfield is in the list with a field number.
    """
    SubfieldRegex = re.compile(r'.*{}'.format(ColumnSubfield))
    SubfieldWithFieldRegex = re.compile(r'Field #.* {}'.format(ColumnSubfield))
    ColumnCount = 0
    ColumnWithFieldCount = 0

    for item in ColumnList:
        if SubfieldRegex.search(item) == None:
            continue # If the item doen't match the regex, the count doesn't increase
        ColumnCount += 1
    
    for item in ColumnList:
        if SubfieldWithFieldRegex.search(item) == None:
            continue # If the item doen't match the regex, the count doesn't increase
        ColumnWithFieldCount += 1
    
    return (ColumnCount, ColumnWithFieldCount)


def Determine_If_Subfield_Is_Useful(Subfield):
    """If the subfield is in the file, the function asks if the values are useful.

    Some of the subfields should be kept only if they contain useful information, but with no values, Python can't make that decision. This function lets the user make the relevant decisions but won't ask about subfields not in the file. The statements that now return True returned Ask_If_Values_Are_Useful(Subfield) before the GUI was implemented.
    """
    if ColumnsNeeded[Subfield][1] > 0:
        return True
    elif ColumnsNeeded[Subfield][0] == True:
        return True
    else:
        return False


''' Depereciated
def Ask_If_Values_Are_Useful(Subfield):
    """Asks if the subfield given as an argument has useful values; accepts "y" or "n" as answers."""
    Answer = input(f"Are the {Subfield} values useful? ")
    if Answer == "y":
        return True
    if Answer == "n":
        return False
    else:
        Ask_If_Values_Are_Useful(Subfield) # Seeing if recusion can be used for validation--if an invalid answer is given, the question is aksed again
'''


#Section: Creating and Preparing a Title List for OpenRefine
#Subsection: Creating a Title List
# Info on generating MARC via print-03 in Alpeh for both BIB and corresponding HOL or vice versa
# May want more general label on getting data in and out of Alpeh

#Subsection: Prepare MARC File for Import
# Create label with steps:
# Open MARC file as .mrk with MarcEdit
# For BIB, Edit > Edit Shortcuts > Field Edits > Clean ISBD Punctuation
# For BIB, Tools > Add/Delete Field: Field data "FTaSU" Remove fields 856, 710, 897 if field data doesn't match
# Export for OpenRefine
# Add instrucion to open BIB and HOL in OpenRefine


#Section: Organize Records and Subfields 
#Subsection: Starting JSON
os.startfile('Organize_BIB_Records_and_Subfields.json')
input("This line keeps the popups in order; press any key to continue.")
FieldsList = Paste_Text_Facet_Choices_into_Text_Editor()


#Subsection: Count Columns by Subfield and Repetition
# This is actually the first step in the Reorder Columns section, but since the subsections below also need the info for certain fields, it's better to get it here
TempColumnsNeeded = [] # This will contain the results of How_Many_Times_Subfields_Appear
ColumnsNeededValues = [] # This will hold the values for the dictionary below
ColumnsNeeded = {"020$a": "", "020$z": "","776$z": "","020$q": "","776$i": "","024$a": "","024$2": "","035$a": "","710$a": "","710$e": "","897$a": "","897$e": "","856$u": "","856$3": "","856$z": "","264$c": "","264$b": "","245$a": "","245$b": "","245$n": "","250$a": ""} # The values will be tuples with a Boolean for unique fields and a number of repeated fields
ColumnsLookingFor = (r"020\$a", r"020\$z", r"776\$z", r"020\$q", r"776\$i", r"024\$a", r"024\$2", r"035\$a", r"710\$a", r"710\$e", r"897\$a", r"897\$e", r"856\$u", r"856\$3", r"856\$z", r"264\$c", r"264\$b", r"245\$a", r"245\$b", r"245\$n", r"250\$a")

for item in ColumnsLookingFor:
    TempColumnsNeeded.append(How_Many_Times_Subfields_Appear(item, FieldsList))

for item in TempColumnsNeeded:
    UniqueField = bool(item[1] - item[0]) # The boolean subtracts the column with field numbers count from the total column count--if there's a value left, there's a unique subfield
    if UniqueField:
        NumberOfRepeatedFields = item[0] - 1
    else:
        NumberOfRepeatedFields = item[0]
    TupleValues = UniqueField, NumberOfRepeatedFields
    ColumnsNeededValues.append(tuple(TupleValues))

i = 0
for key in ColumnsNeeded:
    ColumnsNeeded[key] = ColumnsNeededValues[i]
    i += 1


#Subsection: Perform Automated Workflow Subfield Checks
if ColumnsNeeded["856$u"][1] > 0: # If there are multiple 856$u fields
    WS_Multiple856u = True
else:
    WS_Multiple856u = False

if ColumnsNeeded["020$q"][1] > 0: # If there are 020$q fields
    WS_Has020q = True
elif ColumnsNeeded["020$q"][0] == True:
    WS_Has020q = True
else:
    WS_Has020q = False

#ToDo: consider dividing these into individual variables
if ColumnsNeeded["264$b"][1] > 0: # If there are multiple 264$b fields
    WS_Multiple264 = True
elif ColumnsNeeded["264$c"][1] > 0: # If there are multiple 264$c fields
    WS_Multiple264 = True
else:
    WS_Multiple264 = False

#Subsection: Create Needed Manual Workflow Subfield Checks--Does this need to appear in the GUI?
WS_Useful024 = Determine_If_Subfield_Is_Useful("024$a")
WS_Useful776i = Determine_If_Subfield_Is_Useful("776$i")
WS_Useful8563 = Determine_If_Subfield_Is_Useful("856$3")
WS_Useful856z = Determine_If_Subfield_Is_Useful("856$z")

if Determine_If_Subfield_Is_Useful("710$a"): # If either function returns True, the value of WS_GobiProviderInfo should be True
    WS_GobiProviderInfo = True
elif Determine_If_Subfield_Is_Useful("897$a"):
    WS_GobiProviderInfo = True
else:
    WS_GobiProviderInfo = False

#Subsection: Create Needed Manual Workflow Subfield Checks--Create the GUI to ask
root_window = Tk()
ttk.Label(root_window, text="If the statement is true, have the checkbox selected.").pack()
if WS_Useful024 == True:
    temp_Useful024 = BooleanVar()
    ttk.Checkbutton(root_window, text="Is the 024 field useful?", variable=temp_Useful024, onvalue=True, offvalue=False).pack()
if WS_Useful776i == True:
    temp_Useful776i = BooleanVar()
    ttk.Checkbutton(root_window, text="Does the 776$i subfield contain aything beyond \"print version\"?", variable=temp_Useful776i, onvalue=True, offvalue=False).pack()
if WS_Useful8563 == True:
    temp_Useful8563 = BooleanVar()
    ttk.Checkbutton(root_window, text="Does the 856$3 subfield contain identifiers?", variable=temp_Useful8563, onvalue=True, offvalue=False).pack()
if WS_Useful856z == True:
    temp_Useful856z = BooleanVar()
    ttk.Checkbutton(root_window, text="Does the 856$z subfield contain identifiers?", variable=temp_Useful856z, onvalue=True, offvalue=False).pack()
if WS_GobiProviderInfo == True:
    temp_GobiProviderInfo = BooleanVar()
    ttk.Checkbutton(root_window, text="Are the 710 and/or 897 fields from Gobi?", variable=temp_GobiProviderInfo, onvalue=True, offvalue=False).pack()
root_window.mainloop() # The program continues automatically when the window closes

# For the questions not asked, the assignment raises an error; the try-excepts below skip them
try:
    WS_Useful024 = temp_Useful024.get()
except NameError:
    pass
try:
    WS_Useful776i = temp_Useful776i.get()
except NameError:
    pass
try:
    WS_Useful8563 = temp_Useful8563.get()
except NameError:
    pass
try:
    WS_Useful856z = temp_Useful856z.get()
except NameError:
    pass
try:
    WS_GobiProviderInfo = temp_GobiProviderInfo.get()
except NameError:
    pass

#Subsection: Workflow Subfield Debugging Checker
# This exists for potential debugging of the workflow subfield statements; instead of running the complete program, the vales for each of the workflow subfield will print to the terminal, then the program will quit
"""
print("Multiple URLs: " + str(WS_Multiple856u))
print("020$q: " + str(WS_Has020q))
print("Multiple 264: " + str(WS_Multiple264))
print("Useful 024: " + str(WS_Useful024))
print("Useful 776$i: " + str(WS_Useful776i))
print("Useful 856$3: " + str(WS_Useful8563))
print("Useful 856$z: " + str(WS_Useful856z))
print("Has Gobi info: :" + str(WS_GobiProviderInfo))
sys.exit() # Supposed to raise SystemExit exception
"""

#Section: Create Table with Wanted Subfields as Columns
#Subsection: Pivot Table
os.startfile('Pivot_Subfields_and_Values.json')

#Subsection: Generate Column List
SubfieldsInColumnOrder = ("020$a", "020$z", "776$z", "020$q", "776$i", "024$a", "024$2", "035$a", "710$a", "710$e", "897$a", "897$e", "856$u", "856$3", "856$z", "264$c", "264$b", "245$a", "245$b", "245$n", "250$a") # Contains subfields in the order they're going into the JSON for reordering columns
OrderOfColumns = ["SYS Number", "Count"]
ColumnsToAdd = {"020$a": None, "020$z": None,"776$z": None,"020$q": None,"776$i": None,"024$a": None,"024$2": None,"035$a": None,"710$a": None,"710$e": None,"897$a": None,"897$e": None,"856$u": None,"856$3": None,"856$z": None,"264$c": None,"264$b": None}
for subfield in SubfieldsInColumnOrder:
    if ColumnsNeeded[subfield][0] == True:
        OrderOfColumns.append(subfield)
    else: # If the subfield needs to appear as a column with no field numbers for the JSONs to work, it's in ColumnsToAdd as a key, and the insert index for the required column can be the value
        if subfield in list(ColumnsToAdd):
            ColumnsToAdd[subfield] = len(OrderOfColumns) # The appropriate insert index might be plus or minus one--check this

    if ColumnsNeeded[subfield][1] > 0:
        for column in range(ColumnsNeeded[subfield][1]):
            OrderOfColumns.append(f"Field #{column+1} {subfield}")

#Subsection: Embed Ordered List of Columns in Column Reordering JSON

#Subsection: Add JSON Objects for Adding Any Needed Columns
for k, v in ColumnsToAdd.items():
    if v != None:
        # create JSON for inserting new column named k at index v with expression "grel:null"
        pass









#Section: JSON for non-repeating fields
if ColumnsNeeded["250$a"][1] > 0: # If there are multiple 250$a fields
    input("Consolidate the edition information to a single 250$a column before continuing.")
#Section: JSON for cleaning 264 fields
    # No reason to believe that this wouldn't work with single 264 field JSON
#Section: JSON for cleaning URLs
    # If 856$3 or 856$z are included, this will include interruption for headers
    # The list input at the beginning can be used to mathematically determine the insertion index
#Section: Cleaning Gobi fields
    # Not tested
#Section: Cleaning 035 fields
    # Not tested
    # This will include interruption for 035 sources
    # the list input at the beginning can be used to determine the insertion index (comes before URLs, so number of columns from that doesn't matter)
#Section: cleaning 024 fields
    # Not tested
#Section: JSONs for cleaning ISBNs
    # The non-subfield JSON needs the deduping added
    # The pause for cleaning up the numbers can be removed
    # Ordering for the ISBN types can be added as well
    # The list input at the beginning can be used matehmatically to determine the index for insertion
#Section: JSON for non-TKR HOL
#Section: TKR loop
    # Need to break to ask and check if there are remaining TKRs
    # Ends with removing TRK$a column
#Section: Cross BIB and HOL
    # Not written yet
    # Below is GREL for add column based on SYS Number column of BIB records
    # cell.cross("<other openrefine project name>", "SYS Number")[0].cells["name of column in other project with value to be pulled in"].value
    # Need way to determine insert indexes