#!/usr/bin/python

import cgi,cgitb
import smtplib, ssl
from xml.etree.ElementTree import Element, SubElement, Comment, tostring, parse
import os
import string
import secrets

from email.message import EmailMessage
from datetime import datetime

# Send token link to author for accessing the initialized metadata form.
def email_token(receiver_email, token):
  ## Setting up server and credentials
  port = 465  # For SSL
  smtp_server = "smtp.gmail.com"
  # smtp_server = "127.0.0.1"
  sender_email = "emailtesting253@gmail.com"  # Enter your address
  # receiver_email = "musabshakeel@gmail.com"  # Enter receiver address
  password = "emailtesting123"

  ## Set up message contents
  message = EmailMessage()
  message['Subject'] = "Contribution Form Token"
  message['From'] = f"CRAWDAD Admin {sender_email}"
  message['To'] = receiver_email
  content = f"You may access the contribution form you started at the " \
  f"following link:\n\n{token}"
  message.set_content(content)

  # server = smtplib.SMTP('127.0.0.1', 1025)
  # server.set_debuglevel(True)
  # server.sendmail(sender_email, receiver_email, message)

  context = ssl.create_default_context()
  with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
      server.login(sender_email, password)
      server.send_message(message)
      # server.sendmail(sender_email, receiver_email, message)

## Generate xml file name from dataset name, initialization page submission date, randomly string
def gen_xml_name(dset_name):
  alphabet = string.ascii_letters + string.digits
  random_str = ''.join(secrets.choice(alphabet) for i in range(8))

  curr_date = datetime.today().strftime('%Y-%m-%d')
  xml_file_name = f"{curr_date}-{random_str}-{dset_name}"

  return xml_file_name

## Generate xml file from a given CGI form object
def save_xml(form):
  tree = parse('other/init.xml')
  root = tree.getroot()
  for key in form.keys():
    field_input_list = form.getlist(key)
    if field_input_list != []:
      element = root.find(key)
      element.text = field_input_list[0]

  xml_file_name = gen_xml_name(form.getlist("dset_name")[0])
  # prefix = "home.cs.dartmouth.edu/~mshakeel/contribution_form/xml_files"
  abs_filename = f"xml_files/{xml_file_name}.xml"
  print(tostring(root).decode('UTF-8'), file=open(abs_filename, 'w'))

  return xml_file_name


def main():
  # print("Content-Type:text/html\n")                          
  
  cgitb.enable() #for debugging
  form = cgi.FieldStorage()

  # print(", ".join(form.getlist("hair color")))
  # cgi.print_form(form)
  # cgi.print_directory()
  # print()

  # print(form.getlist("dset_name"))
  # print(form.getlist("dset_num_tracesets"))

  ## Gather filled fields from the initialization page.
  # dset_name = form.getlist("dset_name")[0]
  # dset_description_short = form.getlist("dset_description_short")[0]
  # dset_institution_name = form.getlist("dset_institution_name")[0]
  # dset_author1_name = form.getlist("dset_author1_name")[0]
  dset_author1_email = form.getlist("dset_author1_email")[0]
  # dset_author1_institution = form.getlist("dset_author1_institution")[0]
  # dset_author1_country = form.getlist("dset_author1_country")[0]

  ## Generate xml file. Save initial fields to xml file.
  xml_file_name = save_xml(form)
  token = f"home.cs.dartmouth.edu/~mshakeel/contribution_form/load_progress.py?token={xml_file_name}"

  ## Email token to primary author
  try: 
    email_token(dset_author1_email, token)
  except: 
    print("emailing token unsuccessful")

  # Render contribution form with fields from initialization page filled in.
  with open ("contribution_form_template.txt", "r") as form_contents_file:
    # form_contents = form_contents_file.read()
    # filled_form = form_contents
    # filled_form = filled_form.replace("[dset_name]", dset_name)
    # filled_form = filled_form.replace("[dset_description_short]", dset_description_short)
    # filled_form = filled_form.replace("[dset_institution_name]", dset_institution_name)
    # filled_form = filled_form.replace("[dset_author1_name]", dset_author1_name)
    # filled_form = filled_form.replace("[dset_author1_email]", dset_author1_email)
    # filled_form = filled_form.replace("[dset_author1_institution]", dset_author1_institution)
    # filled_form = filled_form.replace(f">{dset_author1_country}", f"selected> {dset_author1_country}")
    # print(filled_form)
    print('Location:', 'http://', token, '\n', sep="")   


if __name__ == '__main__':
  main()
