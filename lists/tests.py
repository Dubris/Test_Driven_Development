from django.test import SimpleTestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.models import Item
from lists.views import home_page

import pytest

class TestHomePage():


    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        assert found.func == home_page

        
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()

        response = home_page(request)
        expected_html = render_to_string('home.html')

        assert expected_html == response.content.decode()


class TestListView():

    simpletestcase = SimpleTestCase()

    def test_home_page_displays_all_list_items(self, client):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')
        
        response = client.get('/lists/the-only-list-in-the-world/')
        
        assert self.simpletestcase.assertContains (response, "itemey 1") is None
        assert self.simpletestcase.assertContains (response, "itemey 2") is None


    def test_uses_list_template(self, client):
        response = client.get('/lists/the-only-list-in-the-world/')
        assert self.simpletestcase.assertTemplateUsed(response, 'list.html') is None


class TestItemModel():


    def test_saving_and_retrieving_items(self):
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
            

class TestNewList():


    simpletestcase = SimpleTestCase()

    def test_saving_a_POST_request(self, client):
        client.post('/lists/new',
        data={'item_text': 'A new list item'}
        )
        
        assert Item.objects.count() == 1
        new_item = Item.objects.first()
        assert new_item.text == 'A new list item'


    def test_redirects_after_POST(self, client):
        response = client.post('/lists/new',
        data={'item_text': "A new list item"}
        )

        assert response.status_code == 302
        assert self.simpletestcase.assertRedirects(
        response, '/lists/the-only-list-in-the-world/'
        ) is None