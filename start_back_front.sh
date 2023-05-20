#!/bin/bash

cd frontend/my-app/src

npm run start &

cd ..
cd ..
cd ..

cd backend

python3 app.py

echo 'finish'
