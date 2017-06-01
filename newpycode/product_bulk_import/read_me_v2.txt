read_me_v2



output file is the xxx_verify.xlsx

command usage:  python3 create_product_xlsx_py.py [--d] number [Brandcode_prefix] [Number of Brands]
	1. --d , optional, delete the xlsx file's existing records. if not presented, will append new rows at bottom row
	2. number, required, how many new products to create
	3. Brandcode_prefix and Number of Brands are optional, but have to be provided together. If not presented, will use 'demo' as default prefix and 1 as number of brand

example:
	python3 create_product_xlsx_py_v2.py --d 101 revolve 5
		create a new excel file with 101 rows of skus, with 5 brands, brands name from revolve1 to revolve5

tip: can change how many rows to remain by changing:
    if delete_exist:
        delete_rows(2,exist_count,column_list)  // change 2 to 102 if 100 rows to remain
        exist_count=0							// don't forget to set exist_count=100