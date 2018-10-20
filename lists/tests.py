from django.test import SimpleTestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.models import Item, List
from lists.views import home_page

import pytest
import re

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

    def test_displays_only_items_for_that_list(self, client):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other item list 1', list=other_list)
        Item.objects.create(text='other item list 2', list=other_list)
        
        response = client.get('/lists/%d/' % (correct_list.id))
        
        assert self.simpletestcase.assertContains (response, "itemey 1") is None
        assert self.simpletestcase.assertContains (response, "itemey 2") is None
        assert self.simpletestcase.assertNotContains (response, "other item list 1") is None
        assert self.simpletestcase.assertNotContains (response, "other item list 2") is None


    def test_uses_list_template(self, client):
        list_ = List.objects.create()
        response = client.get('/lists/%d/' % (list_.id,))
        assert self.simpletestcase.assertTemplateUsed(response, 'list.html') is None
        
    def test_passes_correct_list_to_template(self, client):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = client.get('/lists/%d/' % (correct_list.id,))
        response.context['list'] == correct_list


class TestListAndItemModel():


    def test_saving_and_retrieving_items(self):
            list_ = List()
            list_.save()
            
            first_item = Item()
            first_item.text = 'The first (ever) list item'
            first_item.list = list_
            first_item.save()

            second_item = Item()
            second_item.text = 'Item the second'
            second_item.list = list_
            second_item.save()
            
            saved_list = List.objects.first()
            assert saved_list == list_
            
            saved_items = Item.objects.all()
            assert saved_items.count() == 2
            
            first_saved_item = saved_items[0]
            second_saved_item = saved_items[1]
            assert first_saved_item.text == 'The first (ever) list item'
            assert first_saved_item.list == list_
            assert second_saved_item.text == 'Item the second'
            assert second_saved_item.list == list_
            

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
        new_list = List.objects.first()

        assert response.status_code == 302
        self.simpletestcase.assertRedirects(
        response, '/lists/%d/' % (new_list.id)
        )


class TestNewItem():

    simpletestcase = SimpleTestCase()

    def test_can_save_a_POST_request_to_an_existing_list(self, client):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        client.post('/lists/%d/add_item' % (correct_list.id,),
        data = {'item_text': 'A new item for an existing list'}
        )

        assert Item.objects.count() == 1
        new_item = Item.objects.first()
        assert new_item.text == 'A new item for an existing list'
        assert new_item.list == correct_list


    def test_redirects_to_list_view(self, client):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        response = client.post('/lists/%d/add_item' % (correct_list.id,),
        data = {'item_text': 'A new item for an existing list'}
        )
        
        assert response.status_code == 302
        self.simpletestcase.assertRedirects(response,
        'lists/%d/' % (correct_list.id, )
        )