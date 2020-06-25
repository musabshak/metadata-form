#!/usr/bin/python
import cgi, cgitb
from save_progress import save_progress
from validation_common import validate_contribution_form


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
    with open('templates/submit_failure.txt') as submit_failure_file:
      submit_failure_template = submit_failure_file.read()
      submit_failure_template = submit_failure_template.replace('[error_list]', validation_errors)
      print(submit_failure_template)     
    return


  save_progress(form, submitting=True)

  print("Content-Type:text/html\n") 
  with open('templates/submit_success.txt', 'r') as success_file:  
    print(success_file.read())


if __name__ == "__main__":
  main()
  
  