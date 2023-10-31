import os
#replace api with another


def convert_api(str):
    # "IE_THROW()<<" is replaced by "OPENVINO_THROW("
    # "<<" is replaced by ","
    old_str =["IE_THROW() << " , " << ", ";", "IE_THROW() <<",  " <<" ]
    new_str =["OPENVINO_THROW(", ", "  , ");", "OPENVINO_THROW("," ,"]
    for i in range(len(old_str)):
        if old_str[i] in str:
            str = str.replace(old_str[i], new_str[i])
    return str

def test_convert_api():
    test_str_1='        IE_THROW() << \"Cannot get input memory descriptor for edge: \" << getParent()->getName() << \"->\"'
    test_str_2='                   << getChild()->getName();'

    test_str_1 = convert_api(test_str_1)
    test_str_2 = convert_api(test_str_2)
    print(test_str_1)
    print(test_str_2)


def handle_one_file(file_name):
    f = open(file_name,"r")
    new_name = file_name + ".new"
    new_f = open(new_name,"w+")

    line = f.readline()
    flag = 0
    need_update=False
    start_str="IE_THROW()"
    while line:
        str = line
        if flag == 1:
            str = convert_api(line)
            need_update = True
            if ";" in line:
                flag = 0
        if flag == 0:
            if start_str in line:
                str = convert_api(line)
                need_update = True
                if ";" not in line:
                    flag = 1
        new_f.write(str)
        line = f.readline()
    new_f.close()
    f.close()
    if need_update:
        os.remove(file_name)
        os.rename(new_name, file_name)
    else:
        os.remove(new_name)

def process_dir(dir):
    file_list=[]

    for item in os.listdir(dir):
        if item.endswith(".cpp"):
            file_list.append(item)

    for f in file_list:
        print(f)
        handle_one_file(f)


def list_all_files(dir):
    file_list=[]

    for folder_name, sub_folder_name, file_names in os.walk(dir):
        for file_name in file_names:
            file_list.append(folder_name + "/" + file_name)
    
    #for i in file_list:
    #    print(os.path.getsize(i), i)

    return file_list

dir="/mnt/data1_1c41/river/openvino/src/plugins/intel_cpu/src"
file_list = list_all_files(dir)

for file in file_list:
    handle_one_file(file)
    print(file)

#handle_one_file("/mnt/data1_1c41/river/utils/batch_to_space.cpp")
