#!/bin/bash

rm *.zip
zip -r image_to_text.zip * -x beginvegan-venv\*
cd beginvegan-venv/lib/python3.7/site-packages
zip -r /Users/jisuhan/Desktop/beginvegan/SProject/lambda_functions/image_to_text/image_to_text.zip .
cd /Users/jisuhan/Desktop/beginvegan/SProject/lambda_functions/image_to_text

aws s3 rm s3://beginvegan-lambda/image_to_text.zip
aws s3 cp ./image_to_text.zip s3://beginvegan-lambda/image_to_text.zip
aws lambda update-function-code --function-name image_to_text --s3-bucket beginvegan-lambda --s3-key image_to_text.zip
