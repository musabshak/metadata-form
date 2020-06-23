import re


def validateXsetName(name, fieldID):
  XsetName = name

  regexp = r"^[a-zA-Z0-9-]+$"
  if XsetName == "":
     return (f"<li>{fieldID} is a required field</li>\n")
  elif (not re.match(regexp, XsetName)):
    return (f"<li>{fieldID} may contain only alpha-numeric characters, preferable all lowercase</li>\n")

  return ''

def validateEmail(email, fieldID):
  EMAIL_RE1 = r"^([^.@]+)(\.[^.@]+)*@([^.@]+\.)+([^.@]+)$"
  EMAIL_RE2 = r"^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"

  if email == "":
    return (f"<li>{fieldID} is a required field</li>\n")
  elif not re.match(EMAIL_RE1, email) or not re.match(EMAIL_RE2, email):
    return (f"<li>{fieldID} must be a valid email address</li>\n")

  return ''

def validate_init_form(form):
  errs = ''

  # Validate dataset name
  dset_name = form.getlist('dset_name')[0]
  errs += validateXsetName(dset_name, 'dset_name')

  # Validate email
  dset_author1_email = form.getlist('dset_author1_email')[0]
  errs += validateEmail(dset_author1_email, 'dset_author1_email')

  return errs
