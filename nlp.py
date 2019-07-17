from tokenizer import Tokenizer

def nlp(text):

    tk = Tokenizer(text)

    tk.hannanum()
    print("\n")
    tk.kkma()
    print("\n")
    # tk.komoran()
    # print("\n")
    # tk.mecab()
    # print("\n")
    tk.okt()
