from django.shortcuts import render

from nice import models

import random


def new(request):

    data = models.New.objects.order_by('?')[0]

    pic = str(random.randint(1, 400))+'.png'
    title = data.title
    author = data.author
    nice = data.article

    context = {'title': title, 'author': author, 'nice': nice, 'pic':pic}
    return render(request, 'index.html', context)
