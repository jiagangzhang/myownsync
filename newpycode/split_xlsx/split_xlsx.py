import math
import sys
import itertools
from string import ascii_uppercase
from openpyxl import Workbook
from openpyxl import load_workbook


filename = 'split-product'
original_file='forward_25k.xlsx'
file_count = 30
# user_list=[]

# wb=load_workbook(filename=original_file,read_only=True)
wb=load_workbook(filename=original_file)
ws=wb.active

# with open(original_file) as f:
#     user_list=f.readlines()

# how_many_users_per_csv = int(math.floor(len(user_list)/file_count))

# for i in range(1,file_count+1):
#     with open(filename+str(i)+'.csv','w') as fhand:
#         fhand.write(user_list[0])
#         for user in user_list[how_many_users_per_csv*(i-1)+2 : how_many_users_per_csv*i+2]:
#             fhand.write(user)

def count_exist_rows():
    count=0
    for row in ws.iter_rows(min_row=2, max_col=1):
        for cell in row:
            if cell.value and len(cell.value)>0:
                # print(cell.value)
                count+=1
    return count
    # print ('Exist:',count)

# generate a list of A to Z......Z
def iter_all_strings():
    size = 1
    while True:
        for s in itertools.product(ascii_uppercase, repeat=size):
            yield "".join(s)
        size +=1

#  create column from A,B,C to AL,AM... default is 39 columns(AM)
def generate_columnlist(opt=39):
    columnlist=[]
    for s in itertools.islice(iter_all_strings(), opt):
        columnlist.append(s)
    return columnlist

# cache the format of excel of the first row if delete all existing records
def cache_row(n=1, row_size=[]):
    cache=[]
    for s in row_size:
        cache.append(ws['%s%d'%(s,n)].value)
    return cache

def main():
    args = sys.argv[1:]
    if not args:
      print ("will split to %d copies, if you want to specify number of copies, use 'python3 xxx.py numberofcopies'"%file_count)
      howmanynewfiles=file_count
    else:
      try:
          howmanynewfiles=int(args[0])
          if howmanynewfiles<=0:
              print ('\n\tWrong format\tuse python3 xxx.py numberofcopies')
              sys.exit(1)
      except:
          print ("usage: Number. "+'Must specify a number')
          sys.exit(1)

    exist_count=count_exist_rows()
    print ('\n\tExist:',exist_count)
    how_many_rows_per_file = int(math.floor(exist_count/howmanynewfiles))
    print ('how_many_rows_per_file',how_many_rows_per_file)
    columns=generate_columnlist()
    template_row=cache_row(1,columns)

    row_counter=0
    for i in range(1,howmanynewfiles+1):
        wb_new=Workbook()
        # ws_new=wb_new.create_sheet()
        ws_new=wb_new.active

        # fill in data
        ws_new.append(template_row)
        for row in range(2,how_many_rows_per_file + 2):
            for col in range(1,len(columns)):
                ws_new.cell(row=row,column=col).value=ws.cell(row=row+row_counter,column=col).value
            # ws_new.append(cache_row(row,columns))
            # col_d = ws[row] # 0-indexing
            # for idx, cell in enumerate(col_d, 1):
            #     ws_new.cell(row=idx, column=4).value = cell.value #1-indexing
        # for row in range(row_counter,how_many_rows_per_file + row_counter):
        #     ws_new.append(ws[row])
        #     print(row)
        # ws_new[2:5]=ws[2:5]

        row_counter=row_counter+how_many_rows_per_file
        print (row_counter)
        print(filename+'-'+str(i))
        wb_new.save(filename+'-'+str(i)+'.xlsx')

if __name__ == "__main__":
  main()
