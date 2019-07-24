#정의부분
import jellyfish
import os
import konlpy
import hgtk
import glob
stopwords = ["수입업소","교환처","반품","공정거래위원회","식품위생법","소비자","제조업소명","제품명","식품의유형","식품유형","유통기한","내용량","용기","재질","용기재질","포장재질","반품","보관방법","영양정보","총","총 내용량","내용량","보관방법","이미지","부정","불량식품","불량","1399","표시일","표시일까지","년","뚜껑","서늘한","구입처",'www',"고객상담실","고객","상담실","kcal","제조사","유형","플라스틱","폴리에틸렌","폴리","후면","이마트","서울시","소비자","직사광선","품목","품목보고번호","번호","보고","멸균","앞면","뒷면","충격","마십시오","포장","폴리프로필렌"]
cautionwords = ["본","본 제품은","본제품은","본제품","제품","공장에서","공장","있습니다","알러지","알레르기","유발","유발물질","이 제품은","이제품은","이제품","제조시설","제조","같은제조시설","같은제조","설사"]
#원재료명 써져있는 이미지 있는 파일에서 돌림
def get_jamo():
	userdic = open('user_dic.txt','r')
	result = {}
	while True:
		line = userdic.readline()
		if len(line) is 0:
			break
		line = line.split('	')[0]
		result[line] = hgtk.text.decompose(line)
	return result

def find_most_similar(word_list,jamo_dict):
	val = 0
	food = ' '
	comp = hgtk.text.decompose(word_list)
	for idx,jamo in jamo_dict.items():
		comp_score = jellyfish.jaro_distance(comp,jamo)
		if comp_score > val:
			val = comp_score
			food = idx
	
	if val < 0.9:
		food = ' '	
	return food

		
def start():
	jamo_dict = get_jamo()
	komo = konlpy.tag.Komoran(userdic='user_dic.txt')
	#kkma = konlpy.tag.Kkma()
	#komo = konlpy.tag.Komoran(userdic='user_dic.txt')
	#tw = konlpy.tag.Okt()

	for file in glob.glob("txt_from_img/*.txt"):
		f = open(file,'r')
		while True:
			oneLine = f.readline()
			if len(oneLine) is 0 or oneLine == '\n' or oneLine == None:
				break
			#kkma = konlpy.tag.Kkma()
			#komo = konlpy.tag.Komoran(userdic='user_dic.txt')
			#tw = konlpy.tag.Okt()

			#---------------------------------
			oneLine = oneLine.replace('\n','')
			print(oneLine)
			splited_word= komo.nouns(oneLine)
	
			#kkma.nouns(oneLine)
			#komo.nouns(oneLine)
			#tw.nouns(oneLine)
			#kkma.morphs(oneLine)
			#komo.morphs(oneLine)
			#tw.morphs(oneLine)
			#oneLine.replace(',',' ')
			#splited_word = splited_word.split()
			# 여기서 띄어쓰기로 split할지 kkma나 komoran 쓸건지 고민
			filename = str(file).split('/')[1]
			stop_f = open('stopword_file/'+filename,'a')
			cau_f = open('caution_file/'+filename,'a')
			for word_list in splited_word:
				if word_list in stopwords:
					#open_writing_file('stopword_file/'+filename)
					#stop_f = open('stopword_file'+filename,'a')
					stop_f.write(oneLine+'\n')
					#stop_f.close()
					break
				#스톱 워드중에서 공장 표시를 얘기하는 것들은 따로 저장해야할 것 같다.
				if word_list in cautionwords:
					#open_writing_file('caution_file/'+filename)
					#cau_f = open('caution_file/'+filename,'a')
					cau_f.write(oneLine+'\n')
					#cau_f.close()
					break
			else:
				#open_writing_file('processed_file/'+filename)
				data_file = open('processed_file/'+filename,'a')
				non_counter = 0 # 연속적으로 식쟤료 아닌 것 같으면 그 문장 건너뜀
				for word_list in splited_word:
					food = find_most_similar(word_list,jamo_dict)
					
					#if food is ' ' and non_counter < 3:
					#	non_counter = non_counter+1
					#elif food is ' ' and non_counter == 3:
					#	break
					#else:
					#	non_counter = 0
					if food is not ' ':
						data_file.write(food+' ')
						print(food)
				data_file.close()
			cau_f.close()
			stop_f.close()
		f.close()

def makefolder(folder_name):
	if os.path.exists(folder_name) is False:
		os.mkdir(folder_name)

makefolder('stopword_file')
makefolder('caution_file')
makefolder('processed_file')
if os.path.isfile('user_dic.txt') is True:
	start()
else:
	print('user_dic.txt does not exists')



