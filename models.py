class Person:
    def __init__(self, name, email, partner):
        self.name = name
        self.email = email
        self.partner = partner

    def __str__(self):
        return "%s <%s>" % (self.name, self.email)


class Pair:
    def __init__(self, giver, reciever):
        self.giver = giver
        self.reciever = reciever

    def __str__(self):
        return "%s ---> %s" % (self.giver.name, self.reciever.name)


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg
