Lbw2vue
=======

Laubwerk plant model importer for Vue Infinite
  
Requirements
------------
* e-on Vue Infinite
	* tested with Vue Infinite 2014.2 and 2015.2 full and Personal Learning Editions
* Laubwerk Plants Kit
	* Any Laubwerk Plants Kit, following the default installation file hierarchy

Installation
------------
Download or clone the current version of the repository to a location of your choice using GitHub's "Clone or download" button.

Running
-------
* Launch Vue Infinite
* In the top menu, click Automation, and then Run Python Script. Navigate to import_lbw.py and launch it.
* For now, script parameters must be set by editing import_lbw.py. Use a text editor to set the Laubwerk plant install directory and the number of placeholder objects you want to create.

Known Issues
------------
* For some reason the script doesn't bring up the Python Console up when it starts. Since the Python Console is used to show the selection of plant species, you may want to bring it up maually before you run the script. This problem will go away as soon as the UI is more developed.

Next Steps
----------
* use wxPython to write user interface for this tool plugin
* Specify plant attributes
* Automatic saving to .vob
* Improve materials?
* Make the specification of the Plant library search path more flexible