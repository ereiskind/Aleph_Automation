# Process for handling having multiple records for a given owned title in UXU01 and possibly UXU60

import os
from tkinter import messagebox

# 1. Collect all possible BIB numbers for the platform/collection in question
# 2. Send BIBs to cataloging to have them check what ones have ACQ records attached
# 3. Pull HOL for BIBs and get TKR, if suppressed
# tkinter.messagebox.showwarning(title=None, message=None, **options) that JSON is for Ebook Central
# 4. Pull all 856$u to get propriatary IDs and determine what BIBs are duplicates
# 5. Pull ISBNs from 020 and 776
# 6. Determine duplicates
# 7. For keeps, check URL, TKR--provide alpeh sequential to update if needed
# 8. For removals, check if other HOLs--if yes, say delete HOL, if no, say delete BIB and HOL