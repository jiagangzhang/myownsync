from locust import HttpLocust, TaskSet, task
import sys,random

token=''
userkey=''
merchantid = 1
printTask = True
printError = True

def print_task(arg):
    if printTask : print(arg)
    elif printError : print (arg)
    else: pass

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
            print_task(sys._getframe().f_code.co_name)
            data=r.json()
            randome_style=random.randrange(0,len(data['PageData']))
            get_ReviewStyleCode=data['PageData'][randome_style]['StyleCode']
            get_ReviewStyleId=data['PageData'][randome_style]['StyleId']
        if get_ReviewStyleId and get_ReviewStyleCode:

            api='/review/sku/summary'
            params={'cc': 'CHS','merchantid':merchantid, 'stylecode':get_ReviewStyleCode}
            self.client.get(api,params=params,name=api)

            api='/search/style/activity/count/list'
            params={'cc': 'CHS', 'styleids':get_ReviewStyleCode}
            self.client.get(api,params=params,name=api)
        self.interrupt()


class MyTaskSet(TaskSet):
    tasks={product_discovery_home:1, product_discovery_browseByBrands:1}

    def on_start(self):
        self.login()

    def login(self):
        print 'login'

    # @task
    # def try_nest(self):
    #     print 'this is my task set'

class MyLocust(HttpLocust):
    task_set = MyTaskSet
    print 'woala'
    host= 'http://test-mm.eastasia.cloudapp.azure.com/api'
    min_wait = 500
    max_wait = 500
