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
  smtp_server = "mail.cs.dartmouth.edu"
  sender_email = "crawdadmeta@cs.dartmouth.edu"
  receiver_email = "crawdadmin@cs.dartmouth.edu"
  
  ## Set up message content
  message = EmailMessage()
  message['Subject'] = "New Metadata Form Submitted"
  message['To'] = receiver_email
  content = f"A new metadata form has been submitted. The submission is saved in the following file:\n\n" \
  f"{xml_file_name}"
  message.set_content(content)

  server = smtplib.SMTP(smtp_server)
  server.send_message(message, from_addr=sender_email, to_addrs=receiver_email)

  return


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
  
  