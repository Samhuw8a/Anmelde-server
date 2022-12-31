#! /bin/bash

cd tests

rm handling.py
ln ../src/handling.py .

rm main.py
ln ../src/main.py .

rm email_handler.py
ln ../src/email_handler.py .

rm errors.py
ln ../src/errors.py .
