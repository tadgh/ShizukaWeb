call C:\Users\Master\ShizukaEnvironment/Scripts/activate.bat
cd D:\dropbox\github\Shizukaweb
celery -A ShizukaWeb beat --loglevel=info
