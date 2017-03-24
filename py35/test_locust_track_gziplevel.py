from locust import HttpLocust, TaskSet, task, Locust
import sys,random,requests,re, gzip, json, uuid

# AC_token='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiIxZmNhMmI5My1jM2U1LTExZTUtOTE5NS0wNmU1MTdjMGExMTMiLCJVc2VyS2V5IjoiMWZjYTJiOTMtYzNlNS0xMWU1LTkxOTUtMDZlNTE3YzBhMTEzIiwiaWF0IjoxNDc5OTU0NDAwLCJleHAiOjE0ODI1NDY0MDB9.3nj2DHf4Ppq7LW_SxlH1YKLJ48TjVse-y4cirHmTsLk'
# userkey=''

merchantid = 1
printTask = True
printError = True
url='http://test-mm.eastasia.cloudapp.azure.com' #this is for /track/t only, because track does not have a leading /api
# url='https://uat-lt.mymm.com'

# url='http://test-mm.eastasia.cloudapp.azure.com/api' #this is for the most apis
# url='https://uat-lw.mymm.com/api'
# howManyUsers=5000
fname='users.csv'
# #### retrieve username list from users.csv file, comment out when debug#######
# with open(fname) as f:
#     user_list = re.findall(r'qap\w{12}', f.read())

user_list=['qap-dh-213516ATEt', 'qap-dh-213519v5Gn', 'qap-dh-213517FblF', 'qap-dh-213518Fa5I', 'qap-dh-213518qgcR', 'qap-dh-213518qTVV', 'qap-dh-213518TRBQ', 'qap-dh-213518yKSk', 'qap-dh-213518YSvf', 'qap-dh-213519YNEJ', 'qap-dh-216456wCG3', 'qap-dh-216493shPR', 'qap-dh-216499kWz6', 'qap-dh-217063yMAh', 'qap-dh-217070TblX', 'qap-dh-217079KCMV', 'qap-dh-217307qlPg', 'qap-dh-217389CGUl', 'qap-dh-2174983aZl', 'qap-dh-217276PFk1', 'qap-dh-219333x41v', 'qap-dh-2193581s1f', 'qap-dh-219401hsyY', 'qap-dh-219883XzR5', 'qap-dh-220030G0aq', 'qap-dh-2203185ziM', 'qap-dh-220165cbNo', 'qap-dh-220345F6Vm', 'qap-dh-2203514LV7', 'qap-dh-220369qoxQ', 'qap-dh-222444xLHv', 'qap-dh-2228502R34', 'qap-dh-222584kkiD', 'qap-dh-222648lO35', 'qap-dh-223284ppm7', 'qap-dh-223557aFCD', 'qap-dh-2237807XZa', 'qap-dh-2239852TE3', 'qap-dh-224140RElt', 'qap-dh-224227PYIj', 'qap-dh-2266809tUi', 'qap-dh-2268489Hvy', 'qap-dh-227328PlPk', 'qap-dh-227334HGxs', 'qap-dh-227346z9YT', 'qap-dh-227414DIgk', 'qap-dh-227742p3P0', 'qap-dh-227797JKad', 'qap-dh-227834HEOD', 'qap-dh-227841OQGD', 'qap-dh-229133nc7i', 'qap-dh-229654Sh6H', 'qap-dh-230012FQU2', 'qap-dh-230056yMDe', 'qap-dh-230091uoW8', 'qap-dh-230136pTUO', 'qap-dh-230452rQba', 'qap-dh-230481wZQ8', 'qap-dh-230529dlr6', 'qap-dh-2305355Kdf', 'qap-dh-2313675dG3', 'qap-dh-232371VLUN', 'qap-dh-232469SgIF', 'qap-dh-232650KTNo', 'qap-dh-232831naer', 'qap-dh-232983azCZ', 'qap-dh-233009xDX5', 'qap-dh-233077xPYe', 'qap-dh-233254mC1G', 'qap-dh-233271QoMg', 'qap-dh-234020tJCz', 'qap-dh-234968GV8d', 'qap-dh-235545WBkG', 'qap-dh-235613hCzH', 'qap-dh-235643PPKJ', 'qap-dh-235899KaDe', 'qap-dh-236045r6U0', 'qap-dh-236219hIWX', 'qap-dh-236600DQ2F', 'qap-dh-236667QEqR', 'qap-dh-237613m7A1', 'qap-dh-239317A3xD', 'qap-dh-239752JSl9', 'qap-dh-240120HaC8', 'qap-dh-240190Yluf', 'qap-dh-240316bZns', 'qap-dh-240381mwSx', 'qap-dh-240256Fsfn', 'qap-dh-24069082dD', 'qap-dh-240749mxVT', 'qap-dh-241290lWGh', 'qap-dh-2429804L8x', 'qap-dh-243738wYhV', 'qap-dh-2437505p5u', 'qap-dh-243761sh6Q', 'qap-dh-243778xzJn', 'qap-dh-243787Z5dc', 'qap-dh-244181BLSP', 'qap-dh-244213RbBA', 'qap-dh-244333wZ6Y']


