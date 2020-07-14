#!/usr/bin/python

import cgi, cgitb
from progress_save import save_progress
from validation_common import validate_contribution_form, validate_save_progress
from error_pages import SUBMIT_ERROR_PAGE, SUBMIT_SUCCESS_PAGE, SAVE_ERROR_PAGE
from email.message import EmailMessage
import smtplib, ssl
import os


def submit_email_notification(xml_file_name):
  """
  Send email to crawdad admin once form has been submitted.
  """
  ## Setting up server and credentials
  # port = 465  # For SSL
  # smtp_server = "smtp.gmail.com"
  # sender_email = "emailtesting253@gmail.com"  
  # password = "emailtesting123"

  port = 465
  smtp_server = "mail.cs.dartmouth.edu"
  sender_email = "crawdadmeta@cs.dartmouth.edu"
  password = "oD/vx0y.cr5j"
  
  ## Set up message content
  message = EmailMessage()
  message['Subject'] = "New Metadata Form Submitted"
  message['From'] = f"CRAWDAD Meta {sender_email}"
  message['To'] = "crawdadmin@cs.dartmouth.edu"
  content = f"A new metadata form has been submitted. The submission is saved in the following file:\n\n" \
  f"{xml_file_name}"
  message.set_content(content)

  context = ssl.create_default_context()
  with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
      server.login(sender_email, password)
      server.send_message(message)


def main():
  cgitb.enable() # For debugging

  form = cgi.FieldStorage(keep_blank_values=True)

  ## Save form without validating it when the 'submit' button is pressed

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
    
  ## If 'save' validation checks passed, save the form
  save_progress(form, submitting=False) 

  ## Validate form for submit
  try:
    validation_errors = validate_contribution_form(form)
  except: 
    validation_errors = "<li>Cannot parse request</li>\n"

  ## If validation checks not passed
  if validation_errors != '':
    print("Content-Type:text/html\n")
    error_page_mod = SUBMIT_ERROR_PAGE.replace('[error_list]', validation_errors)
    print(error_page_mod)
    return

  ## If validation checks passed, save the form
  save_progress(form, submitting=True)

  ## And email CRAWDAD admin notifying them about submitted form
  original_page = os.environ['HTTP_REFERER']
  xml_file_name = original_page.split('token=')[1]
  submit_email_notification(xml_file_name) 

  ## Display confirmation for successful submission
  print("Content-Type:text/html\n") 
  print(SUBMIT_SUCCESS_PAGE)


if __name__ == "__main__":
  main()
  
  