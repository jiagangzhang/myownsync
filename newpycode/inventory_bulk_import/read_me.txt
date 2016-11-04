read_me

input is product_list.xlsx
output file is the dataheavy_inventory.xlsx

command usage:  python3 create_product_xlsx_py.py [--d] [number]
	1. no arguments, append all products from product_list.xlsx to dataheavy_inventory.xlsx
	1. --d , optional, delete the xlsx file's existing records.
	2. number, optional, how many new inventory to create, if >product list, will report error


tip: can change how many rows to remain by changing:
    if delete_exist:
        delete_rows(2,exist_count,column_list)  // change 2 to 102 if 100 rows to remain
        exist_count=0							// don't forget to set exist_count=100