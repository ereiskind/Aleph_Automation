# Upload a list of SYS (BIB or HOL) into Aleph via the web client

#import

#Section: Create the File to Upload
#Subsection: Collect the SYS
# Use the same paste into a notebook as in the title list
# Dedupe the list

#Subsection: Write the Properly Formatted SYS to a File
# Use a pop-up GUI to ask if the SYS are HOL or BIB
# Use the GUI to ask for a file name of six or fewer lowercase letters
# Open a for loop with a file named "fser" plus the letters input with no file extension
# When writing each SYS to the file, add zeros to the front so it's nine digits, then add the database to the end


#Section: Upload the File
# Ask which server to go to
## https://susopac.falsc.org/cgi-bin/afv for production
## https://susopac.test.falsc.org/cgi-bin/afv for test
## https://susopac.rept.falsc.org/cgi-bin/afv for report
# Log in with Aleph credentials
# For uploader, choose file created above

#Section: Final Note
# End with message box stating that inputting hte file name into "Load" in the Aleph search page of the client selected for uploading will return the SYS list as a search result