#Lbw2vue#


Laubwerk plant model importer for VueInfinite
  
##Requirements##

- e-on Vue Infinite
    - tested with Vue Infinite 2014.2 full and Personal Learning Editions
- Laubwerk Plant Kit  
    - Any Laubwerk Plant Kit packs, following the default installation file hierarchy
    - Included Laubwerk Python file lbwtoobj.py 
    
##Run instructions##
- Download import_lbw.py. Save to same directory where lbwtoobj.py is stored (default location C:\Program Files\Laubwerk\Python\examples)
- Launch Vue Infinite
- In the top menu, click Automation, and then Run Python Script. Navigate to import_lbw.py and launch it.
- For now, script parameters must be set by editing import_lbw.py. Use a text editor to set the Laubwerk plant install directory and the number of placeholder objects you want to create.
    
##Next steps##
- Find a way to map textures to object
- Scale models appropriately - see note in import_lbw.py
- use wxPython to write user interface for this tool plugin
- Specify plant attributes?