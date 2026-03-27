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
        {'title':'Python','views':35,'likes':31, 'body': "fGnaLvNcZQwpKsIeYNNuBcfUJsUnAPsF"},
        {'title':'Java','views':64,'likes':30, 'body': "FZbzHDHfwpbfHuJtPGiBdLBQtAiggQyl"},
        {'title':'XJAX','views':32,'likes':32, 'body': "eWLWnIzTUiasXpfSLBZEsLnDcbNqtJyS"}]

    pets = [
        {'title':'Dogs','views':5000,'likes':4000, 'body': "aVXeWQaWPvnKiHEWyriHXKedsYSGNssR"},
        {'title':'Cats','views':10000,'likes':9500, 'body': "IloBZrAvarYhHqocVoezVVUFVVMDlMOZ"},
        {'title':'Igunas','views':324,'likes':250, 'body': "TJFrRzuJqWrzfKeltlCYhDxXozBwGgoY"}]
    
    cooking = [
        {'title':'Pasta','views':545,'likes':33, 'body': "dkPrPkBRHeyqZvVesAOnJIVoaugeWwpI"},
        {'title':'Pizza','views':6700,'likes':6400, 'body': "mnXJEasLGDgPUBPIrEgKrrEQCOSwiYsC"},
        {'title':'Peppers','views':32,'likes':9, 'body': "mnXJEasLGDgPUBPIrEgKrrEQ RaAmpuPLSOwctNS"}]

    tops = {'Coding':{'page': coding , 'views':sum(coding, 'views'), 'likes': sum(coding, 'likes'), 'description': "FOr thoses who want to talk about coding languages"},
            'Pets':{'page': pets , 'views':sum(pets, 'views'), 'likes': sum(pets, 'likes'), 'description': "For those who want to talk about animals"},
            'Cooking': {'page': cooking , 'views':sum(cooking, 'views'), 'likes': sum(cooking, 'likes'), 'description': "For those who want to share recipes"}}
    
    for top, topdata in tops.items():
        views = topdata['views']
        likes = topdata['likes']
        description = topdata['description']
        t = add_top(top, description, views, likes)
        for p in  topdata['page']:
            add_page(t, p['title'], p['body'], p['views'], p['likes'])

def add_page(topic, title, body, views=0, likes=0):
    p = Page.objects.get_or_create(topic=topic, title=title)[0]
    p.views = views
    p.likes =  likes
    p.body = body
    p.save()
    return p

def add_top(name, description, views=0, likes=0):
    t = Topic.objects.get_or_create(name=name)[0]
    t.likes =likes
    t.views = views
    t.description = description
    t.save()
    return t

if __name__ == '__main__':
    print('Staring population script...')
    populate()