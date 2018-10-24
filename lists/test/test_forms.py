from django.test import TestCase

from lists.forms import ItemForm, EMPTY_LIST_ERROR
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