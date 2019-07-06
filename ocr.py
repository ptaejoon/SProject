import io
import os
import sys
import re
import shutil
from google.cloud import vision

def main():

    cnt = 1

    for file in os.listdir("./img"):

        texts = detect_text("./img/{}".format(file))
        text_lst = split_word(texts)
        if text_lst:
            filtered = filter_words(text_lst)
        else:
            continue

        if image_classification(filtered):
            os.rename("./img/{}".format(file), "./img2/{}".format(file))
            print("{} / count : {}".format(file, cnt))
            cnt += 1
            
def detect_text(path):

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    return texts

def split_word(texts):

    # multi delim으로 text to list
    try:
        word_lst = re.split(split_delimeters, texts[0].description)
    except IndexError:
        print("Check texts : {}".format(texts))
        return None

    return word_lst

def filter_words(word_lst):

    #단어 리스트 중 필요없는 것들 제거
    word_lst = [ word for word in word_lst if word not in remove_char ]

    # 한 단어에서 필요없는 문자 제거
    for index, word in enumerate(word_lst):
        if any(x in word for x in remove_char):
            word_lst[index] = re.sub(remove_pattern, "", word)

    return word_lst

def image_classification(filtered):

    classify_cri = ['제품명','식품유형','원재료명','유통기한','품목보고번호']

    l1 = set(filtered)
    l2 = set(classify_cri)
    return l1.intersection(l2)    

    # # 뽑아져 나온 단어들과 classify_cri 두 리스트 교집합 개수가 2개 이상일 때 원재료명이 들어간 이미지라고 인식
    # if len(list(l1.intersection(l2))) >= 2:
    #     return True
    # else:
    #     return False


if __name__ == "__main__":
    client = vision.ImageAnnotatorClient()
    split_delimeters = " |,|\(|\)|\.|\||!|\.|\'|\n"
    remove_char = ['|', '', '\n']
    remove_pattern = " |\||\n|\.|\'|:|!"
    
    main()