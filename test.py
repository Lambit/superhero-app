from app import app
from unittest import TestCase



class ViewsTestCase(TestCase):
    """
    Test the routes of app.
    """
    # root route
    def test_route_direct(self):
        with app.test_client() as client:
            res =client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("<h1 class='display-4'>Find A Hero</h1>", html)

    # register
    def test_register(self):
        with app.test_client() as client:
            res = client.get('/register')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("<h1 class='display-3'>Sign Up</h1>", html) 

    # login
    def test_login(self):
        with app.test_client() as client:
            res = client.get('/login')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("<h1 class='display-3'>Login</h1>", html)

    #superheros
    def test_superheros(self):
        with app.test_client() as client:
            res = client.get('/superheros')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("<h1 class='display-4'>Find A Hero</h1>", html)

    # favorites
    def test_favorites(self):
        with app.test_client() as client:
            res = client.get('/favorites')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("<h1 class= 'display-3'>Favorites</h1>", html)          
    



