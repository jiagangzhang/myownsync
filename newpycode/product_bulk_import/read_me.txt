read_me

change the template.xlsx BrandCode to your merchant's BrandCode, without the space
output file is the xxx_verify.xlsx

command usage:  python3 create_product_xlsx_py.py [--d] number
	1. --d , optional, delete the xlsx file's existing records. if not presented, will append new rows at bottom row
	2. number, required, how many new products to create


tip: can change how many rows to remain by changing:
    if delete_exist:
        delete_rows(2,exist_count,column_list)  // change 2 to 102 if 100 rows to remain
        exist_count=0							// don't forget to set exist_count=100