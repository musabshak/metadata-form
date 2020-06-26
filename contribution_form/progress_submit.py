#!/usr/bin/python

import cgi, cgitb
from progress_save import save_progress
from validation_common import validate_contribution_form, validate_save_progress
from error_pages import SUBMIT_ERROR_PAGE, SUBMIT_SUCCESS_PAGE, SAVE_ERROR_PAGE


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
    
  ## If validation checks passed, save the form
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

  ## Display confirmation for successful submission
  print("Content-Type:text/html\n") 
  print(SUBMIT_SUCCESS_PAGE)


if __name__ == "__main__":
  main()
  
  