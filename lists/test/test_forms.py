from django.test import TestCase

from lists.forms import ItemForm, EMPTY_LIST_ERROR

class TestItemForm(TestCase):
    
    def test_form_renders_item_text_input(self):
        form = ItemForm()
        assert 'placeholder="Enter a to-do item"' in form.as_p()
        assert 'class="form-control input-lg"' in form.as_p()
        
    
    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        assert form.is_valid() is False
        assert form.errors['text'] == [EMPTY_LIST_ERROR]