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
from pymongo import MongoClient as MC
import re
import datetime
import locale
client = MC('mongodb://localhost:27017/')
db = client.faces_EOB.FRS_dialoguser


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


def journal(req):
    id = req.GET['uid']
    name = []
    for i in db.find({'uid': id}, {'name': 1}):
        name.append(i['name'])
    urfolder = str(pl.Path(__file__).parents[1])
    with open(urfolder + '\\FRS\\static\\facephotos\\' + id + '\\' + id + '.txt', 'r') as jrnl:
        locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
        a = [datetime.datetime.strptime(j[:16], '%Y-%m-%d %H:%M').strftime('%d %b %Y %H:%M, %A') for j in jrnl.readlines()]
    return render(req, 'FRS/journal.html', {
        'id': id,
        'name': name,
        'times': a
    })


def index(req):
    return render(req, 'FRS/index.html', {})


def faces(req):
    if not req.user.is_authenticated:
        return redirect('/admin/login/?next=/faces')
    data = []
    for i in db.find({}, {'_id': 0, 'uid': 1, 'name': 1, 'time_enrolled': 1, 'photo': 1}):
        data.append((i['uid'], i['name'], i['time_enrolled'], i['photo']))
    return render(req, 'FRS/faces.html', {
        'data': data,
    })


def filtered_faces(req):
    time = req.GET['time']
    name = req.GET['name']
    urfolder = str(pl.Path(__file__).parents[1])
    ids = []
    for i in db.find({'name': re.compile(name, re.IGNORECASE)}, {'_id': 0, 'uid': 1}):
        ids.append(str(i['uid']))

    for id in ids[::-1]:
        with open(urfolder + '\\FRS\\static\\facephotos\\' + id + '\\' + id + '.txt', 'r') as inp:
            times = inp.read().split()
            if time:
                if time not in times:
                    ids.remove(id)
                else:
                    continue
        inp.close()
    data = []
    for i in db.find({'name': re.compile(name, re.IGNORECASE), 'uid': {'$in': ids}}, {'_id': 0, 'uid': 1, 'name': 1, 'time_enrolled': 1}):
        data.append((i['uid'], i['name'], i['time_enrolled']))

    return render(req, 'FRS/filtered_faces.html', {
        'data': data,
        'name_filter': name,
        'date_filter': time,
    })


def save_name(req):
    nm = req.GET['name']
    id = req.GET['uid']
    db.update_one({'uid': {'$eq': id[4:]}},
                  {'$set': {'name': nm}})
    return HttpResponse(json.dumps({'name': nm}))


def delete_name(req):
    thisf = str(pl.Path(__file__).parents[1])
    nm = req.GET['name']
    id = req.GET['uid']
    db.delete_one({'uid': {'$eq': id[4:]}})
    waytofolder = os.path.join(thisf + '\\FRS\\static\\facephotos\\' + id[4:])
    shutil.rmtree(waytofolder)
    return HttpResponse(json.dumps({'name': nm}))


def merge_names(req):
    thisf = str(pl.Path(__file__).parents[1])
    base = req.GET['base']
    merged = req.GET['merged']
    m_user = db.find_one({'uid': {'$eq': merged}})
    for i in m_user.get('vector'):
        db.update_one({'uid': {'$eq': base}},
                     {'$addToSet': {'vector': i}})
    db.delete_one({'uid': {'$eq': merged}})
    waytofolder = os.path.join(thisf + '\\FRS\\static\\facephotos\\' + merged)
    shutil.rmtree(waytofolder)
    return HttpResponse(json.dumps({'base': base}))


def stream(req):
    data = []
    for i in db.find({}, {'_id': 0, 'uid': 1, 'name': 1, 'time_enrolled': 1}).limit(5):
        data.append((i['uid'], i['name'], i['time_enrolled']))
    lang = get_lang(req)

    res = render(req, 'FRS/stream.html', {
        "lang": lang,
        'data': data,
    })
    res['Feature-Policy'] = "fullscreen *"
    return res