#
# written by Chris.McDonald@uwa.edu.au, 2018-
#
import  os, stat, sys, subprocess, fcntl, re
import  time, tempfile
import  shutil

import  csv
import  smtplib as SMTP
from    email.mime.text import MIMEText


EMAIL_FOR_HELP  = 'crawdad@crawdad.org'
EMAIL_SENT_FROM = 'CRAWDAD <crawdad@crawdad.org>'
EMAIL_TEAM      = 'crawdad-team@cs.dartmouth.edu'

SERVER_EMAIL    = 'katahdin.dartmouth.edu'
#SERVER_LISTSERV = 'listserv.dartmouth.edu'
SERVER_LISTSERV = 'smtp.dartmouth.edu'
EMAIL_LISTSERV  = 'listserv@listserv.dartmouth.edu'

# ensure that each DIR_* variable ends with a '/'
DIR_PUBLIC_HTML     = '/home/crawdad/public_html/'
DIR_REGISTRATION    = '/home/crawdad/CRAWDAD/website/registration/'
DIR_DOWNLOAD        = '/home/crawdad/data/download/'

PATH_HTPASSWD   = '/bin/htpasswd'
PATH_SET_HTP    = DIR_REGISTRATION + 'set-htaccess-passwd'

CSV_USERFILE    = DIR_REGISTRATION + 'USERS.csv'
userfieldnames  = ['username','status','when','realname','email','listserv',
                    'institution','country','htpasswd']

CSV_STATFILE    = DIR_REGISTRATION + 'STATS.csv'
statfieldnames  = ['institution','country']

timenow         = int(time.time())

# ----------------------------------------------------------
# TODO Values over-ridden for TESTING:
#
EMAIL_TEAM      = 'chris@cs.dartmouth.edu'
EMAIL_FOR_HELP  = 'chris@cs.dartmouth.edu'
LOGLOG          = DIR_PUBLIC_HTML + 'loglog'

# ----------------------------------------------------------

LOCKFILE        = '/home/crawdad/.crawdad-registration.lock'
# Posix based file locking (on Linux and MacOS)
def lock_CSV():
    global lock_fd
    lock_fd = open(LOCKFILE, 'w+')
    try:
        fcntl.lockf(lock_fd, fcntl.LOCK_EX)
    except:
        pass

def unlock_CSV():
    global lock_fd
    try:
        fcntl.lockf(lock_fd, fcntl.LOCK_UN)
    except:
        pass
    lock_fd.close();

def count_users():
    n  = 0
    lock_CSV()
    with open(CSV_USERFILE, newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile,  quoting=csv.QUOTE_MINIMAL,
                                fieldnames=userfieldnames)
        next(reader, None)      # skip header row
        for row in reader:
            n += 1
    unlock_CSV()
    return n

def copyfile_with_timenow(original):
    copy  = "{}-{}".format(original, timenow)
    shutil.copyfile(original, copy)
    shutil.copystat(original, copy)

# ----------------------------------------------------------

