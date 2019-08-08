#!/bin/bash

scp -i ~/Key/jisu.pem lambda_handler.py ec2-user@ec2-15-164-48-160.ap-northeast-2.compute.amazonaws.com:~/image_to_text
