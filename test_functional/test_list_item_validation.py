from base import TestFunctional


class TestItemValidation(TestFunctional):
    
    
    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries
        # to submit an empty list item. She hits Enter on the empty list
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('\n')
        
        # The home page refreshes, and there is an error saying
        # that list item cannot be blank
        error = self.browser.find_element_by_css_selector('.text-danger')
        assert error.text == "You can't have an empty list item"
        
        # She tries again with some text for the item, and it works
        self.get_item_input_box().send_keys('Buy milk\n')
        self.check_for_row_in_list_table('1: Buy milk')
        
        # Perversely, she now tries to submit a second blank list item
        self.get_item_input_box().send_keys('\n')
        
        # She receives a similar warning on the list page
        self.check_for_row_in_list_table('1: Buy milk')
        error = self.browser.find_element_by_css_selector('.text-danger')
        assert error.text == "You can't have an empty list item"
        
        # And she can correct it by filling some text in
        self.get_item_input_box().send_keys('Make tea\n')
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')