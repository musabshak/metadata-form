#!/usr/bin/python
#
# written by Chris.McDonald@uwa.edu.au, 2018-
#
import  re, os, sys
import  cgi

import  cgitb, traceback
cgitb.enable()

#  REGISTRATIONcommon.py PROVIDES NECESSARY CONSTANTS AND FUNCTIONS
sys.path.append( '/home/crawdad/CRAWDAD/website/registration' )
import  REGISTRATIONcommon  as REGN

# HTML_SUCCESS        = REGN.DIR_PUBLIC_HTML + 'registration-success.html'
# HTML_ERRORS         = REGN.DIR_PUBLIC_HTML + 'registration-errors.html'
HTML_SUCCESS        = 'registration-success.html'
HTML_ERRORS         = 'registration-errors.html'
#
# -- NO CONSTANTS TO MODIFY BEYOND HERE --------------------------------------
#

def send_email_to_admin(form, username, listserv):
    SSH    = 'ssh  crawdad@katahdin.dartmouth.edu ' + REGN.DIR_REGISTRATION
    GOOGLE = 'http://www.google.com/search?hl=en&q='

    name    = form.getvalue('realname')

    body = ''
    body += 'New user registration request:\n\n'

    body += 'Username: {}\n'        .format(username)
    body += 'Name: {}\n'            .format(name)
    body += 'Email: {}\n'           .format(form.getvalue('email1'))
    body += 'Listserv: {}\n'        .format(listserv)
    body += 'Institution: {}\n'     .format(form.getvalue('institution'))
    body += 'Country: {}\n'         .format(form.getvalue('country'))
    body += '\n'

    pat   = '%22{}%22'.format(name)
    pat   = re.sub(' ', '+', pat)
    body += 'To search for this user  (now of much value?):\n\n'
    body += '    {}{}\n'.format(GOOGLE, pat)
    body += '\n\n'

    body += 'To ACCEPT this user, and email a confirmation:\n\n'
    body += '    {}acceptuser.py  {}\n'.format(SSH, username)
    body += '\n\n'

    body += 'To REJECT this user, and email an explanation:\n\n'
    body += '    {}rejectuser.py  {}\n'.format(SSH, username)
    body += '\n\n'
    
    body += 'To IGNORE this user:\n\n'
    body += '    {}ignoreuser.py  {}\n'.format(SSH, username)
    body += '\n\n\n.\n'

    subject = 'CRAWDAD registration request - {}'.format(username)
    REGN.send_email(REGN.EMAIL_TEAM, subject, body)


def send_email_to_newuser(who_to):
    if 'curl' in os.environ['HTTP_USER_AGENT']:
        return

    body = ''
    body += 'Thank you for your interest in CRAWDAD.\n\n'

    body += 'Your request has been passed to our moderators for approval,\n'
    body += 'and you will receive an e-mail when your request has been processed.\n\n'
    body += 'Watch for an email with a subject-line containing "CRAWDAD registration request".\n\n'

    body += 'If you do not hear back within TWO days, please email {}\n'.format(REGN.EMAIL_FOR_HELP)

    subject = 'Your CRAWDAD registration request'
    REGN.send_email(who_to, subject, body )

# --------------------------------------------------------------------

# VALIDATION OF THE REGISTRATION FORM IS NOW DONE IN PYTHON, AND NOT JAVASCRIPT
def validate_registration(form):
    errs = ''

    name    = form.getvalue('realname')
    if not name or len(name) < 2:
        errs += '  <li> You have not provided your name</li>\n'
    else:
        name    = name.strip()
        if not name[0].isalpha():
            errs += '  <li> Ensure that your familyname begins with an alphabetic character</li>\n'

# EMAIL REQUIRED TWICE
    EMAIL_RE1 = r"^([^.@]+)(\.[^.@]+)*@([^.@]+\.)+([^.@]+)$"
    EMAIL_RE2 = r"^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"

    email1   = form.getvalue('email1')
    email2   = form.getvalue('email2')
    if not email1 or email1 == '':
        errs += '  <li> You have not provided your email address</li>\n'
    elif not re.match(EMAIL_RE1, email1) or not re.match(EMAIL_RE2, email1):
        errs += '  <li> You have not provided a recognizable email address</li>\n'

    if not email2:
        errs += '  <li> You have not entered your email address twice (for verification)</li>\n'
    elif email1 != email2:
        errs += '  <li> The two email addresses you provided do not match</li>\n'

# PASSWORD REQUIRED TWICE
    pass1       = form.getvalue('pass1')
    pass2       = form.getvalue('pass2')
    if not pass1 or pass1 == '':
        errs += '  <li> You have not provided your initial password</li>\n'
    elif len(pass1) < 6:
        errs += '  <li> Your password is shorter than 6 characters</li>\n'

    try:
        pass1ascii  = pass1.encode('ascii')
    except:
        errs += '  <li> Your password is not composed of ASCII-only characters</li>\n'

    if not pass2:
        errs += '  <li> You have not entered your password twice (for verification)</li>\n'
    elif pass1 != pass2:
        errs += '  <li> The two passwords you provided do not match</li>\n'

# MUST SELECT A VALID INSTITUTION
    inst = form.getvalue('institution')
    if not inst or inst == '':
        errs += '  <li> You have not selected your institution type</li>\n'
    elif inst not in ['academic', 'corporate', 'government', 'military', 'other']:
        errs += '  <li> You have not selected one of the institution types</li>\n'

# MUST SELECT A 2-CHARACTER COUNTRY CODE
    country = form.getvalue('country')
    if not country or len(country) != 2:
        errs += '  <li> You have not indicated your country</li>\n'

# MUST ACCEPT THE DATA LICENSE AGREEMENT
    if 'click_thru' not in form:
        errs += '  <li> You must read and accept the Data License Agreement</li>\n'
    return errs


def send_html_success():
    with open(HTML_SUCCESS, 'r') as fpin:
        sys.stdout.write(fpin.read())

def send_html_denied(errs):
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

def create_newuser(form, username, listserv):
#
    return REGN.create_newuser(
        username,
        form.getvalue('pass1'),
        form.getvalue('realname'),
        form.getvalue('email1'),
        listserv,
        form.getvalue('institution'),
        form.getvalue('country') )


def main():
    try:
        form = cgi.FieldStorage()
        errs = validate_registration(form)
    except:
        errs = '<li> Cannot parse CGI request</li>\n'

    if errs == '':

# CONVERT USERNAME TO ALPHABETIC ONLY, ALL LOWERCASE
        name  = form.getvalue('realname').strip()
        names = name.split()
        lastname = re.sub(r'[^a-zA-Z]', '', names[len(names)-1]).lower()
        if lastname == '':
            lastname    = 'crawdad'
        next_uid = REGN.count_users() + 1
        username = '{}{}'.format(lastname, next_uid)

        listserv = 'Y' if 'listserv' in form else 'N'

        if create_newuser(form, username, listserv):
            send_email_to_admin(form, username, listserv)
            send_email_to_newuser( form.getvalue('email1') )
        else:
            errs = '<li> There was a server-side problem in storing your registration</li>\n'

# IF NOT INTERACTIVE, HTTP header and blank line
    if not 'HOME' in os.environ.keys():
        print('Content-Type: text/html\n')

# REPLY WITH EITHER SUCCESS OR FAILURE
    if errs == '':
        send_html_success()
    else:
        send_html_denied(errs)

if __name__ == '__main__':
    main()
