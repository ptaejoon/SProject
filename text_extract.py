
import io
from google.cloud import vision

def main():

    print(extract_text("./testimg2.jpeg"))

def extract_text(path):

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    if texts:
        texts = texts[0].description
    else:
        texts = None

    return texts


if __name__ == "__main__":
    client = vision.ImageAnnotatorClient()
    main()