from konlpy import tag

class Tokenizer:

    def __init__(self, text):

        if not type(text) == str:
            raise ValueError("string type 이 아닙니다.")

        self.text = text

    def show(self):

        print(self.text)

    def hannanum(self):

        h1 = tag.Hannanum()
        print(h1.nouns(self.text))

    def kkma(self):

        kkma = tag.Kkma()
        print(kkma.nouns(self.text))

    # def komoran(self):

    #     komoran = tag.Komoran(userdic="./dic.txt")
    #     print(komoran.nouns(self.text))

    # def mecab(self):

    #     mecab = tag.Mecab()
    #     print(mecab.nouns(self.text))

    def okt(self):

        okt = tag.Okt()

        print(okt.nouns(self.text))


    


