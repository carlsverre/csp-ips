import ipaddress
import json
from urllib.request import urlopen, Request
import re
import sys

def fetchjson(url):
    return json.load(urlopen(url))

def expand(cidr):
    net = ipaddress.ip_network(cidr)
    return map(lambda n: str(n), net)

def aws():
    d = fetchjson('https://ip-ranges.amazonaws.com/ip-ranges.json')
    for prefix in d["prefixes"]:
        for ip in expand(prefix.get("ip_prefix", prefix.get("ipv6_prefix"))):
            yield ip

def gcp():
    d = fetchjson('https://www.gstatic.com/ipranges/cloud.json')
    for prefix in d["prefixes"]:
        for ip in expand(prefix.get("ipv4Prefix", prefix.get("ipv6Prefix"))):
            yield ip

def azure():
    # find download link lol
    index = urlopen(Request('https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519', headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    })).read().decode('utf-8')
    reDownload = re.compile(r'https://download.microsoft.com/download[^"]+')
    direct_url = reDownload.search(index)[0]

    d = fetchjson(direct_url)
    for o in d["values"]:
        for prefix in o["properties"]["addressPrefixes"]:
            for ip in expand(prefix):
                yield ip

CSP = {
    "aws": aws,
    "azure": azure,
    "gcp": gcp,
}

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in CSP:
        print(f"usage: {sys.argv[0]} {'|'.join(CSP.keys())}")
        sys.exit(1)

    for ip in CSP[sys.argv[1]]():
        sys.stdout.write(ip)
        sys.stdout.write("\n")
