import knlp
import kss
import hgtk
import jellyfish

#뒤의 파라미터는 그대로 넣어주고, "abc" 지역은 넣어야 할 STring을 의미

def main():
    jamo_dict = get_jamo()
    model,komo,selected_words = knlp.get_model()
    #구현사항
    #1. DB에서 ID와 Raw text를 가져온다.
    #2. kss를 import해서 가져온 Raw Text를 kss로 나눈다.
    #3. 각 문장마다 predict_pos_neg를 실행
    #4. predict_pos_neg가 True일 경우, 해당 Sentence에서 원재료를 뽑는다.
    #5. 해당 Raw Text에 매칭되는 ID의 최종 결과 column에 원재료 리스트들을 삽입한다.


    #6. 모든 사항을 완료했을 경우, 대략적인 정확도를 판단한다.
    #7. 정확도가 낮을 경우, knlp를 수정. selected_words에 punc와 조사가 들어오는 경우를 제거한다.

    # 원재료를 뽑는 방법은 food_extract.py를 참고. 그대로 실행하면 안됌.
    for sentence in kss.split_sentences(text):
        print(sentence)
        if knlp.predict_pos_neg(sentence, model, komo, selected_words):
            if len(sentence) == 0 or sentence == '\n' or sentence == ' ':
                continue
            sentence = sentence.replace('\n','')
            splited_data = spliting(sentence,replacewords)
            result = []
            for word in splited_data:
                food = find_most_similar(word, jamo_dict, 1.0)
                if food is not ' ':
                    result.append(food)
                
                splited_word= komo.nouns(word)
                for word in splited_word:
                    food = find_most_similar(word, jamo_dict, 1.0)
                    if food not in result and food is not ' ':
                        result.append(food)

            print(result)

        else:
            continue

    

def spliting(one_string,rewords):
	one_string = percentage_deletion(one_string)
	for word in rewords:
		one_string = one_string.replace(word,' ')
	
	one_string = one_string.split()
	return one_string

def get_jamo():
    userdic = open('user_dic.txt', 'r')
    result = {}
    while True:
        line = userdic.readline()
        if len(line) is 0:
            break
        line = line.split(' ')[0]
        result[line] = hgtk.text.decompose(line)
    return result


def find_most_similar(word_list,jamo_dict,weight):
	val = 0
	food = ' '
	comp = hgtk.text.decompose(word_list)
	for idx,jamo in jamo_dict.items():
		comp_score = jellyfish.jaro_distance(comp,jamo)
		if comp_score > val:
			val = comp_score
			food = idx
	if val < weight:
		food = ' '
	return food
#find_most_similar : jaro distance를 이용해서 들어온 단어와 유저 딕셔너리에 있는 단어 중 가장 유사한것을 출력.
#word_list : 비교하려는 단어
#damo_dict : user_dic.txt.의 원재료들의 자모 나눔 딕셔너리 jamo_dict['자두'] = 'ㅈㅏㄷㅜ'
#weight : 가중치. 얼마나 유사해야 출력하는지를 정함
def percentage_deletion(string):
	ch = 0
	while ch < len(string):
		if string[ch]<= '9' and string[ch] >= '0':
			if len(string) > ch+1 and string[ch+1] is '%':
				word = string[ch:ch+1]
				string = string.replace(word,' ')
				break
			if len(string) > ch+2 and string[ch+2] is '%':
				word = string[ch:ch+2]
				string = string.replace(word,' ')
				break
		ch = ch+1
	return string

