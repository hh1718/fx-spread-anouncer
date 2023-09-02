cd /d %~dp0
cd src
rmdir /s /q packages
mkdir packages
pip install -r ../requirements.txt -t packages --no-user
pip install pypiwin32 -t packages
pip install pypiwin32
cd ../