import sys,os,getopt,time, select, subprocess,re
from threading import Thread
from IPy import IP

OS="Windows 10"
version="2.4"
version_full="scan-network v."+version
Action="range_scan" # Default action
a=False
x=1
y=254
ping_delay=0 # in seconds
ip="192.168.1.*"

' Copyleft by WebNuLL no any right reserved ;-)'

def usage():
        'Shows program usage and version, lists all options'

        print(version_full+" for "+OS+". A simple local network scanner.")
        print("Usage: scan-network [long GNU option] [option] from [option] to")
        print("")
        print(" --from (-f) range of ip adresses to start, default is 1")
        print(" --to (-t) range of ip adresses where to end, default is 254")
        print(" --ip (-i) mask of adresses to scan, for example 192.168.1, default 192.168.1.*")
        print(" --delay (-d) delay between pings, default is 0 second")
        print(" --load-file (-l) scan ip adresses listed in file")
        print(" --stdin (-s) grab list of ip adresses from stdin")
        print(" --alive (-a) show alive ip adresses only")
        print(" --help this screen")

class PingThread(Thread):
    def __init__(self,Adress):
        Thread.__init__(self) # initialize thread

        # variables
        self.Adress = Adress
        self.Status = ''
        self.ComputerName=""

    def run(self):
        try:
            get = subprocess.getoutput("ping -a "+self.Adress+" -c 1")
        except OSError:
            print("Cannot execute ping, propably you dont have enough permissions to create process")
            sys.exit(1)

        ResponseTime = False

        tmp=re.search('(?<=Pinging) (.*) \[', get)
        ComputerName='' if tmp is None else tmp.group(1)
        self.ComputerName=ComputerName

        tmp=re.search('time(.*) ', get)
        Status='' if tmp is None else tmp.group(1) 
        Status=Status[Status.find('=')+1:]
        #timed out
        Status='' if Status =='d' else Status
        self.Status = Status
def main():
        'Main function'
        global Action, x, y, ping_delay, ip,a

        try:
            opts, args = getopt.getopt(sys.argv[1:], "sl:d:i:f:t:h:a", ["from=", "to=", "help","alive", "delay=", "ip=", "stdin", "load-file="]) # output=

        except getopt.GetoptError as err:
                print("Error: "+str(err)+", Try --help for usage\n\n")
                # usage()
                sys.exit(2)

        for o, a in opts:
                if o in ("-h", "--help"):
                        usage()
                        sys.exit()
                if o in ("-a", "--alive"):
                        a=True
                if o in ("-f", "--from"):
                        try:
                                x=float(a)
                        except ValueError:
                                print("--from argument is taking only numeric values")
                                sys.exit(2);

                if o in ("-t", "--to"):
                        try:
                                y=float(a)
                        except ValueError:
                                print ("--to argument is taking only numeric values")
                                sys.exit(2);

                if o in ("-d", "--delay"):
                        try:
                                ping_delay=float(a)
                        except ValueError:
                                print("--delay argument is taking only numeric values")
                                sys.exit(2);

                if o in ("-i", "--ip"):
                        ip=a
                if o in ("-l", "--load-file"):
                        Action="file_scan"
                        FileToScan = a
                if o in ("-s", "--stdin"):
                        Action="stdin_scan"

        if len(opts) == 0:
            print("scan-network for "+OS+",  See --help for usage")
            sys.exit()

        if Action == "range_scan":
            doRangeScan()
        elif Action == "file_scan":
            if os.access(FileToScan, os.R_OK):
                FileHandler = open(FileToScan, "r")
                doListScan(FileHandler.read())
                FileHandler.close()
            else:
                print("Cannot open input file "+FileToScan)

        elif Action=="stdin_scan":
            if select.select([sys.stdin,],[],[],0.0)[0]:
                Adresses = sys.stdin.read()
                doListScan(Adresses)
            else:
                print("STDIN is empty")

def doListScan(inputList):
    global a
    ListOfHosts = list()
    Lines = inputList.split("\n")

    for Line in Lines: # Line == IP Adress or list of ip adresses seperated by comma ","
        Multiples = Line.split(',')

        for IPAdress in Multiples:
            try:
                IP(IPAdress)
            except ValueError:
                continue
            else:
                Ping = PingThread(IPAdress)
                ListOfHosts.append(Ping)
                Ping.start()

    for Host in ListOfHosts:
       Host.join()
       if Host.Status == '':
          if not a:
             print(Host.Adress+" not responding, offline")
       else:
          if Host.ComputerName.find(Host.Adress)>-1:
              print(Host.Adress+" responds in "+str(Host.Status))
          else:
              print(Host.Adress+" "+Host.ComputerName+" responds in "+str(Host.Status))

       time.sleep(ping_delay)

def doRangeScan():
        global x, y, ping_delay, ip,a
        i=int(x)
        to=int(y)
        ListOfHosts = list()

        try:
            if (y-x) > 0:
                to=to+1
                while i != to:
                    # use system ping and return results
                    current_ip = ip.replace('*', str(i))
                    # Single ping thread
                    Ping = PingThread(current_ip)
                    i=i+1
                    # Append it to list of pinged hosts
                    ListOfHosts.append(Ping)
                    Ping.start()
                    
                print("Adresses to scan: %1.0f" % (y-x))
                print("Ping "+ip.replace('*', "{"+str(int(x))+"-"+str(int(y))+"}"))
                print("Delay: "+str(ping_delay)+"s")

                for Host in ListOfHosts:
                    Host.join()
                    if Host.Status == '':
                        if not a:
                            print(Host.Adress+" not responding, offline")
                    else:
                        if Host.ComputerName.find(Host.Adress)>-1:
                            print(Host.Adress+" responds in "+str(Host.Status))
                        else:
                            print(Host.Adress+" "+Host.ComputerName+" responds in "+str(Host.Status))

                    time.sleep(ping_delay)
            else:
                print ("No ip range to scan, please select valid one with --from, --to and --ip")
        except Exception as e:
            print("There was an running the scan, propably your resources are restricted. "+str(e))
            sys.exit(1)

    
if __name__ == "__main__":
    main()