userkey_token={}   #{userkey:token, uk2:tk2.....}

def print_task(arg):
    if printTask : print(arg)
    elif printError : print (arg)
    else: pass

def get_token():
    api='/auth/login'
    payload={'Username':random.choice(user_list),'Password':'Bart'}
    r=requests.post(url+api,data=payload)
    try:
        token=r.json()['Token']
        userkey=r.json()['UserKey']
        userkey_token[userkey]=token
        return (userkey,token)
    except:
        tmp=random.choice(list(userkey_token.keys()))
        return (tmp,userkey_token[tmp])

def generate_json_track():
    json_list=[]
    SessionKey=str(uuid.uuid4())
    ViewKey=str(uuid.uuid4())
    UserKey=str(uuid.uuid4())
    with open ('track_json.csv') as f:
        for line in f:
            if '${SessionKey}' in line:
                line=re.sub(r"\${SessionKey}",SessionKey,line)
            if '${ViewKey}' in line:
                line=re.sub(r"\${ViewKey}",ViewKey,line)
            if '${UserKey}' in line:
                line=re.sub(r"\${UserKey}",UserKey,line)
            if '\"ir\":\"${__UUID}\"' in line:
                line=re.sub(r'\"ir\"\:\"\${__UUID}\"', r'"ir":"str(uuid.uuid4())"',line)
            if '\"ik\":\"${__UUID}\"' in line:
                line=re.sub(r'\"ik\"\:\"\${__UUID}\"', r'"ik":"str(uuid.uuid4())"',line)
            if '\"ar\":\"${__UUID}\"' in line:
                line=re.sub(r'\"ar\"\:\"\${__UUID}\"', r'"ar":"str(uuid.uuid4())"',line)
            if '\"ak\":\"${__UUID}\"' in line:
                line=re.sub(r'\"ak\"\:\"\${__UUID}\"', r'"ak":"str(uuid.uuid4())"',line)
            if '${__UUID}' in line:
                line=re.sub(r'\${__UUID}',str(uuid.uuid4()),line)
            json_list.append(line)
    return (json_list)
# below are modules of user behavior



class track(TaskSet):
    """track/t with gzip compression level"""
    @task
    def analytics(self):
        api='/track/t'
        json_list_user=generate_json_track()
        for json_str in json_list_user:
            new_data=gzip.compress(json_str.rstrip().encode('utf-8'),3) #set compression level here
            payload=new_data
            headers = {'Content-Encoding': 'gzip','Content-Type': 'application/json; charset=UTF-8','Accept-Encoding': 'gzip'}
            r=self.client.post(api,data=payload,headers=headers)
            print_task(r.text)
        self.interrupt()


class user_login(TaskSet):
    # didn't use the get_token function to list api/auth/login on the statistics of locust result page
    @task
    def qap_user_login(self):
        api='/auth/login'
        payload={'Username':random.choice(user_list),'Password':'Bart'}
        with self.client.post(api,data=payload, catch_response=True) as r:
            userkey=r.json()['UserKey']
            userkey_token[userkey]=r.json()['Token']
        self.interrupt()


