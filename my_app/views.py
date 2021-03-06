import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from requests.compat import quote_plus
from . import models
import calendar

BASE_CRAIGSLIST_URL = 'https://indore.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


def home(request):
    return render(request, 'base.html')

def create_calendar(request):
    if request.method=='POST':
        year = request.POST.get('year')
        month = request.POST.get('month')
        #print("quantity here:-",search)
        old_calendar_array=calendar.monthcalendar(int(year),int(month))
        calendar_array=[]
        for i in old_calendar_array:
            temp=[]
            for j in i:
                if j==0:
                    temp.append('')
                else:temp.append(str(j))
            calendar_array.append(temp)
        stuff_for_frontend ={
            'calendar_array':calendar_array,
        }
        return render(request, 'my_app/calendar.html',stuff_for_frontend)
    return render(request, 'my_app/search_calendar.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find_all('li', {'class': 'result-row'})

    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'

        final_postings.append((post_title, post_url, post_price, post_image_url))

    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
    }

    return render(request, 'my_app/new_search.html', stuff_for_frontend)

# import requests
# from django.shortcuts import render
# from bs4 import BeautifulSoup
# from requests.compat import quote_plus
# from . import models
# # Create your views here.

# BASE_CRAIGSLIST_URL = 'https://losangeles.craigslist.org/search/?query={}'
# BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

# def home(request):
#     return render(request,'base.html')

# def new_search(request):
#     # when someone posts the content in search bar
#     search = request.POST.get('search')
#     models.Search.objects.create(search=search)
#     #print(search)
#     #print(quote_plus(search))
#     final_url=BASE_CRAIGSLIST_URL.format(quote_plus(search))
#     #print(final_url)
#     #response=requests.get("https://indore.craigslist.org/d/services/search/bbb?query=food&sort=rel")
#     response=requests.get(final_url)
#     data=response.text
#     #print(data)
#     soup=BeautifulSoup(data,features='html.parser')
#     #print(soup)
#     # post_titles=soup.find_all('a',{'class':'result-title'})
#     # print(post_titles[0].text)
#     post_listings= soup.find_all('a',{'class':'result-row'})
#     final_postings=[]
#     for post in post_listings:
#         post_title=post.find(class_='result-title').text
#         post_url=post.find('a').get('href')
#         if post.find(class_='result-price'):
#             post_price=post.find(class_='result-price').text
#             print(post_price)
#         else:post_price='N/A'

#         if post.find(class_='result-image').get('data-ids'):
#             post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
#             post_image_url = BASE_IMAGE_URL.format(post_image_id)
#             print(post_image_url)
#         else:
#             post_image_url= 'https://craigslist.org/images/peace.jpg'
#         final_postings.append((post_title,post_url,post_price,post_image_url))
#     print(final_postings)
#     stuff_for_frontend={
#         'search':search,
#         'final_postings':final_postings,
#     }
#     return render(request,'my_app/new_search.html',stuff_for_frontend)