from django.shortcuts import render

# Create your views here.



def new(request):


    title = '测试标题'
    author = '测试作者'
    nice = '测试文章'
    context = {'title': title, 'author': author, 'nice': nice}
    return render(request,'index.html',context)
