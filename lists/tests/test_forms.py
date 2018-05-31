from django.test import TestCase

from lists.forms import EMPTY_ITEM_ERROR, ItemForm


class ItemFormTest(TestCase):

    # Renders ItemForm as HTML input control
    #def test_form_renders_item_text_input(self):
    #    form = ItemForm()
    #    self.fail(form.as_p())

    def test_form_item_input_has_placeholder_and_css_classes(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])
        #print(form)
        #print(form.errors)
        #print(form['text'])
        #print(form['text'].errors)

        # It's trick that you should use 'form.text.errors' in django's
        # template system instead of syntax-correct "form['text'].errors"
        self.assertEqual(form['text'].errors, form.errors['text'])

