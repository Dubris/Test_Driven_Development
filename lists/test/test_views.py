from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import escape

from lists.models import Item, List
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


class TestListView(TestCase):


    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other item list 1', list=other_list)
        Item.objects.create(text='other item list 2', list=other_list)
        
        response = self.client.get('/lists/%d/' % (correct_list.id))
        
        self.assertContains (response, "itemey 1")
        self.assertContains (response, "itemey 2")
        self.assertNotContains (response, "other item list 1")
        self.assertNotContains (response, "other item list 2")


    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertTemplateUsed(response, 'list.html')
        
        
    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        assert response.context['list'] == correct_list
        

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        self.client.post('/lists/%d/' % (correct_list.id,),
        data = {'item_text': 'A new item for an existing list'}
        )

        assert Item.objects.count() == 1
        new_item = Item.objects.first()
        assert new_item.text == 'A new item for an existing list'
        assert new_item.list == correct_list


    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        response = self.client.post('/lists/%d/' % (correct_list.id,),
        data = {'item_text': 'A new item for an existing list'}
        )
        self.assertRedirects(response, 'lists/%d/' % (correct_list.id,))
        
        
    def test_validation_errors_end_up_on_lists_page(self):
        list_=List.objects.create()
        response = self.client.post('/lists/%d/' % (list_.id,), data={'item_text': ''})
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'list.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)


class TestNewList(TestCase):


    def test_saving_a_POST_request(self):
        self.client.post('/lists/new',
        data={'item_text': 'A new list item'}
        )
        
        assert Item.objects.count() == 1
        new_item = Item.objects.first()
        assert new_item.text == 'A new list item'


    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new',
        data={'item_text': "A new list item"}
        )
        new_list = List.objects.first()

        assert response.status_code == 302
        self.assertRedirects(response, '/lists/%d/' % (new_list.id))
        
    
    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data={'item_text': ''})
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)
        
    def test_invalid_list_items_arent_saved(self):
        response = self.client.post('/lists/new', data={'item_text': ''})
        assert List.objects.count() == 0
        assert Item.objects.count() == 0
        