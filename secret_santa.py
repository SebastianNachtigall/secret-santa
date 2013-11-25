import sys
import re
import getopt

from html_email import HtmlMail
from models import Usage, Person
from utils import parse_yaml, create_pairs, parse_email


help_message = '''
To use, fill out config.yml with your own participants. You can also specify
couples so that people don't get assigned their significant other.

You'll also need to specify your mail server settings. An example is provided
for routing mail through gmail.

For more information, see README.
'''

REQRD = (
    'SMTP_SERVER',
    'SMTP_PORT',
    'USERNAME',
    'PASSWORD',
    'TIMEZONE',
    'PARTICIPANTS',
    'COUPLES',
    'FROM',
    'SUBJECT',
)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "shc", ["send", "help"])
        except getopt.error, msg:
            raise Usage(msg)

        # option processing
        send = False
        for option, value in opts:
            if option in ("-s", "--send"):
                send = True
            if option in ("-h", "--help"):
                raise Usage(help_message)

        # Parse configuration
        config = parse_yaml()
        for key in REQRD:
            if key not in config.keys():
                raise Exception(
                    'Required parameter %s not in yaml config file!' % (key,))

        participants = config['PARTICIPANTS']
        couples = config['COUPLES']
        if len(participants) < 2:
            raise Exception('Not enough participants specified.')

        # Mail parsing
        f = open('templates/mail.html', 'r')
        mail_html = ""
        while 1:
            line = f.readline()
            if not line:
                break
            mail_html += line

        f.close()

        givers = []
        for person in participants:
            name, email = re.match(r'([^<]*)<([^>]*)>', person).groups()
            name = name.strip()
            partner = None
            for couple in couples:
                names = [n.strip() for n in couple.split(',')]
                if name in names:
                    # is part of this couple
                    for member in names:
                        if name != member:
                            partner = member
            person = Person(name, email, partner)
            givers.append(person)

        recievers = givers[:]
        pairs = create_pairs(givers, recievers)
        if not send:
            print """
                    Test pairings:

                    %s

                    To send out emails with new pairings,
                    call with the --send argument:

                    $ python secret_santa.py --send

            """ % ("\n".join([str(p) for p in pairs]))

        for pair in pairs:

            if send:
                to = "%s <%s>" % (pair.giver.name, pair.giver.email)
                mail = HtmlMail(
                    config['SUBJECT'], config['FROM'], to, config['USERNAME'],
                    config['PASSWORD'])

                mail.send(
                    parse_email(config['TEMPLATE']).format(
                        config['SUBJECT'], pair.giver.name, pair.reciever.name,
                        config['LIMIT'], config['DEATHLINE'])
                )
                print "Emailed %s <%s>" % (pair.giver.name, pair.giver.email)

    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())
