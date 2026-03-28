import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mybase_project.settings')

import django
django.setup()
from mybase.models import Topic, Page, UserProfile
from django.contrib.auth.models import User

# Sums up the values of a specific field given an array of a population data
def sumPopulationData(popData, key):
    sum = 0
    for d in popData:
        sum += d[key]
    return sum


def populate():
    # Define the posts for each topic
    coding = [
        {'title':'Python','views':35,'likes':31, 'body': "fGnaLvNcZQwpKsIeYNNuBcfUJsUnAPsF"},
        {'title':'Java','views':64,'likes':30, 'body': "FZbzHDHfwpbfHuJtPGiBdLBQtAiggQyl"},
        {'title':'XJAX','views':32,'likes':32, 'body': "eWLWnIzTUiasXpfSLBZEsLnDcbNqtJyS"}
    ]

    pets = [
        {'title':'Dogs','views':5000,'likes':4000, 'body': "aVXeWQaWPvnKiHEWyriHXKedsYSGNssR"},
        {'title':'Cats','views':10000,'likes':9500, 'body': "IloBZrAvarYhHqocVoezVVUFVVMDlMOZ"},
        {'title':'Igunas','views':324,'likes':250, 'body': "TJFrRzuJqWrzfKeltlCYhDxXozBwGgoY"}
    ]
    
    cooking = [
        {'title':'Pasta','views':545,'likes':33, 'body': "dkPrPkBRHeyqZvVesAOnJIVoaugeWwpI"},
        {'title':'Pizza','views':6700,'likes':6400, 'body': "mnXJEasLGDgPUBPIrEgKrrEQCOSwiYsC"},
        {'title':'Peppers','views':32,'likes':9, 'body': "mnXJEasLGDgPUBPIrEgKrrEQ RaAmpuPLSOwctNS"}
    ]
    # Define the topics
    tops = {
        'Coding':{
            'page': coding , 
            'views':sumPopulationData(coding, 'views'), 
            'likes': sumPopulationData(coding, 'likes'), 
            'description': "For thoses who want to talk about coding languages"
        },
        'Pets':{
            'page': pets , 
            'views':sumPopulationData(pets, 'views'), 
            'likes': sumPopulationData(pets, 'likes'), 
            'description': "For those who want to talk about animals"
        },
        'Cooking': {
            'page': cooking , 
            'views':sumPopulationData(cooking, 'views'), 
            'likes': sumPopulationData(cooking, 'likes'), 
            'description': "For those who want to share recipes"
        }
    }
    # Create a test user with the most secure of passwords
    user = add_user("test_user", "12345", "My password is not 12345")
    for top, topdata in tops.items():
        views = topdata['views']
        likes = topdata['likes']
        description = topdata['description']
        t = add_top(top, description, views, likes)
        for p in  topdata['page']:
            add_page(t, p['title'], p['body'], user, p['views'], p['likes'])


def add_user(username, password, bio):
    (user, valid) = User.objects.get_or_create(username=username)
    if valid:
        print("Creating a new user!")
        user.password = password
        user.save()
        profile = UserProfile(user=user, bio=bio)
        profile.save()
        return user

def add_page(topic, title, body, author, views=0, likes=0):
    (p, valid) = Page.objects.get_or_create(topic=topic, title=title)
    if valid:
        p.views = views
        p.likes =  likes
        p.body = body
        p.author = author
        p.save()
    return p

def add_top(name, description, views=0, likes=0):
    (t,invalid) = Topic.objects.get_or_create(name=name)
    if not invalid:
        t.likes =likes
        t.views = views
        t.description = description
        t.save()
    return t

if __name__ == '__main__':
    print('Starting population script...')
    populate()