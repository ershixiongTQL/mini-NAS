#mini-NAS

Work Flow Suggestion:

1. Get .docx file by extracting "3gpp/24301-h30-NAS.zip"
2. Clear all the format in the .docx file by using any office-like tools which available.
3. Run script "script/lte_nas_msgs_json_from_ts.py" by the .docx file, 
   and the output will be "lte_nas_msgs.json", which contains information about nas messages.
   (python-docx package is required)
4. Run script "script/lte_nas_cpp_gen.py" by the file "lte_nas_msgs.json" and param "--ie_modules ie_modules",
   the generated codes will be contain in dir "gen".
5. Compile a test by including source files in dir "src", "ie_modules" and "gen".
6. Run the test and see what happend.

7. Add modules in dir "ie_modules" to support more IEs in NAS messages.
8. repeat from step 4-7


Notice:
    This little project is under a very begining status, 
    please contact with the author if you feel confused about anything.
 
