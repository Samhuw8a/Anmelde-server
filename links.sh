#! /bin/bash

mkdir logs
cd logs
mkdir errors
cd ..

cd tests

rm argparser.py
ln ../src/argparser.py .

rm _logging.py
ln ../src/_logging.py .

rm settings_cls.py
ln ../src/settings_cls.py .

rm handling.py
ln ../src/handling.py .

rm main.py
ln ../src/main.py .

rm email_handler.py
ln ../src/email_handler.py .

rm errors.py
ln ../src/errors.py .
