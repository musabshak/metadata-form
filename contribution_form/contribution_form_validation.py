#!/usr/bin/python
import cgi,cgitb
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import os
import re

CHECKBOX_FIELD_KEYS = ["dset_keywords", "dset_measurement_purposes", "dset_network_type"]

cgitb.enable() #for debugging
form = cgi.FieldStorage(keep_blank_values=True)
# cgi.print_form(form)

#print(", ".join(form.getlist("hair color")))
# cgi.print_directory()
# print(form["dset_name"].value)

top = Element('form_in_progress')
top.set('submitted', 'true')

for key in sorted(form.keys()):
	# print("<h3>{key}</h3>".format(key=key))
	# print(form.getlist(key))

	field_input_list = form.getlist(key)
	child = SubElement(top, key)

	# Checkbox datafield
	if key in CHECKBOX_FIELD_KEYS:
		child.set('checkbox', 'true')
		option_ct = 1
		for item in field_input_list: 
			sub_child = SubElement(child, f'option{option_ct}')
			sub_child.text = item
			option_ct += 1
	else:
		if len(field_input_list) == 0: 
			child.text = ""
		elif len(field_input_list) == 1:
			child.text = field_input_list[0]
 
# Contribution form URL
original_page = os.environ['HTTP_REFERER']

# Token stored in contribution form URL as a query parameter (?token=YYYY-MM-DD-randomstring-datasetname)
xml_file_name = original_page.split('token=')[1]

# Save created xml tree to xml file on server
print(tostring(top).decode('UTF-8'), file=open("xml_files/" + xml_file_name + ".xml", 'w'))

print("Content-Type:text/html\n") 

with open('templates/submit_success.txt', 'r') as success_file:  
  print(success_file.read())

# Redirect user back to the form
# print('Location:', original_page, '\n')   



