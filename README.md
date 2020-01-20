# Face Recognition System 
# "Eye Of Beholder" 
# Appended and far more developed by FEFU students - Platon & Egor
#Manual:
To run this on host pc:
1. You`ll need to install python 3.x x64 and install requirments using cmd pip install -r requirments.txt from EyeOfBeholder directory;
2. Install Cuda 10.0 from Nvidia and pip install mxnet-cu100 using cmd;
3. Install ffmpeg;
4. Install Windows Subsistem for Linux. You should use Ubuntu 18.04 LTS from Microsoft store;
5. Using WSL install Redis version 5.0.5 or 5.0.6;
6. Download EyeOfBeholder and ServantGrunbeld files from Git and place them in .../Documents/GitHub;
7. Create database. From EyeOfBeholder run PowerShell and paste "python manage.py migrate";
8. To watch data create superuser using PowerShell "python manage.py createsuperuser" from EyeOfBeholder;
9. Rewrite roots in run.bat like that "C:\root\to\redis-5.0.5" to make it work on host PC;
10. Doubleclick run.bat to run the system.

To run this on other pc:
1. Get host IPv4 address using ipconfig in cmd;
2. Using chrome on client PC go to https://hostip:8001/stream;
3. To watch data on other PC you may create new user with Django admin (https://hostip:8001/admin).

Enjoy!