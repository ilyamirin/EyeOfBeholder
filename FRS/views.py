from django.shortcuts import render
from workers.consumers import FaceRecognitionConsumer
import os
import pathlib as pl
from io import BytesIO
from PIL import Image
import base64
import pickle
import numpy as np
import cv2
import shutil
import json
from django.forms.models import model_to_dict
from django.db import connection
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import redirect


def redirect_view(request):
    tostream = redirect('/stream')
    return tostream


def get_lang(req):
    lang = 'ru'
    if req.session.get('lang') is None:
        req.session['lang'] = lang
    else:
        lang = req.session.get('lang')

    print('Язык:' + lang)
    return lang


def index(req):
    return render(req, 'FRS/index.html', {})


def faces(req):
    if not req.user.is_authenticated:
        return redirect('/admin/login/?next=/faces')

    cursor = connection.cursor()
    cursor.execute('SELECT uid, name, time_enrolled FROM main.FRS_dialoguser ORDER BY time_enrolled DESC')
    ldb = cursor.fetchall()

    return render(req, 'FRS/faces.html', {
        'data': ldb,
    })

def filtered_faces(req):
    time = req.GET['time']
    name = req.GET['name']
    urfolder = str(pl.Path(__file__).parents[1])
    cursor1 = connection.cursor()
    cursor1.execute(f"SELECT uid FROM main.FRS_dialoguser WHERE name LIKE '%{name}%'")
    uids = cursor1.fetchall()
    cursor = connection.cursor()
    ids = []
    for i in uids:
        ids.append(str(*i))
    for id in ids[::-1]:
        with open(urfolder + '\\FRS\\static\\facephotos\\' + id + '\\' + id + '.txt', 'r') as inp:
            times = inp.read().split()
            if time:
                if time not in times:
                    ids.remove(id)
                else:
                    continue
        inp.close()
    ids = ', '.join(["'" + i + "'" for i in ids])

    # name = name.lower()

    q = f"""
        SELECT uid, name, time_enrolled
        FROM main.FRS_dialoguser
        WHERE uid IN ({ids})
        AND name LIKE '%{name}%'
        ORDER BY time_enrolled DESC
        """
    cursor.execute(q)
    tmr = cursor.fetchall()
    return render(req, 'FRS/filtered_faces.html', {
        'data': tmr,
        'name_filter': name,
        'date_filter': time,
    })


def save_name(req):

    nm = req.GET['name']
    id = req.GET['uid']
    with connection.cursor() as cursor:
        cursor.execute(f"UPDATE main.FRS_dialoguser SET name = '{nm}' WHERE uid = '{id[4:]}'")
    connection.close()

    return HttpResponse(json.dumps({'name': nm}))

def delete_name(req):
    thisf = str(pl.Path(__file__).parents[1])
    nm = req.GET['name']
    id = req.GET['uid']
    with connection.cursor() as cursor:
        cursor.execute(f"DELETE FROM main.FRS_dialoguser WHERE uid = '{id[4:]}'")
    connection.close()
    waytofolder = os.path.join(thisf + '\\FRS\\static\\facephotos\\' + id[4:])
    shutil.rmtree(waytofolder)
    return HttpResponse(json.dumps({'name': nm}))


def stream(req):
    cursor = connection.cursor()

    # flag = req.POST.get('flag')
    # if flag == 'reloadpage':800
    #     cursor.execute('SELECT count(*) FROM main.FRS_dialoguser')
    #     rc = cursor.fetchone()
    #     return json.dumps({'rc': rc[0]}, ensure_ascii=False)

    cursor.execute('SELECT uid, name, time_enrolled FROM main.FRS_dialoguser ORDER BY time_enrolled DESC LIMIT 0, 5 ')
    ldb = cursor.fetchall()
    lang = get_lang(req)
    # cursor.execute('SELECT count(*) FROM main.FRS_dialoguser')
    # rc = cursor.fetchone()

    res = render(req, 'FRS/stream.html', {
        "lang": lang,
        'data': ldb,
        # 'row_count': rc[0],
    })
    res['Feature-Policy'] = "fullscreen *"
    return res