class product_discovery_home(TaskSet):
    @task
    def search_brand_combined(self):
        api='/search/brand/combined'
        params={'cc': 'CHS', 'sort': 'NameInvariant','order':'asc','pageno':1,'pagesize':50,'s':None}
        self.client.get(api,params=params,name=api)
        print_task(sys._getframe().f_code.co_name)

    @task
    def search_category(self):
        api='/search/category'
        params={'cc': 'CHS', 'sort': 'Priority'}
        self.client.get(api,params=params,name=api)
        print_task(sys._getframe().f_code.co_name)

    @task
    def banner_public_list(self):
        api='/banner/public/list'
        params={'cc': 'CHS', 'bannercollectionid': '2'}
        self.client.get(api,params=params,name=api)
        print_task(sys._getframe().f_code.co_name)
        self.interrupt()

class product_discovery_browseByBrands(TaskSet):
    @task
    def search_style(self):
        api='/search/style'
        params={'cc': 'CHS', 'pageno':1,'pagesize':50, 'merchantid':merchantid, 'notsoldout':'true'}
        with self.client.get(api,params=params,name=api, catch_response=True) as r:
            print_task(api)
            data=r.json()
            randome_style=random.randrange(0,len(data['PageData']))
            get_ReviewStyleCode=data['PageData'][randome_style]['StyleCode']
            get_ReviewStyleId=data['PageData'][randome_style]['StyleId']
        if get_ReviewStyleId and get_ReviewStyleCode:

            api='/review/sku/summary'
            params={'cc': 'CHS','merchantid':merchantid, 'stylecode':get_ReviewStyleCode}
            self.client.get(api,params=params,name=api)
            print_task(api)
            api='/search/style/activity/count/list'
            params={'cc': 'CHS', 'styleids':get_ReviewStyleCode}
            self.client.get(api,params=params,name=api)
            print_task(api)
        self.interrupt()

class cart_wishlist_ShopCart(TaskSet):
    user_key=''
    user_token=''
    @task(3)
    def get_shopping_cart (self):
        api='/banner/public/list'
        params={'cc': 'CHS', 'bannercollectionid': '3'}
        self.client.get(api,params=params,name=api)
        print_task(api)

        api = '/cart/view/user'
        params = {'cc': 'CHS','userkey':self.user_key}
        r = self.client.get(api,params=params,name=api)
        print_task(api)
        # print r.text
        getStyleCode = []
        if (r.json() is not None) and (len(r.json()['ItemList'])>0) :
            for i in (r.json()['ItemList']):
                getStyleCode.append(i['StyleCode'])
        # print getStyleCode
        for stylecode in getStyleCode:
            api = '/search/style'
            params={'cc': 'CHS', 'stylecode': stylecode}
            self.client.get(api,params=params,name=api)
            print_task(api)
        self.interrupt()

    @task(2)
    def add_to_cart_update_quantity(self):
        api='/cart/item/add'
        payload={"CultureCode":"CHS","Qty":random.randint(1,5),"SkuId":"55153","UserKey":self.user_key} # change the SkuId later
        r=self.client.post(api,data=payload)
        print_task(api)
        # print r.text
        CartItemId=r.json()['ItemList'][0]['CartItemId']
        api='/cart/item/update'
        payload={"CartItemId":CartItemId,"CultureCode":"CHS","Qty":random.randint(1,5),"SkuId":'55153',"UserKey":self.user_key}
        self.client.post(api,data=payload)
        print_task(api)

    @task(1)
    def cart_moveto_wishlist(self):
        api = '/cart/view/user'
        params = {'cc': 'CHS','userkey':self.user_key}
        r = self.client.get(api,params=params,name=api)
        print_task(api)
        if (r.json() is not None) and (len(r.json()['ItemList'])>0) :
            CartItemId=r.json()['ItemList'][0]['CartItemId']
            api='/cart/item/move/wishlist'
            payload={"CartItemId":CartItemId,"CultureCode":"CHS","SkuId":"55153",'IsSpecificSku':1,"UserKey":self.user_key} # change the SkuId later
            r=self.client.post(api,data=payload)
            print_task(api)
            WishlistKey = r.json()['WishlistKey']
            api='/wishlist/view'
            params={'cc': 'CHS', 'cartkey': WishlistKey}
            self.client.get(api,params=params,name=api)
            print_task(api)

    def on_start(self):
        if len(userkey_token) < 50:
            self.user_key,self.user_token = get_token()
            print_task('/auth/login')
        else:
            self.user_key = random.choice(list(userkey_token.keys()))
            self.user_token = userkey_token[self.user_key]

