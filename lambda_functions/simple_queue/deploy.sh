#!/bin/bash

rm *.zip
zip simple_queue.zip -r *

aws s3 rm s3://beginvegan-lambda/simple_queue.zip
aws s3 cp ./simple_queue.zip s3://beginvegan-lambda/simple_queue.zip
aws lambda update-function-code --function-name simple_queue --s3-bucket beginvegan-lambda --s3-key simple_queue.zip
