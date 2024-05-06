from django.shortcuts import render,redirect
from .forms import *
from .models import News

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def delet(request,id):
    News.objects.get(id=id).delete()
    return redirect('home')

def Logout(request):
    logout(request)
    return redirect('home')

def Login(request):
    login_form = LoginForm()
    if request.POST:
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                return redirect('home')
    return render(request, 'create.html', {'form': login_form,'funk':'Login'})

def home(request):
    if request.user.is_authenticated:
        if request.POST:
            id=request.POST['id']
            one_news=News.objects.get(id=id)
            if request.user in one_news.like.all():
                one_news.like.remove(request.user)
            else:
                one_news.like.add(request.user)

        hammasi=News.objects.all()
        search=request.GET.get('search')
        if search:
            hammasi=News.objects.filter(title__icontains=search)
        hammasi=hammasi[::-1]
        context={'news':hammasi}
        return render(request,"no-sidebar.html",context)
    else:
        return Login(request)

def detail(request, id):
    a = News.objects.get(id = id)    
    form=CommentForm()
    a.prasmotr +=1
    a.save()
    if request.POST:
        if not request.user.is_authenticated:
            return redirect('login')
        form=CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                izoh=form.cleaned_data['izoh'],
                user=request.user,
                news=a
                )
            return redirect('detail',a.id)
    return render(request, 'single-post.html', {'one': a, 'form': form})

def createCategory(request):
    form=CategoryForm()
    if request.POST:
        form=CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request,'create.html',{'form':form,'funk':'tur'})


def user_register(request):
    form=UserForm()
    if request.POST:
        form=UserForm(request.POST)
        if form.is_valid():
            user=form.save()
            parol=form.cleaned_data['password']
            user.set_password(parol)
            user.save()
            login(request, user)
            return redirect('home')
    return render(request,'create.html',{'form':form,'funk':'register'})



def createNews(request):
    form=NewsForm()
    if request.POST:
        form=NewsForm(request.POST,files=request.FILES)
        if form.is_valid():
            News.objects.create(
                author=request.user,
                title=form.cleaned_data['title'],
                text=form.cleaned_data['text'],
                tur=form.cleaned_data['tur'],
                rasm=form.cleaned_data['rasm']
                )
            return redirect("home")
    print(dir(form))
    return render(request, 'create.html',{'form':form,'funk':'news'})


def editnews(request,id):

    edit=News.objects.get(id=id)
    form=NewsForm(instance=edit)
    print(dir(form))
    if request.POST:
        form=NewsForm(request.POST,files=request.FILES)
        if form.is_valid():
            edit.title=form.cleaned_data['title']
            edit.text=form.cleaned_data['text']
            edit.tur=form.cleaned_data['tur']
            edit.rasm=form.cleaned_data['rasm']
            edit.save()
            return redirect('detail',edit.id)
    return render(request,'create.html',{'form':form,'funk':'edit'})
    

def createComment(request,id):
    news=News.objects.get(id=id)
    form=CommentForm()
    if request.POST:
        form=CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                izoh=form.cleaned_data['izoh'],
                user=request.user,
                news=news
                )
            return redirect('detail',news.id)
    return render(request, 'detail.html',{'form':form})            

