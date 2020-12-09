# Why?
Sometimes you want to quickly determine if an IP is owned by a CSP.

# But why not just output all the CIDR's?
A couple possible reasons:
* Sometimes you need to do the lookup in a system which doesn't support comparing an IP to a CIDR
* You want to build an optimized lookup table
* You want some simple starting code with no dependencies (other than python3)

# Usage
1. Download process.py
2. Run

```
~/csp $ python3 process.py
usage: process.py aws|azure|gcp

~/csp $ python3 process.py aws | head -n 10
3.5.140.0
3.5.140.1
3.5.140.2
3.5.140.3
3.5.140.4
3.5.140.5
3.5.140.6
3.5.140.7
3.5.140.8
3.5.140.9
...
```

# Future work (contributions welcome)
* Use published ASN's from each of the cloud providers rather than a janky JSON
  API
* Add more CSP's
* Customize the output format to include the IP type (ipv4 vs ipv6)
* Filter the output by IP type (ipv4 vs ipv6)
