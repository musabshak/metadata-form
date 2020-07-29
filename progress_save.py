#!/usr/bin/python

import cgi,cgitb
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import os
import re
from error_pages import SAVE_ERROR_PAGE
from validation_common import validate_save_progress
from datetime import date


CHECKBOX_FIELD_KEYS = ["dset_keywords", "dset_measurement_purposes", "dset_network_type"]
CHECKBOX_TAG_DICT = {"dset_keywords":"kw", "dset_measurement_purposes":"purpose", "dset_network_type":"nwtype"}

def save_progress(form, submitting=False):
  """
  Given a form via CGI, save the fields to an xml file. 
  If 'submitting=true', set the 'submitted' attribute of the top element in 
  the xml file to 'true'.
  """
  top = Element('form_in_progress')
  top.attrib['form-version'] = "2"
  top.attrib['last-saved'] = str(date.today())

  ## Create dataset/traceset hierarchy
  e = SubElement(top, "dataset")
  e.attrib["version"] = str(date.today())

  num_tsets = int(form.getlist('dset_num_tracesets')[0])
  for i in range(1, num_tsets+1):
    e = SubElement(top, "traceset")
    e.attrib["id"] = str(i)
    e.attrib["version"] = str(date.today())

  ## If submitting, add attribute
  if submitting:
    top.set('submitted', 'true')

  ## Iterate through all submitted form fields
  for key in sorted(form.keys()):
    field_input_list = form.getlist(key)

    # Convert form field names to stripeed tag names
    xml_tag = '_'.join(key.split('_')[1:])

    # And append the field information at the appropriate place in the xml tree
    if key.startswith("dset"):
      child = SubElement(top.find('dataset'), xml_tag)
    elif key.startswith("tset"):
      tset_id = key[4]
      for e in top.findall('traceset'):
        if e.attrib["id"] == tset_id:
          child = SubElement(e, xml_tag)
      
    ## Checkbox datafield
    if key in CHECKBOX_FIELD_KEYS:
      child.set('checkbox', 'true')
      for item in field_input_list: 
        sub_child = SubElement(child, CHECKBOX_TAG_DICT[key])
        sub_child.text = item
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
  print(tostring(top, encoding="UTF-8", xml_declaration=True).decode('UTF-8'), file=open("xml_files/" + xml_file_name + ".xml", 'w'))


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
  


