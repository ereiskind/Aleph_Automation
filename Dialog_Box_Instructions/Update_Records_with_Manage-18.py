'''
Manage-18: Add/Update Records
1. Create Alpeh Sequential .txt file
    Line format: <BIB or HOL as 9 digits> <MARC field and indicators--if indicators are null, use spaces> L $$<first subfield code><value of first subfield><repeat pattern of dollar signs, subfield code, and subfield value without spaces for all subfields>
2. Remove file extension
3. Go to https://susopac.falsc.org/cgi-bin/afv for production, https://susopac.test.falsc.org/cgi-bin/afv for test, https://susopac.rept.falsc.org/cgi-bin/afv for report and enter Aleph credentials
4. Select "uxu01/scratch" radio button for BIBs or "uxu60/scratch" radio button for HOLs
5. Upload file
6. Services > Load Catalog Records > Manage-18
7. Dialog box--Input file: name of file
8. Dialog box--Procedure to Run: indicate if adding records or updating existing records
9. Dialog box--If Updating Current Records: append
10. Dialog box--Cataloger Name: Alpeh login
11. Dialog box--Library: match to scratch directory file is in
'''