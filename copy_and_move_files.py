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

        temp = source['Path'].split(path_source)
        if temp[1] not in tlist:
            is_diff = True
        else:
            # 2. 최근 수정 시간 다름 or 3. 파일 사이즈 다름
            # target = tlist[source['Name']]
            target = tlist[temp[1]]
            if  source['Time'] != target['Time'] or source['Size'] != target['Size']:
                is_diff = True
        
        if is_diff:    
            add_list.append(source)
    return add_list

## 디렉토리 생성 함수
def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: 이미 존재하는 폴더입니다. - " + directory)

## 변경파일 복사 함수
def copy_all_file(file_list, path_source):
    curtime_str = datetime.datetime.now().strftime('%Y-%m-%d')
    createDirectory(curtime_str)
    
    ## 파일 복사 진행
    for file in file_list:
        copydir_str = os.path.join(os.getcwd(), curtime_str)  # 2021-06-02
        strr = file['Path'].split(path_source)
        copy_path = copydir_str + strr[1]
        strr2 = strr[1].split('\\')
        
        for i, v in enumerate(strr2):
            if i == 0: # 첫 공백 제거
                continue
            elif i == len(strr2)-1: # 마지막 경로(파일)
                copy_file = os.path.join(file['Path'], copy_path)
                if os.path.isfile(copy_file):  # 이미 있는 파일이면
                    temp = time.strftime('%H-%M-%S')
                    copy_file = copy_file + "_" + temp
                    shutil.copy2(file['Path'],copy_file)
                else:  # 없는 파일이면
                    shutil.copy2(file['Path'],copy_file)
                
            else: # 중간 경로(디렉토리)
                curr_path = os.path.join(copydir_str, v)
                createDirectory(curr_path)
                copydir_str = curr_path

## 텍스트 결과물 출력 함수
def make_txt(list, name):
    text_str = os.path.join(os.getcwd(), name + ".txt")
    f = open(text_str, "w")
    f.write("Total: " + str(len(list)) + "\n")
    f.write(json.dumps(list, indent=4, ensure_ascii=False))
    f.close()




###########################################
###                 Main                ###
###########################################
## 전체결과 파일 생성
text_str = os.path.join(os.getcwd(), "Result.txt")
f_result = open(text_str, "w")
f_result.write("** 코드 시작 ** \n")

json.JSONEncoder.default = datetime_handler

## 시간 입력
in_time = get_time()

## 경로 입력
# path_source = input('Source 경로: ')
# path_target = input('Target 경로: ')
path_source = 'C:\\Users\\재현\\Desktop\\NDS\\0006_Python\\testA' ###
path_target = 'C:\\Users\\재현\\Desktop\\NDS\\0006_Python\\testB' ###

f_result.write("** 코드 실행경로: " + os.getcwd())

## Source 파일 목록 추출
print(" .\n .\n .\n==================  Source Start  =====================")
start_time = time.time()
source = []
flist_source = read_all_file(path_source, in_time, source)
make_txt(flist_source, "Source_Filelist")
f_result.write("\n\n** Source 파일 리스트 생성 소요시간: {}초".format(round(time.time() - start_time),4))
f_result.write("\n** Source 파일 갯수 : " + str(len(flist_source)) + "개")
f_result.write("\n** Source 파일 결과물 : Source_Filelist")
print("Source 실행시간: {}초".format(round(time.time() - start_time),4))
print("==================   Source End   ===================== \n.\n.\n.")



## Target 파일 목록 추출
print("==================  Target Start  =====================")
start_time = time.time()
target = []
flist_target_temp = read_all_file(path_target, in_time, target)

flist_target = {}
for targets in flist_target_temp:
    temp = targets['Path'].split(path_target)
    flist_target[temp[1]] = {
            "Name": targets['Name'],
            "Size": targets['Size'],
            "Time": targets['Time'],
            "Path": targets['Path']
    }
make_txt(flist_target, "Target_Filelist")
f_result.write("\n\n** Target 파일 리스트 생성 소요시간: {}초".format(round(time.time() - start_time),4))
f_result.write("\n** Target 파일 갯수 : " + str(len(flist_target_temp)) + "개")
f_result.write("\n** Target 파일 결과물 : Target_Filelist")
print("Target 실행시간: {}초".format(round(time.time() - start_time),4))
print("==================   Target End   ===================== \n.\n.\n.")



## 추가해야할 파일 목록 추출
print("==================  Extract Add List Start  =====================")
start_time = time.time()
file_list_add = get_addlist(flist_source, flist_target)
make_txt(file_list_add, "Add_Filelist")
f_result.write("\n\n** 복사할 파일 리스트 생성 소요시간: {}초".format(round(time.time() - start_time),4))
f_result.write("\n** 복사할 파일 갯수 : " + str(len(file_list_add)) + "개")
f_result.write("\n** 복사할 파일 결과물 : Add_Filelist")
print("Extract Add List 실행시간: {}초".format(round(time.time() - start_time),4))
print("==================   Extract Add List End   ===================== \n.\n.\n.")



## 파일 복사
print("==================  Copy File Start  =====================")
start_time = time.time()
copy_all_file(file_list_add, path_source)
f_result.write("\n\n** 파일 복사 소요시간: {}초".format(round(time.time() - start_time),4))
print("Copy File 실행시간: {}초".format(round(time.time() - start_time),4))
print("==================   Copy File End   ===================== \n.\n.\n.")




f_result.write("\n** 작업이 완료되었습니다.")
f_result.close()