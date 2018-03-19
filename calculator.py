#! /usr/bin/env python3

import getopt, sys
import os
import configparser
from multiprocessing import Process, Queue 
from datetime import datetime

def usage():
  print('Usage: calculator.py -C cityname -c configfile -d userdata -o resultdata')

def optparser():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "C:c:d:o:h", ["help"])
        opts_dcit = dict((x, y) for x, y in opts)

        cityname = opts_dcit.get('-C')
        if cityname is None:
            cityname = 'DEFAULT'
        else:
            cityname = cityname.upper()

        cfgfile = opts_dcit.get('-c')
        if cfgfile is None:
            print('Configure file not defined')
            sys.exit(2)
        usrfile = opts_dcit.get('-d')
        if usrfile is None:
            print('User file not defined')
            sys.exit(2)
        salfile = opts_dcit.get('-o')
        if salfile is None:
            print('Result file not defined')
            sys.exit(2)
    except getopt.GetoptError as err:
    	# print help information and exit:
    	print(err)
    	usage()
    	sys.exit(2)
    for o, a in opts:
    	if o in ("-h", "--help"):
    		usage()
    		sys.exit()
    return {'cityname':cityname, 'cfgfile':cfgfile, 'usrfile':usrfile,'salfile':salfile}

def readcfg(filename):
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(filename)
    #for key in config['DEFAULT']: 
        #print(key)
    return config

def openread(filename, format):
    if os.path.exists(filename):
        with open(filename,format) as file:
            filedata = file.readlines()
            return filedata
    else:
        print(filename, ' not exists')
        sys.exit(-1)
    
def getinput():
    opts = optparser()
    
    cfgraw = readcfg(opts['cfgfile'])
    uraw = openread(opts['usrfile'],'r')

    rawdata = []
    rawdata.append(opts['cityname'])
    rawdata.append(cfgraw)
    rawdata.append(uraw)
    rawdata.append(opts['salfile'])
    queue.put(rawdata)

def cal():
    tax_thr = 3500
    sidict = {}
    pre_saldict = {}
    post_saldict = {}
    
    rawdata = queue.get()
    cityname = rawdata[0]
    #print(cityname)
    cfgraw = rawdata[1]
    uraw = rawdata[2]
    salfile = rawdata[3]
    #print(cfgraw[cityname])

    sirate = 0
    for key in cfgraw[cityname]: 
        #print(key)
        sidict[key] = float(cfgraw[cityname][key])
        if key != 'JiShuL' and key != 'JiShuH':
            sirate += sidict[key]
    #print(sidict)
    for user in uraw:
        try:
            eid, salary_str = user.split(',')
            pre_saldict[eid] = salary_str
        except:
            print('User File Format Error')
    
    outdata = []
    outdata.append(salfile)
    for eid, salary_str in pre_saldict.items():
        try: 
            salary = int(salary_str)
            if salary < sidict['JiShuL']:
                si_pay = sidict['JiShuL'] * sirate
            elif salary > sidict['JiShuH']:
                si_pay = sidict['JiShuH'] * sirate
            else:
                si_pay = salary * sirate
            if salary <= tax_thr:
                tax_salary = 0
            else:
                tax_salary = salary - si_pay - tax_thr
        
            if tax_salary <= 1500:
                rate = 3/100
                deduct = 0
            elif 1500 < tax_salary <= 4500: 
                rate = 10/100 
                deduct = 105
            elif 4500 < tax_salary <= 9000:
                rate = 20/100
                deduct = 555
            elif 9000 < tax_salary <= 35000:
                rate = 25/100
                deduct = 1005
            elif 35000 < tax_salary <= 55000:
                rate = 30/100
                deduct = 2755
            elif 55000 < tax_salary <= 80000:
                rate = 35/100
                deduct = 5505
            elif 80000 < tax_salary:
                rate = 45/100
                deduct = 13505
            tax = tax_salary * rate - deduct
            #print('deduct',tax_salary)
            #print('tax ', tax)
            post_salary = format((salary - si_pay - tax),".2f")       
            #post_saldict[eid] = post_salary
            #post_salpair = str(eid) + ':' + str(post_salary) 
            #print(post_salpair)
            t = datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S')
            data_per = str(eid) + ',' + str(salary) + ',' + str(format(si_pay,".2f")) + ',' + str(format(tax,".2f")) + ',' + str(post_salary) + ',' + t + '\n'
            outdata.append(data_per)    
        except:
            print("Parameter Error")
    queue.put(outdata)

def output():
    outdata = queue.get()
    salfile = outdata.pop(0)
    with open(salfile,'a') as file:
        for item in outdata:
            file.write(item)

queue = Queue()

def main():
    Process(target = getinput).start()
    Process(target = cal).start()
    Process(target = output).start()

if __name__ == "__main__":
	main()
