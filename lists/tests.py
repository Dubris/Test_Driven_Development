from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.models import Item
from lists.views import home_page
import pytest


def test_root_url_resolves_to_home_page_view():
    found = resolve('/')
    assert found.func == home_page


def test_home_page_returns_correct_html():
    request = HttpRequest()

    response = home_page(request)
    expected_html = render_to_string('home.html')

    assert expected_html == response.content.decode()


def test_home_page_can_save_a_POST_request():
    request = HttpRequest()
    request.method = 'POST'
    request.POST['item_text'] = 'A new list item'

    response = home_page(request)
    expected_html = render_to_string('home.html', {'new_item_text': 'A new list item'})

    assert 'A new list item' in response.content.decode()
    assert expected_html == response.content.decode()
    
def test_saving_and_retrieving_items():
    first_item = Item()
    first_item.text = 'The first (ever) list item'
    first_item.save()

    second_item = Item()
    second_item.text = 'Item the second'
    second_item.save()
    
    saved_items = Item.objects.all()
    assert saved_items.count() == 2
    
    first_saved_item = saved_items[0]
    second_saved_item = saved_items[1]
    assert first_saved_item.text == 'The first (ever) list item'
    assert second_saved_item.text == 'Item the second'