if __name__ == "__main__":
    replacewords = ['.',',',':',';','[',']','{','}','(',')','/','중국산','호주산','미국산','국내산','스페인산','우크라이나산','뉴질랜드산','독일산','일본산','러시아산','터키산','가용성고형분','이탈리아산']
    text = """제 품 명 | 가쓰오곤약우동 | 식품의유형 |즉석조리식품
        유통 기한 | 별도표기일까지| 보관 방법 |실온(1~350)보관 | 반품 및교환 |고객센터 및 구입체
        판 매 원 | 주)푸드나무/ 서울시 마포구 월드컵북로 396, 15층 (상암동, 누리꿈스퀘어비즈니스타워)
        제 조 원 | ㈜)성보/충북진천군 덕산면 초금로 632-11
        포장 재질 | 컵용기· 건더기후레이크 : 폴리에틸렌(내면) 곤약우동면 : 폴리프로필렌(내면,
        내용 량 | 200g
        품목보고번호 20130443168878
        뚜껑 : 폴리프로필렌(PP)
        *부정불량식품 신고는국번없이 1399
        *본제품은공정거래위원회 고시소비자분쟁해결기준에 의거 교환또는 보상받으실 수있습니다.
        총 내용량 200g 40kal
        당류 5g 5%
        포화지방 Og 0%
        영양 정보
        탄수화물 7g 2%
        트랜스지방 Og
        단백질 2g 49%
        1일 영양성분 기준치에 대한 비율%)은 2000kcal 기준 이므로
        에 따라 다를 수 있습니다.
        나트륨 1200mg 60%
        지방 Og 0%
        콜레스테롤
        개인의 필요 열량
        원재료명 및 함량
        가쓰오곤약우동면 199g(즉석조리식품/레토르트제
        품) 우동모양곤약65%[곤약분 998%(중국산)수산
        화칼슘]정제수,진간장[탈지대두(인도산)천일염(호
        주산)양조간장기타과당효소처리스테비아파라옥
        시안식향산에틸(보존료)]기타과당정제소금(국산),
        다랑어엑기스08%가쓰오추출물615%(훈연맛다랑어분말12%(인도네시아산),다랑어엑기스S3.5%
        {다랑어추출베이스65%<훈연맛다랑어분말129%인도네시아산)>}]핀크스우동쓰유-W06%다랑어
        엑기스79%가쓰오추출물615%<훈연맛다랑어분말129%(인도네시아산)>>다랑어엑기스S3.5%<대랑
        어추출베이스65%(훈연맛다랑어분말12 인도네시아산)>},우동분말5%우동분말베이스38.049%6<
        다랑어추출베이스52%훈연맛다랑어분말20%)>다랑어엑기스S<다랑어추출베이스65%(훈연맛다
        랑어분말129%)>}참치액35%가다랑어추출액508%고형분119%)M설탕미림L-글루탐산나트륨[향미
        증진제1참치액05%가다랑어추출액50.8%고형분11%)]포도당,양조간장조미페이스트#SW-07합
        성향료[가쯔오부시향] 건더기후레이크1g(기타가공품) 건파파100%(중국산)구운김후레이크[김1
        00%국산)]계란지단[전란분(덴마크산),밀가루(밀미국산호주산),D-소비톨액난백분정제소금]
        우유대두, 밀쇠고기난류함유
        안전관리인증
        HACCP
        식품의약품안진처,
        조리예
        제 품 명 | 비빔곤약우동 | 식품의유형 |즉석조리식품
        유통 기한 | 별도표기일까지| 보관 방법 |실온(1~350)보관 | 반품 및교환 |고객센터 및 구입처
        판 매 원 | ㈜)푸드나무/ 서울시 마포구 월드컵북로 396, 15층 (상암동, 누리꿈스퀘어 비즈니스타워)
        제 조 원 | 주)성보/충북 진천군 덕산면 초금로 632-11
        포장 재질 | 컵용기 건더기후레이크 : 폴리에틸렌(내면), 곤약우동면: 폴리프로필렌(내면)
        량 | 200g
        내용
        |품목보고번호 | 20130443168878
        뚜껑 : 폴리프로필렌(P)
        *부정불량식품신고는국번없이 1399
        *본제품은공정거래위원회 고시 소비자분쟁해결기준에 의거 교환또는 보상받으실 수있습니다.
        영양 정보
        총내용량 200g 165kcal
        나트륨 890mg 45%
        당류 21g 21%
        포화지방 Og 0%
        탄수화물 36g 11%
        지방 12g 2%
        콜레스테롤.
        1일 영양성분 기준치에 대한 비율%)은 2,000kcal 기준 이므로
        개인의 필요 열량에 따라다를수 있습니다.
        트랜스지방 Og
        단백질 2g 4%
        원재료명 및 함량
        비빔곤약우동면 199g(즉석조리식품/레토르트제품
        )우동모양곤약65%(곤약분998%(중국산), 수산화
        칼슘]고추장[물엿소맥분(밀: 미국산호주산)고추양
        념(중국산)고추양념분말정제소금]설탕정제수사
        과식초농축사과과즙(중국산)]맥아물엿조미페이
        스트M-21|1-글루탐산나트륨(향미증진제)1사과농축액 1496배과즙농축액07%고춧가루다진마늘
        혼합제제[히드록시프로필인산이전분말토덱스트린참기름,양조간장파프리카추출색소 건더기후
        레이크 1g기타가공품)건파파100%(중국산]구운김후레이크[김100%(국산)]계란지단[전란분(덴마
        크산)밀가루(말미국산호주산)D-소비톨액난백분정제소금]
        우유 대두, 밀 쇠고기,난류 함유
        안전관리인증
        HACCP
        식품의약품안전처
        ,
        조리예"""
    main()
