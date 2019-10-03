#!/usr/bin/env python
import argparse
import dns.resolver
import re
import sys

# Domain Data Structure
_DOMAIN = {
    'name': "",
    'mx': [],
    'provider': [],
}

# Proofpoint Regex
_RE_PROOFPOINT = '^(mx[0-9]-[a-z]{2}[0-9]{1}\.ppe-hosted\.com\.)$'

# O365 Regex - Less Stringent than PP
_RE_365 = '^(.*mail\.protection\.outlook\.com\.)$'

# Build Arguments
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--domain', type=str,
                    help='Domain to query.', required=True)
parser.add_argument('-n', '--nameserver', type=str,
                    help='Nameserver to use when querying DNS records.')
args = parser.parse_args()

# Exit if domain not provided with non-zero
if not args.domain:
    sys.exit(2)
else:
    # Set Domain
    _DOMAIN['name'] = args.domain
try:
    # Try running through MX Records and add to _DOMAIN
    answers = dns.resolver.query(args.domain, 'MX')
    for rdata in answers:
        _DOMAIN['mx'].append(rdata.exchange.to_text())
        print('MX for {}'.format(rdata.exchange))
# No Records found
except dns.resolver.NoAnswer as e:
    print("No MX for domain {}".format(args.domain))

# Determine who owns the MX
for mx in _DOMAIN['mx']:
    if re.match(_RE_PROOFPOINT,str(mx)):
        print("Proofpoint Detected.")
    elif re.match(_RE_365, str(mx)):
        print("Office 365 Detected")


def check_365(domain):
    """
    Check if Domain has an A record @ O365
    :param domain:
    :return: 365 String if True
    """
    try:
        domain_dash = domain.replace('.','-')
        name_365 = '{}.mail.protection.outlook.com'.format(domain_dash)
        answers = dns.resolver.query(name_365,'A')
        res = []
        for rdata in answers:
            # Append to res - TODO: Remove this step
            res.append(rdata.to_text())
        # TODO: Modify This if this data is not needed
        if len(res) >= 2:
            # Append 365 Name to Provider
            _DOMAIN['provider'].append(name_365)
            # Return the 365 A Record
            return name_365
    except dns.resolver.NoAnswer as e:
        print("No response @ 365")
        return False

a = check_365(_DOMAIN['name'])
if a:
    print(a)
print(_DOMAIN)