import requests
import codecs,random, re



token='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiIxZmNhMmI5My1jM2U1LTExZTUtOTE5NS0wNmU1MTdjMGExMTMiLCJVc2VyS2V5IjoiMWZjYTJiOTMtYzNlNS0xMWU1LTkxOTUtMDZlNTE3YzBhMTEzIiwiaWF0IjoxNDgwMzg0MTIxLCJleHAiOjE0ODI5NzYxMjF9.LDX-KltwupSFvXYCTUjSeLYI1B1X_OVg0K4M05WKfyY'
# url='http://test-mm.eastasia.cloudapp.azure.com/api'
url='https://uat-lw.mymm.com/api'
if not token:
    api='/auth/login'
    payload={'Username':'qap-dh-213519v5Gn','Password':'Bart'}
    r=requests.post(url+api,data=payload)
    print r.text
    token=r.json()['Token']
    print token
# print token

api='/user/list/mm'
# params={'page':1,'size':howManyUsers, 'search':'qap', 'reverse':'true','statusid':2}
headers = {'Authorization': token}
r=requests.get(url+api,headers=headers)
print 'status code',r.status_code
# print r.text

qap_user = re.findall(r'qap\w{12}', r.text)
print len(qap_user)
for i in range(1000):
    print qap_user[i]


howManyUsers=5000

###### list users and select random from , backup for locust login########
# api='/user/list/consumer'
# params={'page':1,'size':howManyUsers, 'search':'qap', 'reverse':'true','statusid':2}
# headers = {'Authorization': token}
# r=requests.get(url+api,params=params,headers=headers)
# print 'status code',r.status_code
# # print r.text
# data=r.json()['PageData']
# print len(data)
# # print data
# try:
#     user_list=[]
#     for i in range(howManyUsers):
#         user_list.append(data[i]['UserName'])
#
#     print len(user_list)
#     print user_list[random.randrange(0,howManyUsers)]
# except:
#     print 'fail'
#     pass
# randome_style=random.randrange(0,len(data))
# print randome_style
########################################################

# get_ReviewStyleCode=data['PageData'][randome_style]['StyleCode']
# get_ReviewStyleId=data['PageData'][randome_style]['StyleId']
# print get_ReviewStyleCode
# print get_ReviewStyleId



# api_2='/api/product/style/view'
# params={'cc': 'CHS', 'merchantid': 1,'stylecode':'MJ00206'}
# headers = {'Authorization': token}
# r=requests.get(url+api_2,params=params,headers=headers)
# data= r.json()
# print r.status_code
# if r.status_code==401: quit()
#
# # print r.json['UserKey']
# # print r.json['Token']
#
# # f_in=open('raw.txt')
# # data = json.load(f_in)
# #
# ColorImageListMap={}
# for colors in data['ColorImageList']:
#     ColorImageListMap[colors["ColorKey"]]=[colors]
#
# data["ColorImageListMap"]=ColorImageListMap
# data_new={}
# data_new['style']=data
# data_new['MerchantId']=str(data['MerchantId'])
# data_new['deleteSkuIdList']=[]
# data_new['isCategoryChanged']=False
# data_new['isImageChanged']=False
# data_new['isStyleCodeChanged']=False
# data_new['originalStyleCode']=data['StyleCode']
#
# # print data_new
#
# api_3='/api/product/style/update'
# headers = {'Authorization': token,'Content-Type':'application/json'}
# r=requests.post(url+api_3,json=data_new,headers=headers)
# print r.text
#
# f_out = codecs.open('json_out.txt', 'w', 'utf-8')
# json.dump(data_new, f_out, ensure_ascii=False,indent=4)
# f_out.close()



# print data["SkuList"]
# def count_exist_rows(worksheet):
#     count=0
#     for row in worksheet.iter_rows(min_row=2, max_col=1):
#         for cell in row:
#             if cell.value and len(cell.value)>0:
#                 # print(cell.value)
#                 count+=1
#     return count
#     # print ('Exist:',count)
#
# def delete_rows(start,howmanyrows,columns):
#     for i in range(start,howmanyrows+2):
#         for s in columns:
#             ws2['%s%d'%(s,i)]=None
#
#
# def main():
#     delete_exist=0
#     product_count=count_exist_rows(ws1)
#     exist_inventory=count_exist_rows(ws2)
#
#     args = sys.argv[1:]
#     if not args:
#       howManyNewInventory=product_count
#     else:
#         if args[0] == '--d':
#             delete_exist=1
#             del args[0:1]
#             if not args:
#                 print ('Delete all rows!')
#                 howManyNewInventory=0
#             else:
#                 try:
#                     howManyNewInventory=int(args[0])
#                     if howManyNewInventory<0:
#                         print ('\n\tIdiot')
#                         sys.exit(1)
#                 except:
#                     print ("usage: [--d] [Number]. "+'Must specify a number')
#                     sys.exit(1)
#
#
# if __name__ == "__main__":
#   main()
