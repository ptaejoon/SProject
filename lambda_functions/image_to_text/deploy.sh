#!/bin/bash

rm *.zip
zip image_to_text.zip -r *

aws s3 rm s3://beginvegan-lambda/image_to_text.zip
aws s3 cp ./image_to_text.zip s3://beginvegan-lambda/image_to_text.zip
aws lambda update-function-code --function-name image_to_text --s3-bucket beginvegan-lambda --s3-key image_to_text.zip
