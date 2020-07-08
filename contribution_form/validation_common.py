import re

## Constants. Should match the constants at the top of 'main_validation.js' file.
INPUT_TEXT_CHARLIMIT = 50
TEXTAREA_CHARLIMIT = 5000
MAX_TSET_PAGES = 15
MAX_AUTHORS = 4

dset_required_fields = [
  "dset_name", 
  "dset_institution_name",
  "dset_description_short",
  "dset_description_long",
  "dset_num_tracesets",
  "dset_author1_name",
  "dset_author1_email", 
  "dset_author1_institution",
  "dset_author1_country",
  # "dset_start_date",
  # "dset_end_date"
]

tset_required_fields = [
  "tsetX_name",
  "tsetX_description_short",
  "tsetX_tech_description",
  "tsetX_start_date",
  "tsetX_end_date"
]

def validateXsetName(value, fieldID):
  XsetName = value

  regexp = r"^[a-zA-Z0-9-_]+$"
  if XsetName == "":
     return (f"<li>{fieldID} is a required field</li>\n")
  elif (not re.match(regexp, XsetName)):
    return (f"<li>{fieldID} may contain only alpha-numeric characters and/or hyphens and underscores</li>\n")

  return ''

def validateEmail(value, fieldID):
  email = value
  EMAIL_RE1 = r"^([^.@]+)(\.[^.@]+)*@([^.@]+\.)+([^.@]+)$"
  EMAIL_RE2 = r"^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"

  if email == "":
    return (f"<li>{fieldID} is a required field</li>\n")
  elif not re.match(EMAIL_RE1, email) or not re.match(EMAIL_RE2, email):
    return (f"<li>{fieldID} must be a valid email address</li>\n")

  return ''

def validateNumTsets(value, fieldID):
  if (value > MAX_TSET_PAGES):
    return (f"<li>{fieldID} must be less than {MAX_TSET_PAGES}</li>\n")
  return ''

def validateNumAuthors(value, fieldID):
  if (value > MAX_AUTHORS):
    return (f"<li>{fieldID} must be less than {MAX_AUTHORS}</li>\n")
  return ''

def validateRequired(value, fieldID):

  if value == "":
    return (f"<li>{fieldID} is a required field; you must fill it</li>\n")

  return ''

def validateDateFormat(value, fieldID):
  """
  'Start date <= End Date' validation NOT performed on server-side
  """
  regexp = r"^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$"

  if not re.match(regexp, value):
    return (f"<li>{fieldID} must be formatted correctly</li>\n")

  return ''

def validateCharLimit(value, fieldID):
  """
  Only 5000 character max char limit validated on server-side (input field text limit of 50 character
  not validated).
  """
  if len(value) > TEXTAREA_CHARLIMIT:
    return (f"<li>{fieldID} may not contain more than {TEXTAREA_CHARLIMIT} characters</li>\n")
  return ''

def validate_init_form(form):
  errs = ''

  ## Validate dataset name
  dset_name = form.getlist('dset_name')[0]
  errs += validateXsetName(dset_name, 'dset_name')

  ## Validate email
  dset_author1_email = form.getlist('dset_author1_email')[0]
  errs += validateEmail(dset_author1_email, 'dset_author1_email')

  return errs


def validate_save_progress(form):
  errs = ''

  ## Validate 'num tracesets'
  dset_num_tracesets = int(form.getlist('dset_num_tracesets')[0])
  errs += validateNumTsets(dset_num_tracesets, 'dset_num_tracesets')

  ## Validate all Xset names
  dset_name = form.getlist('dset_name')[0]
  errs += validateXsetName(dset_name, 'dset_name')

  dset_name = form.getlist('dset_institution_name')[0]
  errs += validateXsetName(dset_name, 'dset_institution_name')

  for i in range(1, dset_num_tracesets+1):
    fieldName = f"tset{i}_name"
    errs += validateXsetName(form.getlist(fieldName)[0], fieldName)

  ## Validate character limit for all fields
  for key in sorted(form.keys()):
    for item in form.getlist(key):
      errs += validateCharLimit(item, key) 
  
  return errs

def validate_contribution_form(form):
  errs = ''

  ## Validate 'num tracesets'
  dset_num_tracesets = int(form.getlist('dset_num_tracesets')[0])
  errs += validateNumTsets(dset_num_tracesets, 'dset_num_tracesets')

  ## Validate 'num authors'
  dset_num_authors = int(form.getlist('dset_num_authors')[0])
  errs += validateNumAuthors(dset_num_authors, 'dset_num_authors')

  ## Validate all required fields
  all_required_fields = dset_required_fields
  for i in range(1, dset_num_tracesets+1):
    for j in range(len(tset_required_fields)):
      all_required_fields.append(tset_required_fields[j].replace('X', str(i)))
  for i in range(len(all_required_fields)):
    fieldName = all_required_fields[i]
    errs += validateRequired(form.getlist(fieldName)[0], fieldName)

  ## If required fields not filled in, return early and indicate so
  if errs != '':
    return errs

  ## Validate all Xset names
  dset_name = form.getlist('dset_name')[0]
  errs += validateXsetName(dset_name, 'dset_name')

  dset_name = form.getlist('dset_institution_name')[0]
  errs += validateXsetName(dset_name, 'dset_institution_name')

  for i in range(1, dset_num_tracesets+1):
    fieldName = f"tset{i}_name"
    errs += validateXsetName(form.getlist(fieldName)[0], fieldName)

  ## Validate all dates (format only)
  # dset_start_date = form.getlist('dset_start_date')[0]
  # dset_end_date = form.getlist('dset_end_date')[0]
  # errs += validateDateFormat(dset_start_date, 'dset_start_date')
  # errs += validateDateFormat(dset_end_date, 'dset_end_date')

  for i in range(1, dset_num_tracesets+1):
    fieldName1 = f"tset{i}_start_date"
    fieldName2 = f"tset{i}_end_date"
    errs += validateDateFormat(form.getlist(fieldName1)[0], fieldName1)
    errs += validateDateFormat(form.getlist(fieldName2)[0], fieldName2)

  ## Validate all emails
  for i in range(1, dset_num_authors+1):
    fieldName = f"dset_author{i}_email"
    errs += validateEmail(form.getlist(fieldName)[0], fieldName)

  ## Validate character limit for all fields
  for key in sorted(form.keys()):
    for item in form.getlist(key):
      errs += validateCharLimit(item, key) 

  return errs
   
