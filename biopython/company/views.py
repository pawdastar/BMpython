#coding=utf-8
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
import requests
from uquick.utils import response
import json
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os
from answer import *

@csrf_exempt
def com_index(request):
    '''
    返回系统主页哈哈
    :return:
    '''
    return render_to_response('index.html','')

@csrf_exempt
def com_courier(request):
    '''
    courier
    :return:
    '''
    return render_to_response('courier.html','')

@csrf_exempt
def com_business(request):
    '''
    business
    :return:
    '''
    return render_to_response('business.html','')

@csrf_exempt
def com_privacy(request):
    '''
    privacy
    :return:
    '''
    return render_to_response('privacy.html','')

@csrf_exempt
def login(request):
    '''
    GET:登录页, POST:登录操作
    '''


    if request.method == 'GET':
        # 登录页面
        user = request.session.get('user')
        if user:
            userid = user.get('userid')
            sid = user.get('sid')
            if userid:
                # 判断一下session是否存在
                data = dict()
                data['user'] = userid
                data['sid'] = sid
                r = requests.post('http://game.52sourcecode.com/api/user/profile',data)
                result = eval(r._content)
                if result['succeed'] == 1:
                    if result['user']:
                        return redirect('/com_profile')
                else:
                    return redirect('/logout')
        data = dict(error="请登陆")
        return render_to_response('login.html', dict(data=data))
    elif request.method == 'POST':
        # 登录操作
        userid = request.POST.get('userid')
        password = request.POST.get('password')
        data = dict()
        data['mobile_phone'] = userid
        data['password'] = password
        data['platform'] = 'ios'
        data['ver'] = 1
        r = requests.post('http://game.52sourcecode.com/api/user/signin',data)
        result = eval(r._content)
        if result['succeed'] == 1:
            session_user = dict(
            userid=result['user']['id'],
            sid=result['sid'],
            )
            request.session['user'] = session_user
            return redirect('/com_profile')
        else:
            r_data = dict()
            r_data['info'] = 'WRONG NUMBER OR PASSWORD'
            return render_to_response('login.html',dict(data=r_data))


@csrf_exempt
def logout(request):
    '''
    退出登录
    '''
    request.session.clear()
    return redirect('/login')

@csrf_exempt
def register(request):
    '''
    注册
    '''
    return redirect('/login')


@csrf_exempt
def edit_profile(request):
    '''
    个人信息页面
    '''
    request.session.clear()
    return redirect('/login')


@csrf_exempt
def com_backend(request):
    '''
    后台 Dashborad
    '''
    if request.method == 'GET':
        return render_to_response('backend.html','')

@csrf_exempt
def com_profile(request):
    '''
    个人信息页面
    '''
    if request.method == 'GET':
        user = request.session.get('user')
        if user:
            data = dict(
            user=user['userid'],
            sid=user['sid'],
            )
            r = requests.post('http://game.52sourcecode.com/api/user/profile',data)
            result = json.loads(r.content)
            r_data = dict()
            if result['succeed'] == 1:
                r_data['fname'] = result['user']['given_name']
                r_data['lname'] = result['user']['family_name']
                r_data['email'] = result['user']['email']
                r_data['phone'] = result['user']['mobile_phone']
                r_data['car'] = result['user']['car']
                r_data['avatar_url'] = result['user']['avatar']['thumb']
                return render_to_response('profile.html',dict(data=r_data))
        return redirect('/login')
        # data = dict()
        # data['fname'] = 'Da'
        # data['lname'] = 'Zhang'
        # data['email'] = 'davidzd@163.com'
        # data['phone'] = '18601041575'
        # data['phone'] = '18601041575'
        # return render_to_response('profile.html',dict(data = data))
    elif request.method == 'POST':
        user = request.session.get('user')
        if user:
            data = dict(
            user=user['userid'],
            sid=user['sid'],
            )
            r = requests.post('http://game.52sourcecode.com/api/user/profile',data)
            result = json.loads(r.content)
            r_data = dict()
            if result['succeed'] == 1:
                data = dict()
                data['fname'] = request.POST.get('first_name','')
                data['lname'] = request.POST.get('last_name','')
                data['email'] = request.POST.get('email','')
                data['phone'] = request.POST.get('phone_number','')
                data['home_address'] = request.POST.get('home_address')
                data['abn'] = request.POST.get('abn')
                data['vehicle'] = request.POST.get('vehicle')
                data['pre_working_hours'] = request.POST.get('hours')
                data['bank_name'] = request.POST.get('bank_name')
                data['bsb'] = request.POST.get('bsb')
                data['account_name'] = request.POST.get('account_name')
                data['account_number'] = request.POST.get('account_number')
                r = requests.post('')
    elif request.method == 'GET':
        return response('No Access')

