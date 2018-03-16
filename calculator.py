#!/usr/bin/env python3

import sys

tax_thr = 3500
pre_saldict = {}
post_saldict = {}

for arg in sys.argv[1:]:
    eid, salary_str = arg.split(':')
    pre_saldict[eid] = salary_str

for eid, salary_str in pre_saldict.items():
    try: 
        salary = int(salary_str)
        si_pay = salary * (8/100 + 2/100 + 0.5/100 + 6/100)
        if salary == tax_thr:
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
        post_salary = format((salary - si_pay - tax),".2f")       
        post_saldict[eid] = post_salary
        post_salpair = str(eid) + ':' + str(post_salary) 
        print(post_salpair)
    except:
        print("Parameter Error")
