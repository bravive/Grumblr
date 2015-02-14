from django.test import TestCase
from models import *

# Create your tests here.
class AddCommentModelsTest(TestCase):
    # Seeds the test database with data we obtained
    fixtures = ['grumblr']  # from python manage.py dumpdata
    
    
    def test_add_item(self):    # Tests the to-do list add-item function.
        #client = Client()       # add-item expects a POST request with one
        self.assertTrue(Grumbls.objects.all().count() > 0)

        # query parameter, item, the text of the to-do
        # list item.
        # Grumblr.objects.all()
        #sample_item = 'This is the comment for my grumblr'
        #response = client.post('/grumblrApp/addcomment/1/1', {'item':sample_item})
#self.assertTrue(response.content.find(sample_item) >= 0)


