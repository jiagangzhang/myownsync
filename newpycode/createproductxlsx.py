#! /usr/bin/env python3
import openpyxl
import random

from string import ascii_uppercase
import itertools

from openpyxl import Workbook
from openpyxl import load_workbook
# wb = Workbook()
#
# # grab the active worksheet
# ws = wb.active
#
# # Data can be assigned directly to cells
# ws['A1'] = 42
#
# # Rows can also be appended
# ws.append([1, 2, 3])
#
# # Python types will automatically be converted
# import datetime
# ws['A2'] = datetime.datetime.now()
#
# # Save the file
# wb.save("sample.xlsx")

wb=load_workbook('dataheavy_products_py.xlsx')
ws=wb.active


howmanynewproducts=1000
exist_count=0

for row in ws.iter_rows(min_row=1, max_col=1):
    for cell in row:
        if cell.value and len(cell.value)>0:
            # print(cell.value)
            exist_count+=1

print ('Exist:',exist_count)
# for i in range(1,100):
#     a=ws['A%d'%(i)]
#     if a.value and len(a.value)>0:
#         print(a.value)
#         count+=1

for i in range(exist_count+1,exist_count+howmanynewproducts+1,4):
    randstr=''.join(random.choice('0123456789'+ascii_uppercase) for a in range(11))
    for k,v in {'-PINK-S':123,'-PINK-M':456,'-PINK-L':789,'-PINK-XL':101}.items():
        ws['A%d'%(i)]='qap-dh-'+randstr
        ws['B%d'%(i)]='qap-dh-'+randstr+k
        ws['C%d'%(i)]='h-'+randstr+str(v)
        ws['D%d'%(i)]=ws['D2'].value
        ws['E%d'%(i)]=0
        ws['F%d'%(i)]='CN'
        ws['H%d'%(i)]=0
        ws['I%d'%(i)]=ws['I2'].value
        ws['O%d'%(i)]=0
        ws['P%d'%(i)]=ws['P2'].value
        ws['Q%d'%(i)]=ws['Q2'].value
        ws['V%d'%(i)]=ws['V2'].value
        ws['W%d'%(i)]=ws['W2'].value
        ws['X%d'%(i)]=ws['X2'].value
        ws['Y%d'%(i)]=ws['Y2'].value
        ws['Z%d'%(i)]=ws['Z2'].value
        ws['AA%d'%(i)]=ws['AA2'].value
        ws['AB%d'%(i)]=ws['AB2'].value
        ws['AC%d'%(i)]=ws['AC2'].value
        ws['AD%d'%(i)]=ws['AC2'].value
        ws['AE%d'%(i)]=ws['AE2'].value
        ws['AF%d'%(i)]=ws['AF2'].value
        ws['AG%d'%(i)]=ws['AG2'].value
        ws['AH%d'%(i)]=ws['AH2'].value
        ws['AI%d'%(i)]=ws['AI2'].value
        ws['AJ%d'%(i)]=ws['AJ2'].value
        ws['AK%d'%(i)]=0
        ws['AL%d'%(i)]=1
        # ws['AM%d'%(i)]='Active'
        # print (ws['A%d'%(i)].value, ws['B%d'%(i)].value, ws['C%d'%(i)].value,ws['D%d'%(i)].value,ws['I%d'%(i)].value,ws['W%d'%(i)].value,ws['AJ%d'%(i)].value)
        i+=1
        # print ('i in dic loop is: ',i)
    # print ('i in outer loop is:',i)

print ('final i:',i)

# print the value of a specif row
# def iter_all_strings():
#     size = 1
#     while True:
#         for s in itertools.product(ascii_uppercase, repeat=size):
#             yield "".join(s)
#         size +=1
#
# printlist=[]
# for s in itertools.islice(iter_all_strings(), 39):
#     printlist.append(s)
#
# for s in printlist:
#     print (ws['%s%d'%(s,i-1)].value)
# #######################################

wb.save('dataheavy_products_py.xlsx')
