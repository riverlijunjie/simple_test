#
# pip install xlwt openpyxl

import subprocess
import time
import re

import xlwt
from xlwt import Workbook

bin_dir='/mnt/data1_1c41/river/openvino/bin/intel64/Release/'
model_dir='/mnt/data1_1c41/river/models/'
cache_dir=bin_dir+'cache_dir_test/'
iteration = 11
run_time=60 # ms
sleep_time = 10 #ms
#blob_names=['benchmark_import_latency_14MB.blob', 'benchmark_import_latency_4GB.blob']
#blob_names=['benchmark_import_latency_4GB.blob']
blob_names=['lm_1b.xml']

output=[]
for name in blob_names:
    model_path=model_dir+name
    print('run ' + model_path + ':')
    subprocess.run(['rm', '-rf', cache_dir+'*.blob'])
    blob_out=[]
    for it in range(iteration):
        print("iteration : %d/%d"%(it+1,iteration))
        #cmd = [bin_dir+'benchmark_app','-m',bin_dir+blob_name,'-d','CPU','-t',str(run_time), '-hint', 'none', '-nstreams', '18','-nthreads', '18']
        cmd = [bin_dir+'benchmark_app','-m',model_path,'-d','CPU','-t',str(run_time), '-hint', 'tput', '-cache_dir', cache_dir]
        print("    ",cmd)
        result = subprocess.run(cmd, capture_output=True, text=True)
        #result = subprocess.run(cmd, stdout=PIPE, stderr=PIPE)
        logs = result.stdout.split('\n')
        out={}
        for log in logs:
            print(log)
            if 'Compile model took' in log:
                data = re.findall(r"\d+\.?\d*",log)[0]
                out['compile_time'] = data
                print(log)
            if 'First inference took' in log:
                data = re.findall(r"\d+\.?\d*",log)[0]
                out['first_inference_latency'] = data
                print(log)
            if 'Throughput' in log:
                data = re.findall(r"\d+\.?\d*",log)[0]
                out['fps'] = data
                print(log)
            if 'CNNNetworkDeserializer::parse' in log:
                data = log.split(" ")[0]
                out['parse_type'] = data
                print(log)
        blob_out.append(out)
        time.sleep(sleep_time)
        print()
    #
    output.append(blob_out)
    print()

# save to excel file
print(output)
#creat workbook
wb = Workbook()

cout = 0
for page in output:
    cout += 1
    name = 'blob_' + str(cout)
    sheet = wb.add_sheet(name)
    sheet.write(0, 1, 'Compile time')
    sheet.write(0, 2, 'FIL')
    sheet.write(0, 3, 'FPS')
    num = 0

    compile_time_tot = 0
    fil_tot = 0
    fps_tot = 0
    for item in page:
        print('item=',item)
        compile_time_tot += float(item['compile_time'])
        fil_tot += float(item['first_inference_latency'])
        fps_tot += float(item['fps'])
        sheet.write(num + 1, 0, num+1)
        sheet.write(num + 1, 1, float(item['compile_time']))
        sheet.write(num + 1, 2, float(item['first_inference_latency']))
        sheet.write(num + 1, 3, float(item['fps']))
        num += 1
        print('num:',num, item['compile_time'],item['first_inference_latency'],item['fps'])
    sheet.write(num + 1, 0, num+1)
    sheet.write(num + 1, 1, compile_time_tot/num)
    sheet.write(num + 1, 2, fil_tot/num)
    sheet.write(num + 1, 3, fps_tot/num)
    print('average: compile_time=%.2f ms, fil = %.2f ms, fps = %.2f'%(compile_time_tot/num, fil_tot/num, fps_tot/num))
wb.save('result.xls')

