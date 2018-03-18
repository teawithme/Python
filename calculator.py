#!/usr/bin/env python3

import sys
import os

argvs = sys.argv

if argvs[1] == '-c'  and argvs[3] == '-d' and argvs[5] == '-o':
    cfgfile = argvs[2]
    usrfile = argvs[4]
    salfile = argvs[6] 

if os.path.exists(cfgfile):
    with open(cfgfile,'r') as file:
        cfgraw = file.readlines()
else:
    print('Configure file not exists')
    sys.exit(-1)

if os.path.exists(usrfile):
    with open(usrfile,'r') as file:
        uraw = file.readlines()
else:
    print('User file not exists')
    sys.exit(-1)

tax_thr = 3500
sidict = {}
pre_saldict = {}
post_saldict = {}

sirate = 0
for cfg in cfgraw:
    try:
        siname, value = cfg.split('=')
        sidict[siname] = float(value)
        if siname != 'JiShuL ' and siname != 'JiShuH ':
            sirate += sidict[siname]
    except:
        print('Configure File Format Error')
        #print(cfg)
#print(sidict)
#print(sirate)
for user in uraw:
    try:
        eid, salary_str = user.split(',')
        pre_saldict[eid] = salary_str
    except:
        print('User File Format Error')
#print(pre_saldict)

for eid, salary_str in pre_saldict.items():
    #try: 
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
        with open(salfile,'a') as file:
            file.write(str(eid) + ',' + str(salary) + ',' + str(format(si_pay,".2f")) + ',' + str(format(tax,".2f")) + ',' + str(post_salary) + '\n')
    #except:
        #print("Parameter Error")
