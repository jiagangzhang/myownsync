import requests
import codecs,random, re
import json, sys

token='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiIxZmNhMmI5My1jM2U1LTExZTUtOTE5NS0wNmU1MTdjMGExMTMiLCJVc2VyS2V5IjoiMWZjYTJiOTMtYzNlNS0xMWU1LTkxOTUtMDZlNTE3YzBhMTEzIiwiaWF0IjoxNDk3ODQ2MTcwLCJleHAiOjE1MDA0MzgxNzB9.1M1BhZy7YxV03hEqdnW6UsLa_qkWRJtAtsXzpQVBfGQ'
url='https://load.mymm.com/'
# url='http://uat-lt.mymm.com'
howManyProdBanners=2
# reference
# raw_json={'Link': 'https://mymm.com/l?sku=332308,332311,332314,332317,332320,332323,332326,332329,332332,332335&h=https://load.mymm.com:443',
# 'BannerImageProgress': '', 'AvailableTo': '2017-07-24 23:59:59', 'Priority': 9, 'BannerTypeId': 2, 'BannerNames': {'CHT': 'qap35', 'CHS': 'qap35', 'EN': 'qap35'},
#  'topBanner': False, 'InterestKeywordIds': [], 'thumbnail0': False, 'thumbnail1': False, 'AvailableFrom': '2017-06-19 00:00:00',
#  'BannerCollectionId': 10, 'ProductIndex': 0, 'StatusId': 2, 'thumbnail2': False, 'IsShowToAll': 0, 'BannerImage': 'd79b8df76244e0715ceab76adef91750',
#  'SkuList': [{'PriceSale': None, 'BrandName': 'Alexander McQueen', 'ImageDefault': 'f167971b1ef7db4ffb08ccac1fff69d4', 'PriceRetail': 4226, 'SkuId': 390835},
#  {'PriceSale': None, 'BrandName': 'Alexander McQueen', 'ImageDefault': '3d5bc6fd569c0852cdcb05b735246616', 'PriceRetail': 58763, 'SkuId': 330832},
#  {'PriceSale': None, 'BrandName': 'Alexander McQueen', 'ImageDefault': '6e47bbc30596259b1054aa03f2225dcb', 'PriceRetail': 4116, 'SkuId': 343366}]}

sku_list=[]
with open ('skuids.csv') as f:
    for line in f:
        l=line.strip()
        if l != 'SkuId' and l is not None:
            sku_list.append(l)
if howManyProdBanners > len(sku_list)/10:
    print ('Too many product banners VS skuid given')
    sys.exit(1)

BrandName_list=[]
PriceRetail_list=[]
PriceSale_list=[]
ImageDefault_list=[]
for n in range(0,howManyProdBanners*10,10):
    api='api/search/style'
    for i in range(3):
        params={'cc':'CHS','skuid':sku_list[n+i]}
        # headers = {'Authorization': token}
        r=requests.get(url+api,params=params)
        print ('search/style',r.status_code)
        raw_data=r.json()
        try:
            BrandName_list.append(raw_data['PageData'][0]['BrandName'])
            sku_index=[d['SkuId'] for d in raw_data['PageData'][0]['SkuList']].index(int(sku_list[n+i]))
            PriceRetail_list.append(raw_data['PageData'][0]['SkuList'][sku_index]['PriceRetail'])
            PriceSale_list.append(raw_data['PageData'][0]['SkuList'][sku_index]['PriceSale'])
            ImageDefault_list.append(raw_data['PageData'][0]['ImageDefault'])
        except:
            print ('something went wrong')
            print (params)
            print (r.text)
            sys.exit(1)
# print (BrandName_list,PriceRetail_list,PriceSale_list,ImageDefault_list)
print (len(BrandName_list),len(PriceRetail_list),len(PriceSale_list),len(ImageDefault_list))

for n in range(howManyProdBanners):
    raw_json={}
    raw_json['Link']='https://mymm.com/l?sku='+','.join(sku_list[n*10+0 : n*10+10])+'&h=https://load.mymm.com:443'
    raw_json['BannerImageProgress']=''
    raw_json['AvailableTo']='2017-06-21 23:59:59'
    raw_json['Priority']=random.choice(range(1,999))
    raw_json['BannerTypeId']=2
    raw_json['BannerNames']={'CHT':'qap-'+str(n),'CHS':'qap-'+str(n),'EN':'qap-'+str(n)}  #not finished
    raw_json['topBanner']=False
    raw_json['InterestKeywordIds']=[]
    raw_json['thumbnail0']=False
    raw_json['thumbnail1']=False
    raw_json['AvailableFrom']='2017-06-19 00:00:00'
    raw_json['BannerCollectionId']=10       # 10 for redzone, 11 for blackzone
    raw_json['ProductIndex']=0
    raw_json['StatusId']=2    # 3 for debug, 2 for in-use
    raw_json['thumbnail2']=False
    raw_json['IsShowToAll']=0
    raw_json['BannerImage']='d79b8df76244e0715ceab76adef91750'
    SkuList=[]
    for i in range(3):
        SkuList.append({'SkuId':sku_list[n*10+i],'BrandName':BrandName_list[n*3+i],'PriceRetail':PriceRetail_list[n*3+i],'PriceSale':PriceSale_list[n*3+i],'ImageDefault':ImageDefault_list[n*3+i]})
    raw_json['SkuList']=SkuList
    api='api/banner/save'
    payload=json.dumps(raw_json)
    headers = {'Content-Type': 'application/json; charset=UTF-8','Authorization':token}
    r=requests.post(url+api,data=payload,headers=headers)
    print ('banner/save',r.status_code)
    if r.status_code != 200:
        print (r.text)

print ('Done %d new product banners'%(n+1))
