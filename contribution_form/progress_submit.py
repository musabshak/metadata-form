#!/usr/bin/python
import cgi, cgitb
from progress_save import save_progress
from validation_common import validate_contribution_form
from error_pages import FORM_SUBMISSION_ERROR_PAGE, SUBMIT_SUCCESS_PAGE


def main():

  cgitb.enable() # for debugging
  form = cgi.FieldStorage(keep_blank_values=True)
  save_progress(form, submitting=False)


  try:
    validation_errors = validate_contribution_form(form)
  except: 
    validation_errors = "<li>Cannot parse request</li>\n"

  if validation_errors != '':
    print("Content-Type:text/html\n")
    error_page_mod = FORM_SUBMISSION_ERROR_PAGE.replace('[error_list]', validation_errors)
    print(error_page_mod)
    return


  save_progress(form, submitting=True)

  print("Content-Type:text/html\n") 
  print(SUBMIT_SUCCESS_PAGE)


if __name__ == "__main__":
  main()
  
  