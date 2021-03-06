#!/usr/bin/python

import cgi,cgitb
import smtplib, ssl
from xml.etree.ElementTree import Element, SubElement, Comment, tostring, parse
import os
import string
import secrets
from email.message import EmailMessage
from datetime import datetime
from validation_common import *
from error_pages import SUBMIT_ERROR_PAGE
from datetime import date

# TOKEN_BASE = "home.cs.dartmouth.edu/~mshakeel/contribution_form"
TOKEN_BASE = "home.cs.dartmouth.edu/~crawdad/metadata-form"


def email_token(receiver_email, token):
  """
  Send token link to author for accessing the initialized metadata form.
  """
  smtp_server = "mail.cs.dartmouth.edu"
  sender_email = "crawdadmeta@cs.dartmouth.edu"
  
  ## Set up message content
  message = EmailMessage()
  message['Subject'] = "Metadata Form Token"
  message['To'] = receiver_email
  message['Reply-to'] = 'crawdad-team@cs.dartmouth.edu'
  content = f"You may access the metadata form you started at the " \
  f"following link:\n\n{token}"
  message.set_content(content)

  server = smtplib.SMTP(smtp_server)
  server.send_message(message, from_addr=sender_email, to_addrs=receiver_email)

  return


def gen_xml_name(dset_name):
  """
  Generate xml file name from dataset name and form initialization date
  """
  alphabet = string.ascii_letters + string.digits
  random_str = ''.join(secrets.choice(alphabet) for i in range(8))

  curr_date = datetime.today().strftime('%Y-%m-%d')
  xml_file_name = f"{curr_date}-{random_str}-{dset_name}"

  return xml_file_name


def save_xml(form):
  """
  Save xml file locally from a given CGI form object
  """
  tree = parse('templates/init.xml') # Template xml
  root = tree.getroot()
  for key in form.keys():
    field_input_list = form.getlist(key)
    if field_input_list != []:
      xml_tag = '_'.join(key.split('_')[1:]) # Convert form key to xml tag by stripping 'dset_' from start
      element = root.find('dataset').find(xml_tag)
      element.text = field_input_list[0]

  xml_file_name = gen_xml_name(form.getlist("dset_name")[0]) # "2020-06-25-FcBwiGO2-mobility5g"
  abs_filename = f"xml_files/{xml_file_name}.xml" # "xml_files/2020-06-25-FcBwiGO2-mobility5g.xml"

  print(tostring(root, encoding="UTF-8", xml_declaration=True).decode('UTF-8'), file=open(abs_filename, 'w'))

  return xml_file_name


def main():  
  cgitb.enable() # For debugging
  form = cgi.FieldStorage(keep_blank_values=True)

  try:
    validation_errors = validate_init_form(form)
  except: 
    validation_errors = "<li>Cannot parse request</li>\n"

  if validation_errors != '':
    print("Content-Type:text/html\n")
    error_page_mod = SUBMIT_ERROR_PAGE.replace('[error_list]', validation_errors)
    print(error_page_mod)
    return

  dset_author1_email = form.getlist("dset_author1_email")[0]

  ## Generate xml file. Save initial fields to xml file.
  xml_file_name = save_xml(form)
  token = f"{TOKEN_BASE}/progress_load.py?token={xml_file_name}"

  ## Email token to primary author
  try: 
    email_token(dset_author1_email, token)
  except: 
    print("Content-Type:text/html\n")
    print("Your form has been initialized but the token URL could not be successfully ",
    "emailed. Please access your form at: <br><br>",
    f"<a href='http://{token}'>http://{token}</a><br><br> You must save this URL if you wish to access the form in the future. Note that you ",
    "will not be able to access the form once you have submitted it.")
    return

  ## Render contribution form with fields from initialization page filled in.
  print('Location:', 'http://', token, '\n', sep="")   


if __name__ == '__main__':
  main()
