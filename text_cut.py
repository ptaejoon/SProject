
import io
from PIL import Image
from google.cloud import vision
def main():
    f = open('tt5','w')
    texts = extract_text("timg/t (11).jpg")
    for lis in texts:
        print("-----------------------------------------------------------")
        if lis is not None and lis is not '\n' and lis is not '' and lis is not ' ':
            f.write(lis+'\n')
            print(lis)
    f.close()
def extract_text(path):

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    texts = texts[0].description
    print(texts)
    texts = texts.replace('1','\n1')
    texts = texts.replace('|','\n')
    texts = texts.split('\n')
    return texts


if __name__ == "__main__":
    client = vision.ImageAnnotatorClient()
    main()

