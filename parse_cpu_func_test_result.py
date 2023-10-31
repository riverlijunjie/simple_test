import os

data_dir='./test_result_dir'
dst_file='./failed_list.txt'

dir_list = os.listdir(data_dir)
result=[]
file_num=0
item_num=0
for file in dir_list:
    if '_failed' in file:
        file_name=data_dir + '/' + file
        file_num +=1
        #print(file_name)
        with open(file_name,'r') as src:
            lines = src.readlines()
            for line in lines:
                if "[  FAILED  ]" in line:
                    #line=line.replace("[  FAILED  ]","").split(',')[0].split("=")[0]
                    line=line.replace("[  FAILED  ]","").replace(" ","").split('.')[0]
                    if ":" in  line:
                        continue
                    if len(line)<2:
                        continue
                    result.append(line)
                    item_num +=1

# remove duplicated item
result = list(set(result))

with open(dst_file,'w') as dst:
    for line in result:
        dst.write(line+'\n')

print("suite_num = ", file_num)
print("item_num = ", item_num)
