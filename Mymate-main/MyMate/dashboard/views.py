from pyexpat import model
from urllib import request
from django.shortcuts import render,redirect
from . forms import *
from django.contrib import messages
from django.views import generic

from youtubesearchpython import VideosSearch
import requests
import json
import wikipedia

from .decorators import login_required 

# Create your views here.
def home(request):
    return render(request,'dashboard/home.html')

@login_required  ##this is as decorator
def notes(request):
    if request.method=='POST':
        form=Notesform(request.POST)  #by this the data will be save in the form
        if form.is_valid():
            notes=Notes(user=request.user,title=request.POST['title'],description=request.POST['description'])
            notes.save()
            messages.success(request,'Successfully  added Notes by {}'.format(request.user.username))
    else:    
        form=Notesform()
    notes=Notes.objects.filter(user=request.user)
    context={'notes':notes,'form':form}
    return render(request,'dashboard/notes.html',context)

@login_required
def delete_note(request,pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")



class Notesdetailedview(generic.DetailView):   #generic views is a class but the other views are the functions
    model = Notes

@login_required
def homework(request):
    if request.method=='POST':
        homeworkform=Homeworkform(request.POST)
        if homeworkform.is_valid():
            try:
                finish=request.POST['is_finish']
                if finish=='on':
                    finish=True
                else:
                    finish=False
            except:
                finish=False

            homeworks=Homework(
                 user=request.user,
                 subject=request.POST['subject'],
                 title=request.POST['title'],
                 description=request.POST['description'],
                 due=request.POST['due'],
                 is_finish=finish
                 )
            homeworks.save()
            messages.success(request,"Homework added from {}".format(request.user.username))
    else:
        homeworkform=Homeworkform()
    homeworks=Homework.objects.filter(user=request.user)
    homework_pending=False
    for homework in homeworks:    
        if not homework.is_finish :
            homework_pending=True
        else:
            homework_pending=False
        
    context={'homeworks':homeworks,'homework_pending':homework_pending,'homeworkform':homeworkform}
    return render(request,'dashboard/homework.html',context)


@login_required
def homework_update(request,pk=None):
    homework=Homework.objects.get(id=pk)
    if homework.is_finish==True:
        homework.is_finish=False
    else:
        homework.is_finish=True

    homework.save()

    return redirect('homework')


@login_required
def delete_homework(request,pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect('homework')


def youtube(request):
    if request.method=='POST':
        form=dashboardform(request.POST)
        text=request.POST['text']
        video=VideosSearch(text,limit=10)
        result_list=[]
        for i in video.result()['result']:
            result_dict={
                 'input':text,
                 'title':i['title'],
                 'duration':i['duration'],
                 'thumbnail':i['thumbnails'][0]['url'],
                 'channel':i['channel']['name'],
                 'link':i['link'],
                 'views':i['viewCount']['short'],
                 'published':i['publishedTime']
                }
            desc=''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc+=j['text']
            result_dict['description']=desc
            result_list.append(result_dict)
        context={
             'form':form,
             'results':result_list
            }
        return render(request,'dashboard/youtube.html',context)            
    else:
        form=dashboardform()
    context={'form':form}
    return render(request,'dashboard/youtube.html',context)



@login_required
def todo(request):
    if request.method=='POST':
        form=Todoform(request.POST)
        if form.is_valid():
            try:
               status=request.POST['status']
            #    print(" SO HERE THE STATUS FROM THE FORM IS {}".format(status))
               if status=='on':
                   status=True
               else:
                   status=False   
            except:
               status=False   
                   
            todo=Todo(
                user=request.user,
                title=request.POST['title'],
                status=status
                )
            todo.save()
            messages.success(request,'successfully added in todo list by {}'.format(request.user.username))
    else:
        form=Todoform()
    todos=Todo.objects.filter(user=request.user)
    pending=False
    for todo in todos:
        if todo.status == False:
            pending=True
    context={'todos':todos,'pending':pending,'form':form}
    return render(request,'dashboard/todo.html',context)  


@login_required
def update_todo(request,pk=None):
    todo=Todo.objects.get(id=pk)
    if todo.status == False:
        todo.status=True
    else:
        todo.status=False
    todo.save()
    return redirect('todo') 


@login_required
def delete_todo(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect('todo')   




def books(request):
    if request.method=='POST':
        form=dashboardform(request.POST)
        if form.is_valid():
            text=request.POST['text']
            url='https://www.googleapis.com/books/v1/volumes?q='+text
            r=requests.get(url)
            answer=r.json()
            result_list=[]

            for i in range(10):
                result_dict={
                    'title':answer['items'][i]['volumeInfo']['title'],
                    'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                    'description':answer['items'][i]['volumeInfo'].get('description'),
                    'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                    'categories':answer['items'][i]['volumeInfo'].get('categories'),
                    'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                    'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                    'preview':answer['items'][i]['volumeInfo'].get('previewLink')
                    }
                result_list.append(result_dict)
            context={'form':form,'results':result_list}
            return render(request,'dashboard/books.html',context)
    else:
        form=dashboardform()
    context={'form':form}
    return render(request,'dashboard/books.html',context)



def dictionary(request):
    if request.method=='POST':
        form=dashboardform(request.POST)
        if form.is_valid():
            text=request.POST['text']
            url='https://api.dictionaryapi.dev/api/v2/entries/en_US/'+text
            r=requests.get(url)
            answer=r.json()
            
            try:
                phonetics=answer[0]['phonetics'][0]['text']       #decode: in first answer -> first phonetic ->text
                audio=answer[0]['phonetics'][0]['audio']
                definition=answer[0]['meanings'][0]['definitions'][0]['definition']
                example=answer[0]['meanings'][0]['definitions'][0]['example']
                synonyms=answer[0]['meanings'][0]['definitions'][0]['synonyms']
                context={
                    'form':form,
                    'phonetics':phonetics,
                    'definition':definition,
                    'audio':audio,
                    'example':example,
                    'synonyms':synonyms,
                    'input':text
                    }
            except:
                context={
                   'form':form,
                    'input':''
                    }
            return render(request,'dashboard/dictionary.html',context)
    else:        
        form=dashboardform()
    context={'form':form}
    return render(request,'dashboard/dictionary.html',context)



def wikipedia_view(request):
    if request.method=='POST':
        form=dashboardform(request.POST)
        if form.is_valid():
            text=request.POST['text']
            search=wikipedia.page(text)
            context={
                 'form':form,
                 'title':search.title,
                 'link':search.url,
                 'details':search.summary
                }
           

        return render(request,'dashboard/wiki.html',context)
    else:
        form=dashboardform()
    context={'form':form}
    return render(request,'dashboard/wiki.html',context)