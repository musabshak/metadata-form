#!/usr/bin/python

import cgi,cgitb
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import os
import re
from error_pages import SAVE_ERROR_PAGE
from validation_common import validate_save_progress


CHECKBOX_FIELD_KEYS = ["dset_keywords", "dset_measurement_purposes", "dset_network_type"]


def save_progress(form, submitting=False):
  """
  Given a form via CGI, save the fields to an xml file. 
  If 'submitting=true', set the 'submitted' attribute of the top element in 
  the xml file to 'true'.
  """
  top = Element('form_in_progress')
  if submitting:
    top.set('submitted', 'true')

  for key in sorted(form.keys()):
    field_input_list = form.getlist(key)
    child = SubElement(top, key)

    ## Checkbox datafield
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
  
  ## Form URL
  original_page = os.environ['HTTP_REFERER']

  # Token stored in contribution form URL as a query parameter (?token=YYYY-MM-DD-randomstring-datasetname)
  xml_file_name = original_page.split('token=')[1]

  # Save created xml tree to xml file on server
  print(tostring(top).decode('UTF-8'), file=open("xml_files/" + xml_file_name + ".xml", 'w'))


def main():
  cgitb.enable() # For debugging

  form = cgi.FieldStorage(keep_blank_values=True)

  ## Validate form for save
  try:
    validation_errors = validate_save_progress(form)
  except: 
    validation_errors = "<li>Cannot parse request</li>\n"

  ## If 'save' validation checks not passed, display error page
  if validation_errors != '':
    print("Content-Type:text/html\n")
    error_page_mod = SAVE_ERROR_PAGE.replace('[error_list]', validation_errors)
    print(error_page_mod)
    return

  ## If validation checks passed, save the form
  save_progress(form, submitting=False) 

  ## After saving progress, redirect user back to original page
  original_page = os.environ['HTTP_REFERER']
  print('Location:', original_page, '\n')  

if __name__ == "__main__":
  main()
  


