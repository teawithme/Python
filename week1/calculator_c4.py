#!/usr/bin/env python3

import sys
import os
from multiprocessing import Process, Queue 

argvs = sys.argv

if argvs[1] == '-c'  and argvs[3] == '-d' and argvs[5] == '-o':
    cfgfile = argvs[2]
    usrfile = argvs[4]
    salfile = argvs[6]

def openread(filename, format):
    if os.path.exists(filename):
        with open(filename,format) as file:
            filedata = file.readlines()
            return filedata
    else:
        print(filename, ' not exists')
        sys.exit(-1)

queue = Queue()

#conn1, conn2 = Pipe()
#conn3, conn4 = Pipe()

def getinput():

    cfgraw = openread(cfgfile,'r')
    uraw = openread(usrfile,'r')
    
    #print(cfgraw)
    #print(uraw)
    rawdata = []
    
    rawdata.append(cfgraw)
    rawdata.append(uraw)
    #print(rawdata)
    queue.put(rawdata)

def cal():
    tax_thr = 3500
    sidict = {}
    pre_saldict = {}
    post_saldict = {}
    
    rawdata = queue.get()
    cfgraw = rawdata[0]
    uraw = rawdata[1]

    sirate = 0
    for cfg in cfgraw:
        try:
            siname, value = cfg.split('=')
            sidict[siname] = float(value)
            if siname != 'JiShuL ' and siname != 'JiShuH ':
                sirate += sidict[siname]
        except:
            print('Configure File Format Error')

    for user in uraw:
        try:
            eid, salary_str = user.split(',')
            pre_saldict[eid] = salary_str
        except:
            print('User File Format Error')
    #print(pre_saldict)
    outdata = []
    for eid, salary_str in pre_saldict.items():
        try: 
            salary = int(salary_str)
            if salary < sidict['JiShuL ']:
                si_pay = sidict['JiShuL '] * sirate
            elif salary > sidict['JiShuH ']:
                si_pay = sidict['JiShuH '] * sirate
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
            data_per = str(eid) + ',' + str(salary) + ',' + str(format(si_pay,".2f")) + ',' + str(format(tax,".2f")) + ',' + str(post_salary) + '\n'
            outdata.append(data_per)    
        except:
            print("Parameter Error")
    queue.put(outdata)

def output():
    outdata = queue.get()
    with open(salfile,'a') as file:
        for item in outdata:
            file.write(item)

def main():
    Process(target = getinput).start()
    Process(target = cal).start()
    Process(target = output).start()

if __name__ == '__main__':
    main()
    


