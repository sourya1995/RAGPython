#!/bin/bash

echo "Testing the root endpoint..."
curl http://127.0.0.1:8000/


echo "Testing file upload..."
#curl -X 'POST' 'http://127.0.0.1:8000/uploadfile/' -F 'file=/home/sourya/Desktop/RAGPython/obama.txt'

curl -X 'POST' 'http://127.0.0.1:8000/uploadfile' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@/home/sourya/Desktop/RAGPython/obama.txt'



echo "Testing the ask question endpoint..."
curl -X 'POST' \
'http://127.0.0.1:8000/ask' \
-H 'Content-Type: application/json' \
-d '{"question": "What is the capital of France?"}'