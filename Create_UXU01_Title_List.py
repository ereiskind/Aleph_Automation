# Generate JSONs to turn UXU01 MARC record in OpenRefine into a title list

#Section: label about removing ISBD punctuation, non-FTaSU 856, 710, 897 in MarcEdit
#Section: starting JSON
#Section: copy "Fields" choices into text box
    # If list has "Field #1 856$u", has multiple 856$u
    # If list has "020$q", has 020$q
    # If list has "Field #1 264$b" or "Field 264$c" (determine w/ regex), has multiple 264
    # Note if multiple 250 fields, if ISBN columns without fields
#Section: if the following fields appear, generate checkboxes to ask if they're relevant
    # 024
    # 776$i
    # 710 and/or 897
    # 856$3
    # 856$z
#Section: JSON for unneeded field removal
    # Can this be done by adding the pieces for the sometimes included subfields to the end of something with the always included subfields, saving the new file as a JSON, and deleting that file just before the program finishes running?
#Section: JSON to pivot table
#Section: JSON to reorder columns
    # Reorder via custom class that takes in the list, puts the items in order by field number with no field number first (have no field number be a zero?), then orders those lists according to the custom order
    # Class removes spaces from items in list, takes attributes MARC for final five characters and Field from after pound sign to sixth character; null field replaced by zero; sort by field using standard sorting; sort by MARC using order below; generate JSON object
    # Only subfields that will be kept by the JSON are included in the class--can exclude SYS Number and Count since they'll always be the same and they'll always be in the same position
    # Order: SYS Number < Count < 020$a < 020$z < 776$z < 020$q < 776$i < 024$a < 024$2 < 035$a < 710$a < 710$e < 897$a < 897$e < 856$u < 856$3 < 856$3 < 856$z < 264$c < 264$b < 245$a < 245$b < 245$n < 250$a
    # Include ISBN columns with no field numbers--if none exist, add those columns; the expression in the JSON object for the addition will be "grel:null"
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