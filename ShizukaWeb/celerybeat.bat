call C:\Users\Master\ShizukaEnvironment\Scripts\activate.bat
cd C:\Users\Master\Documents\GitHub\ShizukaWeb
celery -A ShizukaWeb beat --loglevel=info
