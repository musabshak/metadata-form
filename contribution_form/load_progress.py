#!/usr/bin/python

import cgi,cgitb, os
import xml.etree.ElementTree as ET
import re

"""
Normal fields (have either 'value' attribute or can fill in text)
- input text
- input number
- input date
- textarea

Special fields 
- select ('country')
- input checkbox ('keywords')
"""
def main():
  cgitb.enable() #for debugging

  xml_file_name = os.environ['QUERY_STRING'].split('=')[1]
  # print(xml_file_name)
  # print("<br>")

  tree = ET.parse("xml_files/" + xml_file_name + ".xml")
  root = tree.getroot()
  
  ## Open contribution form template. Populate field values with values read
  ## from xml file above. Render contribution form with populated values.
  with open ("templates/contribution_form_template.txt", "r") as form_template_file:
    form_template = form_template_file.read()
    # form_template = form_template.replace("label", "div")
    # form_template = form_template.replace("</label>", "")

    ## Add traceset pages based on saved form field "dset_num_tracesets"
    tracepage_template = ""
    with open ("templates/trace_page_template.txt", 'r') as tracepage_template_file:
      tracepage_template = tracepage_template_file.read()

    end_tsetpages_str = '</div> <button id="prev_button_bottom" type="button" onclick="nextPrev(-1)">Previous</button>'
    dset_num_tracesets = int(root.find('dset_num_tracesets').text)

    modified_tracepage = ""
    for i in range(1, dset_num_tracesets+1):
      modified_tracepage = tracepage_template.replace('[id]', str(i))
      modified_tracepage += '\n' + end_tsetpages_str
      form_template = form_template.replace(end_tsetpages_str, modified_tracepage)

    # print("Content-Type:text/html\n")
    # print(form_template)
    
    filled_form = form_template
    for child in root: 
      # 'Select' datafield
      # if ("country" in child.tag):
      #   ## TODO: Deal with this edge case by re-formatting country option tags in template file
      #   continue
      # 'input type="checkbox"' datafield
      if ("checkbox" in child.attrib):
        for sub_child in child:
          checkbox_str = f'input type="checkbox" name="{child.tag}" value="{sub_child.text}"'
          filled_form = filled_form.replace(checkbox_str, checkbox_str + ' checked')
      # All other datafields (text, number, date, textarea)
      else:
        if (child.text == None):
          filled_form = filled_form.replace(f"[{child.tag}]", "")
        else:
          filled_form = filled_form.replace(f"[{child.tag}]", child.text)
    print("Content-Type:text/html\n")    
    print(filled_form)
  
if __name__ == '__main__':
  main()