@csrf_exempt
def update_avatar(request):
    '''
    修改个人头像
    '''
    if request.method != 'POST':
        return response(msg='方法错误 ！')
    elif request.method == 'POST':
        if len(request.FILES)!=0:
            picfile = request.FILES['picfile']
            name = str(picfile._name)
            af = name.split('.')[-1]
            if af == 'png' or 'jpg' or 'gif':
                user = request.session.get('user')
                userid = user.get('userid')
                sid = user.get('sid')
                if userid:
                    # 判断一下session是否存在
                    data = dict()
                    data['uid'] = userid
                    data['sid'] = sid
                    file = dict()
                    file['avatar'] = picfile
                    r = requests.request('post','http://game.52sourcecode.com/api/user/change-avatar',data=data, files=file)
                    print r._content
        else:
            return redirect('/com_profile')
    return redirect('/com_profile')

@csrf_exempt
def get_answer(request):
    '''
    上传并获取答案
    '''
    if request.method != 'POST':
        return response(msg='方法错误 ！')
    elif request.method == 'POST':
        if len(request.FILES)!=0:
            reference = request.FILES['reference']
            reads = request.FILES['read']
        try:
            for s in SeqIO.parse(reference, "fasta"):
              f = open('alignment1.txt','w')
              aligner = Aligner1(s)
              align_0 = 0
              align_1 = 0
              align_over_2 = 0
              count_all = 0
              # get each read aligned
              for each_read in SeqIO.parse(reads, "fasta"):
                count_all += 1
                result = aligner.align(each_read)
                if result:
                  if len(result) == 1:
                    align_1 += 1
                  else:
                    align_over_2 += 1
                  f.write("ReadName: %s\t"%each_read.id)
                  if result[0].strand == '-':
                    # f.write("Position: %s\t"%str(len(aligner.refseq)-((int(result[0].pos))+len(each_read.seq))+2))
                    f.write("PositionL %s\t"%str(int(result[0].pos)-len(each_read)+2))
                  else:
                    f.write("Position: %s\t"%str(result[0].pos))
                  f.write("Alignment: %s\tStrand: %s\tNumber of Alignments: \t%d\n"%(str(result[0].chr),str(result[0].strand),len(result)))
                else:
                  align_0 += 1
                  f.write("ReadName: %s\tPosition: %s\tStrand: %s\tNumber of Alignments: %s\t\n"%(each_read.id,'0','*','0'))
              f.close()
              print '''
              Alignment Statistic:
              ----------------------
              None:        %d Per:%f
              Exactly One: %d Per:%f
              Over Two:    %d Per:%f

              '''%(align_0,align_0/count_all,align_1,align_1/count_all,align_over_2,align_over_2/count_all)
              r_list = []
              f = open('alignment1.txt','r')
              for i in range(count_all):
                  r_list.append(f.readline())
              break
            return render_to_response('answer.html',dict(data=r_list))
        #Stop after the fist sequence in the reference
        except IOError as e:
            print "Could not read reference sequence file (see below)!"
            print e
            sys.exit(1)
        else:
            return redirect('/')
    return redirect('/')
