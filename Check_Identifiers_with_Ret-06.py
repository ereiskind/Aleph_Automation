'''
Ret-06: Check Identifiers (ISBN, 035, OCLC)
1. Services > Retrieve Catalog Records > Ret-06
2. For dialog box
    Input file: list of BIBs imported via above process
    Output file: name of new file
    Search Index: "020" for ISBN, "UTL" for 035
3. Go to https://susopac.falsc.org/cgi-bin/afv for production, https://susopac.test.falsc.org/cgi-bin/afv for test, https://susopac.rept.falsc.org/cgi-bin/afv for report and enter Aleph credentials
4. Retrieve files from "uxu01/scratch" (I think, instructions don't specify)
    Success file has BIB numbers
    Failures file has original inputs (BIBs + directory)
'''