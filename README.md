# scan-network for Windows 10
scan-network is a simple IP range scanner in Windows 10.

## Getting Started
The program can run in Windows 10. 

### Prerequisites
* You need run command prompt as administrator to try it.
* [Download and install Python3](https://www.python.org/downloads/).

### Installing
Download windows\scan-network.py

## Running the tests
### Show help
```
vereperrot@desktop>python scan-network.py --help
scan-network v.2.4 for Windows 10. A simple local network scanner.
Usage: scan-network [long GNU option] [option] from [option] to

 --from (-f) range of ip adresses to start, default is 1
 --to (-t) range of ip adresses where to end, default is 254
 --ip (-i) mask of adresses to scan, for example 192.168.1, default 192.168.1.*
 --delay (-d) delay between pings, default is 0 second
 --load-file (-l) scan ip adresses listed in file
 --stdin (-s) grab list of ip adresses from stdin
 --alive (-a) show alive ip adresses only
 --help this screen
 ```
 
### Scan range from 192.168.1.100 to 192.168.1.110
```
vereperrot@desktop>python scan-network.py --from=100 --to=110 --ip 192.168.1.*
Adresses to scan: 10
Ping 192.168.1.{100 to 110}
Delay: 1
192.168.1.100 DESKTOP2 responds in 0.0013279914856
192.168.1.101 not responding, offline
192.168.1.102 DESKTOP1 responds in 0.000174999237061
192.168.1.103 not responding, offline
192.168.1.104 not responding, offline
192.168.1.105 not responding, offline
192.168.1.106 not responding, offline
192.168.1.107 not responding, offline
192.168.1.108 not responding, offline
192.168.1.109 not responding, offline
192.168.1.110 not responding, offline
```

### Scan range from a file
```
 scan-network.py -l examples/example-ip-list # scan ip adresses from file
 cat example-ip-list
 ~
 192.168.100.1
 192.168.100.2
 ~
```

### Scan from stdin
```
 cat examples/example-ip-list | scan-network -s # scan from stdin
 echo "192.168.1.100,192.168.1.101,192.168.1.102,192.168.1.103,192.168.1.104,192.168.1.107,192.168.1.108" | scan-network -s # scan from stdin
```

## Built With
* [Python](https://www.python.org/) - the Python Programming Language

## Versioning
* Version 2.4:
    * [+] Add a option for listing all alive ip address.
    * [*] Modify code for running on Windows 10.
    * [*] Modify code using Python 3.
    * [+] Find a computer name.

## Authors
* [webnull](https://github.com/webnull) - Initial work
* [vereperrot](https://github.com/vereperrot) - scan-network for Windows 10. 
    * [Vere Perrot Blog](http://vereperrot.github.io/):rocket:
    * Do you like my work? [Please have a cup of coffee!](https://www.paypal.me/vereperrot/4USD):coffee:




