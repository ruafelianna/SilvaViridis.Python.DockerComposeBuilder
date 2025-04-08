from enum import Enum

class AppProtocol(Enum):
    telnet = 0
    ftp = 1
    tftp = 2
    nfs = 3
    smtp = 4
    lpd = 5
    xdm = 6
    snmp = 7
    dns = 8
    dhcp = 9
    http = 10
    https = 11
    pop = 12
    irc = 13
    mime = 14
    rdp = 15
    sip = 16
    xmpp = 17
