import math
filename = 'users'
original_file='users.csv'
file_count = 20
user_list=[]

with open(original_file) as f:
    user_list=f.readlines()

how_many_users_per_csv = int(math.floor(len(user_list)/file_count))

for i in range(1,file_count+1):
    with open(filename+str(i)+'.csv','w') as fhand:
        fhand.write('Username,Password,UserKey\n')
        for user in user_list[how_many_users_per_csv*(i-1)+2 : how_many_users_per_csv*i+2]:
            fhand.write(user)