class cart_wishlist_WishList(TaskSet):
    user_key=''
    user_token=''
    @task(3)
    def get_wishlist (self):
        api = '/wishlist/view/user'
        params = {'cc': 'CHS','userkey':self.user_key}
        self.client.get(api,params=params,name=api)
        print_task(api)
        # print r.text
        api = '/contentpage/liked/list'
        params = {'cc': 'CHS','pageno':1,'pagesize':50,'UserKey':self.user_key}
        headers = {'Authorization': self.user_token}
        self.client.get(api,params=params,name=api,headers=headers)
        print_task(api)

        api = '/search/post/like'
        params = {'cc': 'CHS','pageno':1,'pagesize':1000,'userkey':self.user_key}
        r=self.client.get(api,params=params,name=api)
        print_task(api)



        self.interrupt()

    # @task(2)
    # def add_to_cart_update_quantity(self):
    #     api='/cart/item/add'
    #     payload={"CultureCode":"CHS","Qty":random.randint(1,5),"SkuId":"55153","UserKey":self.user_key} # change the SkuId later
    #     r=self.client.post(api,data=payload)
    #     print_task(api)
    #     # print r.text
    #     CartItemId=r.json()['ItemList'][0]['CartItemId']
    #     api='/cart/item/update'
    #     payload={"CartItemId":CartItemId,"CultureCode":"CHS","Qty":random.randint(1,5),"SkuId":'55153',"UserKey":self.user_key}
    #     self.client.post(api,data=payload)
    #     print_task(api)


    def on_start(self):
        if len(userkey_token) < 50:
            self.user_key,self.user_token = get_token()
            print_task('/auth/login')
        else:
            self.user_key = random.choice(list(userkey_token.keys()))
            self.user_token = userkey_token[self.user_key]


class dummy_task(TaskSet):
    token=''
    @task
    def dum_task(self):
        print (self.token)
        # print self.blabla[0]
        self.interrupt()

    def on_start(self):
        self.token=random.randint(0,10)

class MyTaskSet(TaskSet):
    # tasks={dummy_task:1}
    # tasks={cart_wishlist_WishList:1}
    tasks={track:1}
    # tasks={user_login:1,product_discovery_home:1, product_discovery_browseByBrands:1,cart_wishlist_ShopCart:1, cart_wishlist_WishList:1}
    # def __init__(self, *args, **kwargs):
    #     super(MyTaskSet, self).__init__(*args, **kwargs)
    #     self.blabla='a'
    #
    # def on_start(self):
    #     # self.blabla=self.login()
    #     self.login()
    #     print self.blabla
    #
    # def login(self):
    #     # global blabla
    #     self.blabla=random.randrange(0,len(user_list))
    #     # print self.blabla
        # print 'login'
        # api='/auth/login'
        # random_usr=random.randrange(0,len(user_list))
        # payload={'Username':user_list[random_usr][0],'Password':user_list[random_usr][1]}
        # r=self.client.post(api,data=payload)
        # print r.status_code
        # token=r.json()['Token']
        # userkey=r.json()['UserKey']
        # print token
        # return (token,userkey)

    # @task
    # def try_nest(self):
    #     print random.choice(user_list)

class MyLocust(HttpLocust):
    task_set = MyTaskSet
    print ('woala')
    host= url
    min_wait = 10
    max_wait = 50
