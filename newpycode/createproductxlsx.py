#! /usr/bin/env python3
import openpyxl

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


howmanynewproducts=10
exist_count=0

for row in ws.iter_rows(min_row=1, max_col=1):
    for cell in row:
        if cell.value and len(cell.value)>0:
            # print(cell.value)
            exist_count+=1

print (exist_count)
# for i in range(1,100):
#     a=ws['A%d'%(i)]
#     if a.value and len(a.value)>0:
#         print(a.value)
#         count+=1

for newrow in range(howmanynewproducts):

    newrow+=1
