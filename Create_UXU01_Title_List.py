# Generate JSONs to turn UXU01 MARC record in OpenRefine into a title list

import os
import re

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

#Subsection: Create Needed Manual Workflow Subfield Checks
# If FieldsList has 024, ask if 024 is worth keeping--if yes, set WS_Useful024 to True
# If FiedlsList has 776$i, ask if it contains info besides "print version"--if yes, set WS_Useful776i to True
# If FieldsList has 710 or 897, ask if they're from Gobi/YBP--if yes, set WS_GobiProviderInfo to True
# If FieldsList has 856$3, ask if they're useful--if yes, set WS_Useful8563 to True
# If FiedlsList has 856$z, ask if they're useful--if yes, set WS_Useful856z to True

#Section: Pivot Table
# Open the JSON to create a pivot column and pivot the table--removing unwanted subfields will be done when the columns are reordered in the next section by virtue of not being included in the list of columns in their new order

#Section: Reorder Columns
#Subsection: Generate Column List
#ToDo: if the 250$a subfield has multiple fields, raise some sort of alert asking that the edition subfields be manually consolidated
# Order: SYS Number < Count < 020$a < 020$z < 776$z < 020$q < 776$i < 024$a < 024$2 < 035$a < 710$a < 710$e < 897$a < 897$e < 856$u < 856$3 < 856$3 < 856$z < 264$c < 264$b < 245$a < 245$b < 245$n < 250$a
# Create a list of columns in the order that they're to be added
# For each subfield above in the order presented
# 1. Check if it's in the list
# 2. Subtract number of columns from number of columns with field numbers to dertermine if there's a column with no field number; if there is, add it to the list
# 3. If it's an ISBN and there's no field number, add it to a list of columns to be added after the reordering along with the position it should be inserted at
#ToDo: search for the other places where the first column needs to not have a field number to work
# 4. Create a "Field #X <subfield>" column where X is all numbers between 1 and the number of columns with field numbers for that subfield and add them to the list
# Repeat the numbered steps for each subfield

#Subsection: Embed Ordered List of Columns in Column Reordering JSON

#Subsection: Add JSON Objects for Adding Any Needed Columns
# Take from the list of columns that need to be added and generate JSON objects with insert indexes based on the positions captured from their creation and expressions of "grel:null"









#Section: JSON for non-repeating fields
    # Throw up error if multiple 250 fields
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