# ordnance [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
Python script to perform layer 7 stress test on your web server.  

[![asciicast](https://asciinema.org/a/pOMdeF7iJJApC05N5mBv9DtSZ.png)](https://asciinema.org/a/pOMdeF7iJJApC05N5mBv9DtSZ)

## Installation

To bypass CloudFlare protection, [cfscrape](https://github.com/Anorov/cloudflare-scrape/) library is used for the generation of `cf_clearance` token.    
```
$ sudo pip3 install -r requirements.txt
$ chmod +x ordnance.py
```

## Usage

```
usage: ordnance.py [-h] --host [HOST] [-p PORT] [-d DIR] [-t THREADS] [-s]

optional arguments:
  -h, --help            show this help message and exit
  --host [HOST]         Web server, i.e: example.com
  -p PORT, --port PORT  Port number (Default 80)
  -d DIR, --dir DIR     Web path, i.e: admin/index.php (Default: /)
  -t THREADS, --threads THREADS
                        Number of threads (Default 100)
  -s, --ssl             HTTP/HTTPS (Default HTTP)
```

Basic usage:  
`$ ./ordnance.py --host 127.0.0.1`  

If the web server is running on a different port aside from 80 and with 120 threads instead of the default 100:  
`$ ./ordnance.py --host 127.0.0.1 -p 8080 -t 120`

If the host is equipped with SSL/TLS certificate:  
`$ ./ordnance.py --host 127.0.0.1 --ssl`

In case you want to specify a web path, for example `/home/index.php`:  
`$ ./ordnance.py --host 127.0.0.1 -d home/index.php` 

## Disclaimer

```
[!] Legal disclaimer: Usage of this script for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. I assume no liability and are not responsible for any misuse or damage caused.
```
