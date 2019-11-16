def sim_msd(data, name1, name2):  #유저간의 유사도 측정
    sum = 0
    count = 0
    for movies in data[name1]:
        if movies in data[name2]: #같은 영화를 봤다면
            sum += pow(data[name1][movies]- data[name2][movies], 2)
            count += 1

    return 1 / ( 1 + (sum / count) )


def top_match(data, name, index=3, sim_function=sim_msd):
    li=[]
    for i in data: #딕셔너리를 돌고
        if name!=i: #자기 자신이 아닐때만
            li.append((sim_function(data,name,i),i)) #sim_function()을 통해 상관계수를 구하고 li[]에 추가
    li.sort() #오름차순
    li.reverse() #내림차순
    return li[:index]

def getRecommendation (data, person, k=3, sim_function=sim_msd):
    
    result = top_match(data, person, k)
    
    score = 0 # 평점 합을 위한 변수
    li = list() # 리턴을 위한 리스트
    score_dic = dict() # 유사도 총합을 위한 dic
    sim_dic = dict() # 평점 총합을 위한 dic

    for sim, name in result: # 튜플이므로 한번에
        print(sim, name)
        if sim < 0 : continue #유사도가 양수인 사람만
        for movie in data[name]: 
            if movie not in data[person]: #name이 평가를 내리지 않은 영화
                score += sim * data[name][movie] # 그사람의 영화평점 * 유사도
                score_dic.setdefault(movie, 0) # 기본값 설정
                score_dic[movie] += score # 합계 구함

                # 조건에 맞는 사람의 유사도의 누적합을 구한다
                sim_dic.setdefault(movie, 0) 
                sim_dic[movie] += sim

            score = 0  #영화가 바뀌었으니 초기화한다
    
    for key in score_dic: 
        score_dic[key] = score_dic[key] / sim_dic[key] # 평점 총합/ 유사도 총합
        li.append((score_dic[key],key)) # list((tuple))의 리턴을 위해서.
    li.sort() #오름차순
    li.reverse() #내림차순
    return li


data = {
    '한지수': {
        '팔도비빔면': 3.5,
        '닭안심샐러드': 1.5,
        '아보카도': 3.0,
        '카프레제': 3.5,
        '하늘보리': 2.5,
        '현미잡곡': 3.0,
    },
    '고동섭': {
        '팔도비빔면': 5.0,
        '닭안심샐러드': 4.5,
        '아보카도': 0.5,
        '카프레제': 1.5,
        '하늘보리': 4.5,
        '현미잡곡': 5.0,
    },
    '박태준': {
        '팔도비빔면': 3.0,
        '닭안심샐러드': 2.5,
        '아보카도': 1.5,
        '카프레제': 3.0,
        '현미잡곡': 3.0,
        '하늘보리': 3.5,
    },
    '아이린': {
        '팔도비빔면': 2.5,
        '닭안심샐러드': 3.0,
        '카프레제': 4.5,
        '현미잡곡': 4.0,
    },
    '조인성': {
        '닭안심샐러드': 4.5,
        '아보카도': 3.0,
        '현미잡곡': 4.5,
        '카프레제': 3.0,
        '하늘보리': 2.5,
    },
    '최재원': {
        '팔도비빔면': 3.0,
        '닭안심샐러드': 4.0,
        '아보카도': 1.0,
        '카프레제': 3.0,
        '현미잡곡': 3.5,
        '하늘보리': 2.0,
    },
    '이동현': {
        '팔도비빔면': 3.0,
        '닭안심샐러드': 4.0,
        '현미잡곡': 3.0,
        '카프레제': 5.0,
        '하늘보리': 3.5,
    },
    '김태현': {
        '닭안심샐러드': 4.5, 
        '하늘보리': 1.0,
        '카프레제': 4.0
    }
}





print(getRecommendation(data, '조인성', 3, sim_msd ))