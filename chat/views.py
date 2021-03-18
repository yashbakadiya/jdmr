
from django.shortcuts import render
from pymongo import MongoClient
import datetime
import pymysql
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import default_storage
from chat.models import ChatApplication



def index(request):
    return render(request, 'chat/index.html')

def room(request,room_name,ts):
    # room=request.session.get['roomname']
    # print(room)
    #room=request.GET['roomname']
    #name=request.GET['ts']
    if ts == "Teacher":

        return render(request, 'chat/room1.html', {
            'room': room_name
        })
    elif ts == "Student":
         return render(request, 'chat/room2.html', {
            'room': room_name
        })






def send(request,room_name,ts):
    try:
        message=request.POST["msg"]
        #room_name=request.POST["room"]
        dtime=datetime.datetime.now()
        
        print(message)
        

        
        
        if message != "" :
            c=ChatApplication()
            c.dtime="{0}".format(dtime)
            c.message="{0}".format(message)
            c.room="{0}".format(room_name)
            c.ts="{0}".format(ts)
            c.fl="0"
            c.save()

       
    
    except:
        pass
    

    a=[]
    l=[]
    # a=list(datadb.find())
    a=ChatApplication.objects.filter(room=room_name).order_by('dtime')
   
    l.append(a)
    


    return render(request,'chat/room1.html',{'a':a})


def send2(request,room_name,ts):
    try:
        message=request.POST["msg"]
        #room_name=request.POST["room"]
        dtime=datetime.datetime.now()
        
        

        
        
        if message != "" :
            c2=ChatApplication()
            c2.dtime="{0}".format(dtime)
            c2.message="{0}".format(message)
            c2.room="{0}".format(room_name)
            c2.ts="{0}".format(ts)
            c2.fl="0"
            c2.save()

       
    
    except:
        pass
    

    a=[]
    l=[]
    # a=list(datadb.find())
    a=ChatApplication.objects.filter(room=room_name).order_by('dtime')
   
    l.append(a)
    


    return render(request,'chat/room2.html',{'a':a})


























def upload1(request,room_name,ts):

    myfile = request.FILES['myfile']
    #room_name=request.POST["room"]
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    uploaded_file_url = fs.url(filename)
    dtime=datetime.datetime.now()
    a=list(datadb.find())
    add={
    'id' : len(a)+1,
    'dtime' : dtime,
    'message' : "{0}".format(uploaded_file_url),
    'room' : room_name,
    'ts' : 1,
    'file' : 0,
    }
    if myfile != "" and room_name != "":
        datadb.insert_one(add)
    a=list(datadb.find())
    i=0
    j=[]
    m=[]
    k=[]
    l=[]
    teach=[]
    stud=[]
    while i<int(len(a)):
        if a[i]['room']==room_name:
            e=a[i]['message']
            r=a[i]['dtime']
            check=a[i]['ts']
            file=a[i]['file']
            i=i+1
            if check=="0":
                teach.append(1)
            else:
                stud.append(0)
            j.append(e)
            m.append(r)
            k.append(file)
    
    l=zip(j,m,k,teach,stud)

    m={
    "messages" : l,
    }

    return render(request,'chat/room1.html',m)






def upload2(request,room_name,ts):

    myfile = request.FILES['myfile']
    #room_name=request.POST["room"]
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    uploaded_file_url = fs.url(filename)
    dtime=datetime.datetime.now()
    a=list(datadb.find())
    add={
    'id' : len(a)+1,
    'dtime' : dtime,
    'message' : "{0}".format(uploaded_file_url),
    'room' : room_name,
    'ts' :2,
    'file' : 1,
    }
    if myfile != "" and room_name != "":
        datadb.insert_one(add)
    a=list(datadb.find())
    i=0
    j=[]
    m=[]
    k=[]
    l=[]
    teach=[]
    stud=[]
    while i<int(len(a)):
        if a[i]['room']==room_name:
            e=a[i]['message']
            r=a[i]['dtime']
            check=a[i]['ts']
            file=a[i]['file']
            i=i+1
            if check=="0":
                teach.append(1)
            else:
                stud.append(0)
            j.append(e)
            m.append(r)
            k.append(file)
    
    l=zip(j,m,k,teach,stud)

    m={
    "messages" : l,
    }

    return render(request,'chat/room2.html',m)
