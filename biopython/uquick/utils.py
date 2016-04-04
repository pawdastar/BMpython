# coding: utf-8
import json

from django.http import HttpResponse
from django.shortcuts import render_to_response
import time
import datetime
from bson.objectid import ObjectId

import os

class ComplexEncoder(json.JSONEncoder):
    '''
    encoder for json dumps
    '''

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, ObjectId):
            return obj.__str__()
        else:
            return json.JSONEncoder.default(self, obj)

def response(statusCode=301, msg='method not allowed', data=None, return_type = 'dict'):
    null_return = {}
    if return_type == 'list':
        null_return = []
    elif return_type == 'string':
        null_return = ''
    return HttpResponse(
        json.dumps(
            dict(
                code = statusCode,
                message = msg if msg else '',
                data = data if data else null_return
            )
        )
    )

def render(request, template, data=None, *args, **kwargs):
    '''
    '''
    if data:
        data.update({'menu': get_menu(request), 'admin_realname': request.session.get('user')['realname'], 'cur_uri':request.path})
    else:
        data = {'menu': get_menu(request), 'admin_realname': request.session.get('user')['realname'], 'cur_uri':request.path}

    return render_to_response(template, data, *args, **kwargs)


#计算星座
def constellation(month, day):
    # print month, type(month), '**'
    # print day, type(day), '**'
    n = (u'摩羯座',u'水瓶座',u'双鱼座',u'白羊座',u'金牛座',u'双子座',u'巨蟹座',u'狮子座',u'处女座',u'天秤座',u'天蝎座',u'射手座')
    d = ((1,20),(2,19),(3,21),(4,21),(5,21),(6,22),(7,23),(8,23),(9,23),(10,23),(11,23),(12,23))
    return n[len(filter(lambda y:y<=(month,day), d))%12]

def timestamp_to_strtime(timestamp):
    '''
    时间戳转为时间字符串
    '''

    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))

def timestamp_MS():
    '''
    毫秒级时间戳
    '''
    return int(time.time() * 1000)

def timestamp():
    '''
    秒级时间戳
    '''
    return int(time.time())

def timestamp_today_begin():

    return strtime_to_timestamp(time.strftime('%Y-%m-%d 00:00:00',time.localtime(time.time())))

def time_to_str(timestamp):
    '''
    '''

    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def strtime_to_timestamp(str_time):
    '''
    字符串时间转为时间戳
    '''

    return int(time.mktime(time.strptime(str_time,'%Y-%m-%d %H:%M:%S')))

