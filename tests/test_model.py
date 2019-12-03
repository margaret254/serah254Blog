import unittest
from app.models import User,Blog,Quote
class UserTest(unittest.TestCase):
   def setUp(self):
       self.new_user = User(username = 'maggie',email='maggiemwas91@gmail.com',bio='default bio',password='samuelmwangi')
   def test_password_setter(self):
       self.assertTrue(self.new_user.pass_secure is not None)
   def test_no_password_access(self):
       with self.assertTrue(AttributeError):
           self.new_user.pass_secure
   def test_password_verification(self):
       self.assertTrue(self.new_user.verify_password('maggie'))


class QuoteTest(unittest.TestCase):
    '''
    Test Class to test the behaviour of the Quote class
    
    '''

    def setUp(self):

        '''
        Set up method that will run before every
        
        '''
        self.new_quote = Quote(4,'jane', 'amazing deeds are just but gifts')


    def test_instance(self):
        self.assertTrue(isinstance(self.new_quote,Quote))