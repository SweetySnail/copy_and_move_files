import os
import datetime
import json
import shutil
import time

###########################################
###               Function              ###
###########################################
## 시간 입력 함수
def get_time():
    # get_time = input('시간(ex. 2021-05-24): ')
    get_time = '2020-01-01'   ###
    in_time_temp = get_time.split('-')
    year = int(in_time_temp[0])
    month = int(in_time_temp[1])
    day = int(in_time_temp[2])
    return datetime.datetime(year, month, day, 0, 0, 0)

## json 형태 출력 함수
def datetime_handler(self, obj):
    if isinstance(obj, datetime.datetime):
        return "iso-datetime:" + obj.isoformat()
    elif isinstance(obj, datetime.date):
        return obj.strftime("%Y-%m-%d")
    return str(obj)

## 용량 치환 함수(byte -> Kbyte)
def get_mb(byte_temp):
    return (byte_temp // 1024) + 1

## 완전탐색 함수
def read_all_file(path, time, flist):
    file_list = os.listdir(path)
    for fname in file_list:
        fpath = os.path.join(path, fname)
        ctime = os.path.getmtime(fpath)
        timestamp = datetime.datetime.fromtimestamp(ctime)
        if timestamp > time:
            # 디렉토리일 경우 더 탐색
            if os.path.isdir(fpath):
                read_all_file(fpath, time, flist)
			# 파일일 경우 리스트 추가
            elif os.path.isfile(fpath):
                flist.append(
					{
					"Name": fname,
					"Size": get_mb(os.path.getsize(fpath)),
					"Time": timestamp,
					"Path": fpath
					}
				)
    return flist

## 변경 파일 출력 함수
def get_addlist(slist, tlist):
    add_list = []
    for source in slist:
        # 1. 동일한 파일 이름 없음
        is_diff = False
        if source['Name'] not in tlist:
            is_diff = True
        else:
            # 2. 최근 수정 시간 다름 or 3. 파일 사이즈 다름
            target = tlist[source['Name']]
            if  source['Time'] != target['Time'] or source['Size'] != target['Size']:
                is_diff = True
        
        if is_diff:    
            add_list.append(source)
    return add_list

## 디렉토리 생성 함수
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: 이미 존재하는 폴더입니다. - " + directory)

## 변경파일 복사 함수
def copy_all_file(file_list, new_path):
    curtime_str = datetime.datetime.now().strftime('%Y-%m-%d')
    createFolder(curtime_str)
    copydir_str = os.path.join(os.getcwd(), curtime_str)
    for file in file_list:
        copyfile = os.path.join(copydir_str, file['Name'])
        shutil.copy2(file['Path'], copyfile)

## 텍스트 결과물 출력 함수
def make_txt(list, name):
    text_str = os.path.join(os.getcwd(), name + ".txt")
    f = open(text_str, "w")
    f.write(json.dumps(list, indent=4, ensure_ascii=False))
    f.close()

###########################################
###                 Main                ###
###########################################
json.JSONEncoder.default = datetime_handler

## 시간 입력
in_time = get_time()

## 경로 입력
# path_source = input('Source 경로: ')
# path_target = input('Target 경로: ')
path_source = 'C:\\Users\\재현\\Desktop\\NDS\\0006_Python\\testA' ###
path_target = 'C:\\Users\\재현\\Desktop\\NDS\\0006_Python\\testB' ###

print("****  코드 실행 경로: " + os.getcwd())

## Source 파일 목록 추출
print(" .\n .\n .\n==================  Source Start  =====================")
start_time = time.time()
source = []
flist_source = read_all_file(path_source, in_time, source)
make_txt(flist_source, "source")
print("Source 실행시간: {}".format(time.time() - start_time))
print("==================   Source End   ===================== \n.\n.\n.")



## Target 파일 목록 추출
print("==================  Target Start  =====================")
start_time = time.time()
target = []
flist_target_temp = read_all_file(path_target, in_time, target)
flist_target = {}
for target in flist_target_temp:
    flist_target[target['Name']] = {
            "Name": target['Name'],
            "Size": target['Size'],
            "Time": target['Time'],
            "Path": target['Path']
    }
make_txt(flist_target, "target")
print("Target 실행시간: {}".format(time.time() - start_time))
print("==================   Target End   ===================== \n.\n.\n.")



## 추가해야할 파일 목록 추출
print("==================  Extract Add List Start  =====================")
start_time = time.time()
file_list_add = get_addlist(flist_source, flist_target)
make_txt(file_list_add, "add")
print("Extract Add List 실행시간: {}".format(time.time() - start_time))
print("==================   Extract Add List End   ===================== \n.\n.\n.")



## 파일 복사
copy_all_file(file_list_add, os.getcwd())



































# #### 기존 코드
# ## Source 경로 파일 추출
# file_list_source = []

# filelist_source = os.listdir(path_source)
# for fname in filelist_source:
#     fpath = os.path.join(path_source, fname)
#     ctime = os.path.getmtime(fpath)
#     timestamp = datetime.datetime.fromtimestamp(ctime)
#     if timestamp > in_time:
#         fsize = get_mb(os.path.getsize(fpath))
#         ftime = timestamp
#         fis_Dict = os.path.isdir(fpath)

#         file_list_source.append(
#             {
#             "Name": fname,
#             "Size": fsize,
#             "Time": ftime,
#             "Path": fpath,
#             "is_Dict": fis_Dict
#             }
#         )





# print("Source 실행시간: {}".format(time.time() - start_time))
# print("==================   Source End   ===================== \n.\n.\n.")

# print("==================  Target Start  =====================")
# start_time = time.time()
# ## Target 경로 파일 추출
# file_list_target = {}

# filelist_target = os.listdir(path_target)
# for fname in filelist_target:
#     fpath = os.path.join(path_source, fname)
#     ctime = os.path.getmtime(fpath)
#     timestamp = datetime.datetime.fromtimestamp(ctime)
#     if timestamp > in_time:
#         fsize = get_mb(os.path.getsize(fpath))
#         ftime = timestamp
#         fis_Dict = os.path.isdir(fpath)
        
#         file_list_target[fname] = {
#             "Name": fname,
#             "Size": fsize,
#             "Time": ftime,
#             "Path": fpath,
#             "is_Dict": fis_Dict
#         }
# print("Target 실행시간: {}".format(time.time() - start_time))
# print("==================   Target End   ===================== \n.\n.\n.")

# ## 추가해야할 파일 목록
# file_list_add = []
# for source in file_list_source:
#     # 1. 동일한 파일 이름 없음
#     is_diff = False
#     if source['Name'] not in file_list_target:
#         is_diff = True
#     else:
#         # 2. 최근 수정 시간 다름 or 3. 파일 사이즈 다름
#         target = file_list_target[source['Name']]
#         if  source['Time'] != target['Time'] or source['Size'] != target['Size']:
#             is_diff = True
    
#     if is_diff:    
#         file_list_add.append(source)

# ## 변경된 파일 복사(디렉토리일 경우 에러발생)
# print("현재경로 - " + os.getcwd()) ###
# curtime_str = datetime.datetime.now().strftime('%Y-%m-%d')
# createFolder(curtime_str)
# copydir_str = os.path.join(os.getcwd(), curtime_str)
# for file in file_list_add:
#     ## 파일 복사
#     if file['is_Dict'] == False:
#         copyfile = os.path.join(copydir_str, file['Name'])
#         shutil.copy2(file['Path'], copyfile)
#     ## 폴더 복사
#     # else:
#     #     # createFolder()
#     #     copyfile = os.path.join(copydir_str, file['Name'])
#     #     shutil.copy2(file['Path'], copyfile)

# # shutil.copy2()

# ## 텍스트 파일 출력
# text_str = os.path.join(os.getcwd(), curtime_str + ".txt")
# f = open(text_str, "w")
# f.write(json.dumps(file_list_add, indent=4, ensure_ascii=False))
# f.close()