def generate_htpasswd(username, plaintext):
    proc = subprocess.Popen([PATH_HTPASSWD, '-nbd', username, plaintext],
                            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    htp = proc.communicate()[0]
    htp = htp.decode('utf-8')
    htp = re.sub(r'.*:', '', htp)
    htp = re.sub(r'\n', '', htp)
    return htp

def set_htaccess_passwd(action, username, htpasswd):
    if action is 'add':
        cmd = [PATH_SET_HTP, '-D', DIR_DOWNLOAD, '-a', username, htpasswd]
    elif action is 'set':
        cmd = [PATH_SET_HTP, '-D', DIR_DOWNLOAD, '-s', username, htpasswd]
    elif action is 'del':
        cmd = [PATH_SET_HTP, '-D', DIR_DOWNLOAD, '-d', username]
    else:
        return -1
    return subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#    return subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def reset_password(username, plaintext):
    with open(LOGLOG, 'a', newline='') as log:
        log.write('reset_password({}, {})\n'.format(username, plaintext))
    htpasswd    = generate_htpasswd(username, plaintext)
#
    lock_CSV()
    err = set_htaccess_passwd('set', username, htpasswd)
    unlock_CSV()
    with open(LOGLOG, 'a', newline='') as log:
        log.write('set_htaccess_passwd returned {}\n'.format(err))
    return ''

# ----------------------------------------------------------

def create_newuser(username, plaintext, realname, email, listserv, institution, country):
    htpasswd    = generate_htpasswd(username, plaintext)
#
    lock_CSV()
    copyfile_with_timenow(CSV_USERFILE)
    with open(CSV_USERFILE, 'a', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, quoting=csv.QUOTE_MINIMAL,
                                fieldnames=userfieldnames)
        newrow = {}
        newrow['username']      = username
        newrow['status']        = 'pending'
        newrow['when']          = '{}'.format(timenow)
        newrow['realname']      = realname
        newrow['email']         = email
        newrow['listserv']      = listserv
        newrow['institution']   = institution
        newrow['country']       = country
        newrow['htpasswd']      = htpasswd
        writer.writerow(newrow)
    unlock_CSV()
    return True

# ----------------------------------------------------------

# stat fields = ['institution','country']
def record_statistics(row):
#    copyfile_with_timenow(CSV_STATFILE)
    with open(CSV_STATFILE, 'a', newline='') as stats:
        stats.write('%s,%s\n' % (row['institution'], row['country']))

def set_userstatus(username, newstatus):

    if newstatus not in ['pending', 'active', 'rejected', 'ignored', 'inactive']:
        return False

    found   = False
    (fd, CSV_TEMPFILE)   = tempfile.mkstemp(dir=DIR_REGISTRATION)
    os.close(fd)

    lock_CSV()
    copyfile_with_timenow(CSV_USERFILE)
    with open(CSV_USERFILE, newline='', encoding='utf-8') as infile:
        with open(CSV_TEMPFILE, 'w', newline='', encoding='utf-8') as tmpfile:
            reader = csv.DictReader(infile,  quoting=csv.QUOTE_MINIMAL,
                                    fieldnames=userfieldnames)
            next(reader, None)      # skip header row
            writer = csv.DictWriter(tmpfile, quoting=csv.QUOTE_MINIMAL,
                                    fieldnames=userfieldnames)
            writer.writeheader()

            for row in reader:
# found the required user?
                if row['username'] == username:
                    found           = True
                    row['status']   = newstatus

                    if newstatus == 'active':
                        set_htaccess_passwd('add', username, row['htpasswd'])
                    else:
                        set_htaccess_passwd('del', username, row['htpasswd'])

# save statistics (institution and country) before they are forgotten
                    record_statistics(row)

# anonymize fields that are no longer required
                    row['listserv']     = '_'
                    row['institution']  = '_'
                    row['country']      = '_'
                    row['htpasswd']     = '_'

                    if (newstatus == 'rejected' or newstatus == 'ignored' or
                        newstatus == 'inactive') :
                        row['realname'] = '{}'.format(timenow)
                        row['email']    = '_'

# write (possibly modified) row
                writer.writerow(row)

    if found:
        os.replace(CSV_TEMPFILE, CSV_USERFILE)
#        os.chmod(CSV_USERFILE, stat.S_IRUSR|stat.S_IWUSR|stat.S_IRGRP|stat.S_IWGRP)
        os.chmod(CSV_USERFILE, 0o660)       # owner=crawdad, group=crawdad
    else:
        os.unlink(CSV_TEMPFILE)
    unlock_CSV()
    return found

# ----------------------------------------------------------

def finduser(wanted):
    result = {}                 # empty dictionary
    lock_CSV()
    with open(CSV_USERFILE, newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile,  quoting=csv.QUOTE_MINIMAL,
                                fieldnames=userfieldnames)
        next(reader, None)      # skip header row
        for row in reader:
            if row['username'] == wanted:
                result  = row
                break;
    unlock_CSV()
    return result

def finduser_by_email(username, email):
    result = False
    lock_CSV()
    with open(CSV_USERFILE, newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile,  quoting=csv.QUOTE_MINIMAL,
                                fieldnames=userfieldnames)
        next(reader, None)      # skip header row
        for row in reader:
            if row['username'] == username and row['email'] == email:
                result  = True
                break
    unlock_CSV()
    return result

def search_users(pattern):
    result = []                 # empty list
    lock_CSV()
    with open(CSV_USERFILE, newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile,  quoting=csv.QUOTE_MINIMAL,
                                fieldnames=userfieldnames)
        next(reader, None)      # skip header row
        for row in reader:
            username    = row['username']
            if pattern in username or pattern in row['realname'] or pattern in row['email']:
                result.append(username)
    unlock_CSV()
    return result

# ----------------------------------------------------------

def send_email_0(who_to, bcc, subject, body):
    msg             = MIMEText(body)
    msg['Subject']  = subject
    msg['From']     = EMAIL_SENT_FROM
    msg['To']       = who_to
# TODO: using 'Bcc' does not appear to work
    if bcc:
        msg['Cc']   = EMAIL_TEAM

    try:
        s = SMTP.SMTP(SERVER_EMAIL)
        s.send_message(msg)
        s.quit()
        errs = ''
    except Exception as oops:
        errs = 'cannot send email to {} via {}\nreason: {} {}'.format(who_to, SERVER_EMAIL, type(oops), oops)
    return errs

def send_email(who_to, subject, body):
    return send_email_0(who_to, False, subject, body)

def send_email_bcc(who_to, subject, body):
    return send_email_0(who_to, True, subject, body)


# Mail -n listserv@listserv.dartmouth.edu <<EOF
def email_listserver(who_to, username, name, add):

    print('  called email_listserver()')
    if add:
        print('    ADDING')
        body = 'QUIET ADD CRAWDAD-news {} {}\n'.format(who_to, name)
#        body = 'QUIET ADD CRAWDAD-news {} {} {}\n'.format(who_to, username, name)
    else:
        body = 'QUIET DEL CRAWDAD-news {}\n'.format(who_to)

    msg             = MIMEText(body)
    msg['Subject']  = ''
    msg['From']     = EMAIL_SENT_FROM
    msg['To']       = EMAIL_LISTSERV

    try:
        s = SMTP.SMTP(SERVER_LISTSERV)
        s.send_message(msg)
        s.quit()
        errs = ''
        print('    successful at sending email')
    except Exception as oops:
        print('    failed at sending email')
        errs = 'cannot send email to {}\nreason: {} {}'.format(SERVER_LISTSERV, type(oops), oops)
    return errs

#  encoding='utf_8_sig'

