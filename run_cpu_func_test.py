import os
import subprocess
import threading

test_list_file_name='./tests_list.txt'
test_app='./ov_cpu_func_tests'
dst_dir='./test_result_dir'
parallel_num = 64

#generate test list
generate_test_list_cmd=[test_app,'--gtest_list_tests']
orig_res = subprocess.run(generate_test_list_cmd, capture_output=True, text=True)
orig_res = orig_res.stdout.split('\n')

# save test list
with open(test_list_file_name,'w') as dst:
    for l in orig_res:
        if len(l)>0 and l[0] != ' ':
            dst.write(l + '\n')

# read test suite list
with open(test_list_file_name, 'r') as src:
    test_list=src.readlines()

def run_one_tests(cmd, name):
    res = subprocess.run(cmd, capture_output=True, text=True)
    logs = res.stdout.split('\n')
    failed = False
    aborted = False
    for log in logs:
        if 'FAILED' in log:
            failed = True
        if 'Abort' in log:
            aborted = True
    if failed:
        name += '_failed'
    if aborted:
        name += '_aborted'
    
    with open(name,'w') as dst:
        for log in logs:
            dst.write(log+'\n')

total=len(test_list)
for item in range(0,total+1,parallel_num):
    thds=[]
    for i in range(parallel_num):
        idx = item + i
        test_name = test_list[idx].split('\n')[0]
        cmd = [test_app, '--gtest_filter=' + test_name + '*']
        print(idx, " : ", cmd)
        print(test_name)
        test_name=test_name.replace('/','')
        print(test_name)
        thd = threading.Thread(target=run_one_tests, args=(cmd,dst_dir+'/'+test_name))
        thd.start()
        thds.append(thd)
    
    for i in range(parallel_num):
        thds[i].join()
