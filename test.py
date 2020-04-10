import numpy as np
# boxes = np.array([[[100, 200, 300, 400],['ня'],['wo']],[[100, 220, 200, 400],['ня'],['wo']]])
#
# for i in range(len(boxes)):
#     if boxes[i][1] - boxes[i][0] < 120:
#         boxes = np.delete(boxes,i,0)
# print(boxes)
# print(len(boxes))

# boxes = np.array([[27, 30, 31], [40, 52, 64]])
# boxes2 = np.array([[27, 30, 32], [42, 54, 67]])
from django.db import connection
import os
from datetime import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vef.settings')
cursor = connection.cursor()
# cursor.execute("SELECT uid FROM main.FRS_dialoguser LIMIT 1")
# id = cursor.fetchall()
# print(id)
# coords = np.array([[89, 329, 360, 520]])
# cursor = connection.cursor()
cursor.execute("SELECT uid FROM main.FRS_dialoguser LIMIT 1")
id = ' '.join(map(str, cursor.fetchall()[0]))
# cursor.execute(f"SELECT strftime('%Y-%m-%d %H:%M', time_enrolled) FROM main.FRS_dialoguser WHERE uid = '{id}'")
# user_tm = ' '.join(map(str, cursor.fetchall()[0]))
# cursor.execute(f"SELECT coords FROM main.FRS_dialoguser WHERE uid = '{id}'")
# old_coords = np.array([[int(i) for i in ' '.join(map(str, cursor.fetchall()[0])).replace('[', '').replace(']', '').split()]])
# print(old_coords)
# print(coords)
# overlap = coords * old_coords  # Logical AND
# union = coords + old_coords  # Logical OR
# IOU = overlap.sum() / float(union.sum())
# print(overlap)
# print(union)
# print(IOU)
cursor.execute(f"SELECT time_enrolled FROM main.FRS_dialoguser WHERE uid = '{id}'")
# user_tm = ' '.join(map(str, cursor.fetchall()[0]))[14:]
user_tm = cursor.fetchall()[0][0]
now = datetime.now()
time = now - user_tm
print(time.total_seconds())
if time.total_seconds() > 1000:
    print('alarm')
else:
    print('ok')
print(18*60)
# tm = datetime.strptime('2020-03-31 16:7:04', '%Y-%m-%d %H:%M:%S')
# print(user_tm)
# print(tm)
# print(tm-user_tm)
# if datetime.strptime(str(tm-user_tm), '%H:%M:%S') < datetime.strptime('00:2:00', '%H:%M:%S'):
#     print('ok')
# else:
#     print('not ok')