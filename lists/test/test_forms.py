from django.test import TestCase

from lists.forms import (
    ItemForm, ExistingListItemForm,
    EMPTY_LIST_ERROR, DUPLICATE_ITEM_ERROR
    )
from lists.models import Item, List


class TestItemForm(TestCase):

    def test_form_renders_item_text_input(self):
        form = ItemForm()
        assert 'placeholder="Enter a to-do item"' in form.as_p()
        assert 'class="form-control input-lg"' in form.as_p()

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        assert form.is_valid() is False
        assert form.errors['text'] == [EMPTY_LIST_ERROR]

    def test_form_save_handles_saving_to_a_list(self):
        list_ = List.objects.create()
        form = ItemForm({'text': 'do me'})
        new_item = form.save(for_list=list_)
        assert new_item == Item.objects.first()
        assert new_item.text == 'do me'
        assert new_item.list == list_


class ExistingListItemFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_)
        assert 'placeholder="Enter a to-do item"' in form.as_p()

    def test_form_validation_for_blank_items(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': ''})
        assert form.is_valid() is False
        assert form.errors['text'] == [EMPTY_LIST_ERROR]

    def test_form_validation_for_duplicate_items(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='no twins!')
        form = ExistingListItemForm(for_list=list_, data={'text': 'no twins!'})
        assert form.is_valid() is False
        assert form.errors['text'] == [DUPLICATE_ITEM_ERROR]

    def test_form_save(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': 'hi'})
        new_item = form.save()
        assert new_item == Item.objects.all()[0]
