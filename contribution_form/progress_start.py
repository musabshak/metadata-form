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


def email_token(receiver_email, token):
  """
  Send token link to author for accessing the initialized metadata form.
  """
  ## Setting up server and credentials
  port = 465  # For SSL
  smtp_server = "smtp.gmail.com"
  sender_email = "emailtesting253@gmail.com"  # Enter your address
  password = "emailtesting123"

  ## Set up message content
  message = EmailMessage()
  message['Subject'] = "Contribution Form Token"
  message['From'] = f"CRAWDAD Admin {sender_email}"
  message['To'] = receiver_email
  content = f"You may access the contribution form you started at the " \
  f"following link:\n\n{token}"
  message.set_content(content)

  context = ssl.create_default_context()
  with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
      server.login(sender_email, password)
      server.send_message(message)


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
      element = root.find(key)
      element.text = field_input_list[0]

  xml_file_name = gen_xml_name(form.getlist("dset_name")[0]) # "2020-06-25-FcBwiGO2-mobility5g"
  abs_filename = f"xml_files/{xml_file_name}.xml" # "xml_files/2020-06-25-FcBwiGO2-mobility5g.xml"

  print(tostring(root).decode('UTF-8'), file=open(abs_filename, 'w'))

  return xml_file_name


def main():  
  cgitb.enable() #for debugging
  form = cgi.FieldStorage(keep_blank_values=True)

  try:
    validation_errors = validate_init_form(form)
  except: 
    validation_errors = "<li>Cannot parse request<li>\n"

  if validation_errors != '':
    print("Content-Type:text/html\n")
    error_page_mod = SUBMIT_ERROR_PAGE.replace('[error_list]', validation_errors)
    print(error_page_mod)
    return

  dset_author1_email = form.getlist("dset_author1_email")[0]

  ## Generate xml file. Save initial fields to xml file.
  xml_file_name = save_xml(form)
  token = f"home.cs.dartmouth.edu/~mshakeel/contribution_form/progress_load.py?token={xml_file_name}"

  ## Email token to primary author
  try: 
    email_token(dset_author1_email, token)
  except: 
    print("Content-Type:text/html\n")
    print("emailing token unsuccessful")

  ## Render contribution form with fields from initialization page filled in.
  print('Location:', 'http://', token, '\n', sep="")   


if __name__ == '__main__':
  main()
