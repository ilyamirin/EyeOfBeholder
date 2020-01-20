cd C:\Users\py\Downloads\redis-5.0.5 && start powershell -Command while ($true) {ubuntu run redis-server}
timeout /t 5 /nobreak
cd C:\Users\py\Documents\GitHub\eob && start powershell -Command  while ($true) {daphne -e "ssl:8001:privateKey=myselfsigned.key:certKey=myselfsigned.cer" vef.asgi:application}
timeout /t 7 /nobreak
start "" "https://localhost:8001/stream"
timeout /t 5 /nobreak
start powershell -Command while ($true) {python manage.py runworker recognizefaces}

exit