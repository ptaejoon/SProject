
import io
from PIL import Image
from google.cloud import vision
def main():
    texts = extract_text("timg/important4.jpg")
    #print(texts.replace('|','\n'))
    #f = open("extracted_text.txt",'w')
    #f.write(texts)
    #f.close()
    img = Image.open("timg/important4.jpg")
    num = 1
    for t_list in texts:
        cropped_img = img.crop(t_list)
        cropped_img.save('revised/t'+str(num)+'.jpg')
        num = num+1
def set_to_zero(k):
    if k < 0:
        k = 0
    return k

def cut_texts(texts):
    lists = []
    text = ''
    x1 = None
    y1 = None
    for t in texts:
        #x1 = t.bounding_poly.vertices[0].x
        #y1 = t.bounding_poly.vertices[0].y
        #x2 = t.bounding_poly.vertices[2].x
        #y2 = t.bounding_poly.vertices[2].y
        
        #x1 = set_to_zero(x1)
        #x2 = set_to_zero(x2)
        #y1 = set_to_zero(y1)
        #y2 = set_to_zero(y2)
        
        #lis = [x1,y1,x2,y2]
        #lists.append(lis)
        #print(lis)
        if t.description == '\n' or t.description == '|' or t.description[-1] == '\0':
            if x1 == None and y1 == None:
                continue
            #print(text)
            x2 = t.bounding_poly.vertices[2].x
            y2 = t.bounding_poly.vertices[2].y
            if y2 < 0:
                y2 = 0
            if x2 < 0:
                x2 = 0
            lis = [x1,y1,x2,y2]
            print(lis)
            lists.append(lis)
            text = ''
            x1 = None
            y1 = None
        else:
            #print(text)
            text = text+t.description
            if x1 == None and y1 == None :
                x1 = t.bounding_poly.vertices[0].x
                y1 = t.bounding_poly.vertices[0].y
                if x1 < 0 :
                    x1 = 0
                if y1 < 0 :
                    y1 = 0
    return lists

def extract_text(path):

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.document_text_detection(image=image)
    texts = response.full_text_annotation
    bound = []
    if texts:
        for page in texts.pages:
            for block in page.blocks:
                for para in block.paragraphs:
                    x1 = para.bounding_box.vertices[0].x
                    y1 = para.bounding_box.vertices[0].y
                    x2 = para.bounding_box.vertices[2].x
                    y2 = para.bounding_box.vertices[2].y
                    lis= [x1,y1,x2,y2]
                    bound.append(lis)
            #for bloc in page.blocks:
                #print("block:", bloc)
                #for paragraph in bloc.paragraphs:
                    #print("para :",paragraph)

        #print(texts[0].description)
        #texts = cut_texts(texts[1:])
 #       print(texts)
 #       print(texts[0].bounding_poly.vertices)
 #       texts = texts[0].description
 #       img = Image.open(path)

    else:
        texts = None
    return bound
    #return texts


if __name__ == "__main__":
    client = vision.ImageAnnotatorClient()
    main()

