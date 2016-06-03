#!/usr/bin/python
"""Set Zoneminder admin password and email
Option:
    --pass=     unless provided, will ask interactively
    --email=    unless provided, will ask interactively

"""

import sys
import getopt
import inithooks_cache

from dialog_wrapper import Dialog
from mysqlconf import MySQL

from executil import system

def usage(s=None):
    if s:
        print >> sys.stderr, "Error:", s
    print >> sys.stderr, "Syntax: %s [options]" % sys.argv[0]
    print >> sys.stderr, __doc__
    sys.exit(1)

#DEFAULT_DOMAIN="www.example.com"

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h",
                                       ['help', 'pass=', 'email='])
    except getopt.GetoptError, e:
        usage(e)

    password = ""
    email = ""

    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt == '--pass':
            password = val
        elif opt == '--email':
            email = val

    if not password:
        d = Dialog('TurnKey Linux - First boot configuration')
        password = d.get_password(
            "Zoneminder Password",
            "Enter new password for the Zoneminder 'admin' account.")

    if not email:
        if 'd' not in locals():
            d = Dialog('TurnKey Linux - First boot configuration')

        email = d.get_email(
            "Zoneminder Email",
            "Enter email address for the Zoneminder alerts.",

            "admin@example.com")

    inithooks_cache.write('APP_EMAIL', email)



    inithooks_cache.write('APP_DOMAIN', domain)

    m = MySQL()
    hash=m.execute('')
    m.execute('UPDATE zm.Users SET Password=PASSWORD(\"%s\") WHERE Username=\"admin\";' % password )
    m.execute('UPDATE zm.Config SET Value=\"%s\" WHERE Name=\"ZM_EMAIL_ADDRESS\";' % email)

if __name__ == "__main__":
    main()
