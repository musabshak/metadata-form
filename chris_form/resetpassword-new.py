#!/usr/bin/env python3
#
# written by Chris.McDonald@uwa.edu.au, 2018-
#
import  re, os, sys
import  cgi, hashlib

#import  cgitb, traceback
#cgitb.enable()

#  REGISTRATIONcommon.py PROVIDES NECESSARY CONSTANTS AND FUNCTIONS
sys.path.append( '/home/crawdad/CRAWDAD/website/registration' )
import  REGISTRATIONcommon  as REGN

HTML_SUCCESS        = REGN.DIR_PUBLIC_HTML + 'resetpassword-success.html'
HTML_ERRORS         = REGN.DIR_PUBLIC_HTML + 'resetpassword-errors.html'
#
# -- NO CONSTANTS TO MODIFY BEYOND HERE --------------------------------------
#


# VALIDATION OF THE REGISTRATION FORM IS NOW DONE IN PYTHON, AND NOT JAVASCRIPT
def validate_resetpassword(form):
    errs = ''

# MUST PROVIDE EXISTING USERNAME
    username    = form.getvalue('username')
    if not username or len(username) < 2:
        errs += '  <li> You have not provided your existing username</li>\n'

# MUST PROVIDE EXISTING EMAIL ADDRESS
    email    = form.getvalue('email')
    if not email or len(email) < 5:
        errs += '  <li> You have not provided your recorded email address</li>\n'

# ENSURE THIS USERNAME+EMAIL IS KNOWN
    if not REGN.finduser_by_email(username, email):
        errs += '  <li> No registered user has that username and email address</li>\n'

# PASSWORD REQUIRED TWICE
    pass1   = form.getvalue('pass1')
    pass2   = form.getvalue('pass2')
    if not pass1 or pass1 == '':
        errs += '  <li> You have not provided your new password</li>\n'
    elif len(pass1) < 6:
        errs += '  <li> Your new password is shorter than 6 characters</li>\n'
    try:
        pass1ascii  = pass1.encode('ascii')
    except:
        errs += '  <li> Your password is not composed of ASCII-only characters</li>\n'

    if not pass2:
        errs += '  <li> You have not entered your new password twice (for verification)</li>\n'
    elif pass1 != pass2:
        errs += '  <li> The two passwords you provided do not match</li>\n'

    return errs


def send_html_success():
    with open(HTML_SUCCESS, 'r') as fpin:
        sys.stdout.write(fpin.read())

def send_html_error(errs):
    if 'HOME' in os.environ.keys():
        print(errs)
    else:
        with open(HTML_ERRORS) as fpin:
            for line in fpin:
                line = line.strip('\n')
                if 'DESCRIPTION_OF_ERRORS_HERE' in line:
                    print('<table style="margin-left: 1em;"><tr><td>\n<ul>')
                    print(errs)
                    print('</ul>\n</td></tr></table>')
                else:
                    print(line)

# --------------------------------------------------------------------

def main():
    try:
        form = cgi.FieldStorage()
        errs = validate_resetpassword(form)
    except:
        errs = '<li> Cannot parse CGI request</li>\n'

    if errs == '':

        username    = form.getvalue('username').strip()
        pass1       = form.getvalue('pass1')
        errs        = REGN.reset_password(username, pass1)

# IF NOT INTERACTIVE, HTTP header and blank line
    if not 'HOME' in os.environ.keys():
        print('Content-Type: text/html\n')

# REPLY WITH EITHER SUCCESS OR FAILURE
    if errs == '':
        send_html_success()
    else:
        send_html_error(errs)

if __name__ == '__main__':
    main()
