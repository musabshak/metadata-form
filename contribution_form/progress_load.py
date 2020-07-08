#!/usr/bin/python

import cgi,cgitb, os
import xml.etree.ElementTree as ET
import re
from error_pages import ALREADY_SUBMITTED_ERROR_PAGE

SUBMIT_CHECK = True

def main():
  cgitb.enable() # For debugging

  ## Get the xml file name from the URL
  xml_file_name = os.environ['QUERY_STRING'].split('=')[1]

  tree = ET.parse("xml_files/" + xml_file_name + ".xml")
  root = tree.getroot()

  ## If form has been submitted already, do not allow access
  if SUBMIT_CHECK and root.attrib.get('submitted') == 'true':
    print("Content-Type:text/html\n")   
    print(ALREADY_SUBMITTED_ERROR_PAGE)     
    return
    
  ## Open contribution form template. Populate field values with values read
  ## from xml file above. Render contribution form with populated values.
  with open ("templates/cf_template.txt", "r") as form_template_file:
    form_template = form_template_file.read()

    ## Add author details based on saved form field "dset_num_authors"
    author_template = ""
    with open("templates/author_details_template.txt") as author_template_file:
      author_template = author_template_file.read()
    
    end_author_details_str = "</div> <!-- End of Author Details-->"
    dset_num_authors = int(root.find('dset_num_authors').text)

    modified_author_details = ""
    for i in range(2, dset_num_authors+1):
      modified_author_details = author_template.replace('[id]', str(i))
      modified_author_details += '\n' + end_author_details_str
      form_template = form_template.replace(end_author_details_str, modified_author_details)

    ## Add traceset pages based on saved form field "dset_num_tracesets"
    tracepage_template = ""
    with open ("templates/trace_page_template.txt", 'r') as tracepage_template_file:
      tracepage_template = tracepage_template_file.read()

    end_tsetpages_str = '</div> <!-- End of Tset Pages-->'
    dset_num_tracesets = int(root.find('dset_num_tracesets').text)

    modified_tracepage = ""
    for i in range(1, dset_num_tracesets+1):
      modified_tracepage = tracepage_template.replace('[id]', str(i))
      modified_tracepage += '\n' + end_tsetpages_str
      form_template = form_template.replace(end_tsetpages_str, modified_tracepage)

    filled_form = form_template
    for child in root: 
      ## Checkbox fields (with multiple values)
      if ("checkbox" in child.attrib):
        for sub_child in child:
          checkbox_str = f'input type="checkbox" name="{child.tag}" value="{sub_child.text}"'
          filled_form = filled_form.replace(checkbox_str, checkbox_str + ' checked')
      ## All other fields (text, number, textarea) (have only one value)
      else:
        if (child.text == None):
          filled_form = filled_form.replace(f"[{child.tag}]", "")
        else:
          filled_form = filled_form.replace(f"[{child.tag}]", child.text)

    print("Content-Type:text/html\n")    
    print(filled_form)
  
if __name__ == '__main__':
  main()



