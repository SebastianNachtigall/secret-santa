import random
import os

import yaml

from models import Pair


CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.yml')


def choose_reciever(giver, recievers):
    choice = random.choice(recievers)
    if giver.partner == choice.name or giver.name == choice.name:
        if len(recievers) is 1:
            raise Exception('Only one reciever left, try again')
        return choose_reciever(giver, recievers)
    else:
        return choice


def create_pairs(g, r):
    givers = g[:]
    recievers = r[:]
    pairs = []
    for giver in givers:
        try:
            reciever = choose_reciever(giver, recievers)
            recievers.remove(reciever)
            pairs.append(Pair(giver, reciever))
        except:
            return create_pairs(g, r)
    return pairs


def parse_yaml(yaml_path=CONFIG_PATH):
    return yaml.load(open(yaml_path))


def parse_email(template):
    """Parse HTML email from given template"""

    f = open(template, 'r')
    mail_html = ""
    while 1:
        line = f.readline()
        if not line:
            break
        mail_html += line

    f.close()
    return mail_html
