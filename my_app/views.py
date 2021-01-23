import requests
from requests.compat import quote_plus
from django.shortcuts import render
from bs4 import BeautifulSoup
from . import models

BASE_URl = 'https://losangeles.craigslist.org/search/?query={}'

BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_URl.format(quote_plus(search))

    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    all_posts = soup.find_all('li', {'class': 'result-row'})
    final_listing = []
    for posts in all_posts:
        post_title = posts.find(class_='result-title').text
        post_url = posts.find('a').get('href')
        post_price = posts.find(class_='result-price').text
        if posts.find(class_='result-price').text:
            post_price = posts.find(class_='result-price').text
        else:
            post_price = 'N/A'
        if posts.find(class_='result-image').get('data-ids'):
            post_image_id = posts.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'
        final_listing.append((post_title, post_url, post_price,post_image_url))
    context = {
        'search': search,
        'final_posting': final_listing,

    }

    return render(request, 'my_app/new_search.html', context)
