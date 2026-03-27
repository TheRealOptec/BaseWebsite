import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mybase_project.settings')

import django
django.setup()
from mybase.models import Topic, Page

def sum(dictionary, key):
    sum = 0
    for dict, dictval in dictionary:
        sum += dictval[key]
    return sum


def populate():
    coding = [
        {'title':'Python','views':35,'likes':31},
        {'title':'Java','views':64,'likes':30},
        {'title':'XJAX','views':32,'likes':32}]

    pets = [
        {'title':'Dogs','views':5000,'likes':4000},
        {'title':'Cats','views':10000,'likes':9500},
        {'title':'Igunas','views':324,'likes':250}]
    
    cooking = [
        {'title':'Pasta','views':545,'likes':33},
        {'title':'Pizza','views':6700,'likes':6400},
        {'title':'Peppers','views':32,'likes':9}]

    tops = {'Coding':{'page': coding , 'views':sum(coding, 'views'), 'likes': sum(coding, 'likes')},
            'Pets':{'page': pets , 'views':sum(pets, 'views'), 'likes': sum(pets, 'likes')},
            'Cooking': {'page': cooking , 'views':sum(cooking, 'views'), 'likes': sum(cooking, 'likes')}}
    
    for top, topdata in tops.items():
        views = topdata['views']
        likes = topdata['likes']
        t = add_top(top, views, likes)
        for p in  topdata['page']:
            add_page(t, p['title'], p['views'], p['likes'])

def add_page(topic, title, views=0, likes=0):
    p = Page.objects.get_or_create(topic=topic, title=title)[0]
    p.views = views
    p.likes =  likes
    p.save()
    return p

def add_top(name, views=0, likes=0):
    t = Topic.objects.get_or_create(name=name)[0]
    t.likes =likes
    t.views = views
    t.save()
    return t

if __name__ == '__main__':
    print('Staring population script...')
    populate()