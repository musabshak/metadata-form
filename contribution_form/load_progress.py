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

  # if root.attrib.get('submitted') == 'true':
  #   print("Content-Type:text/html\n")   
  #   submit_error = "<li>You have already submitted the form; please contact CRAWDAD admin if you wish to make any changes</li>\n"
  #   with open('templates/submit_failure.txt') as submit_failure_file:
  #     submit_failure_template = submit_failure_file.read()
  #     submit_failure_template = submit_failure_template.replace('[error_list]', submit_error)
  #     print(submit_failure_template)     
  #   return
    
  ## Open contribution form template. Populate field values with values read
  ## from xml file above. Render contribution form with populated values.
  with open ("templates/contribution_form_template.txt", "r") as form_template_file:
    form_template = form_template_file.read()
    # form_template = form_template.replace("label", "div")
    # form_template = form_template.replace("</label>", "")

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

    # end_tsetpages_str = '</div> <button id="prev_button_bottom" type="button" onclick="nextPrev(-1)">Previous</button>'
    end_tsetpages_str = '</div> <button class="prev_button" type="button">Previous</button>'
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



