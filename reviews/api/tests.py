import json
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from rest_framework.authtoken.models import Token
from api.models import CustomUser, Company, Review, Reviewer
from api.apps import ApiConfig


USER_MODEL = get_user_model()


class CustomUserTestCase(TestCase):
    """
    Tests related to CustomUser Model.
    """

    fixtures = ['testcase_customuser.json']

    def test_model(self):
        """
        User Model must be CustomUser.
        """
        self.assertEqual(USER_MODEL, CustomUser)

    def test_created_token(self):
        """
        When a new CustomUser is created, a token must be created and
        associated to the user.
        """
        user = USER_MODEL.objects.get(username='adam')
        self.assertIsInstance(user.auth_token, Token)


class ApiConfigTestCase(TestCase):
    """
    Tests related to ApiConfig class.
    """

    def test_name(self):
        """
        Check the name of the app.
        """
        self.assertEqual(ApiConfig.name, 'api')


class ReviewerModelTestCase(TestCase):
    """
    Tests related to Reviewer Model.
    """

    fixtures = ['testcase_reviewer_model.json']

    def test_str(self):
        """
        Check the string representation of an object.
        """
        reviewer = Reviewer.objects.get(pk=1)
        self.assertEqual(str(reviewer), 'adam')


class CompanyModelTestCase(TestCase):
    """
    Tests related to Company Model.
    """

    fixtures = ['testcase_company_model.json']

    def test_str(self):
        """
        Check the string representation of an object.
        """
        reviewer = Company.objects.get(pk=1)
        self.assertEqual(str(reviewer), 'Company 1')


class ReviewModelTestCase(TestCase):
    """
    Tests related to Review Model.
    """

    fixtures = ['testcase_review_model.json']

    def test_str(self):
        """
        Check the string representation of an object.
        """
        reviewer = Review.objects.get(pk=1)
        self.assertEqual(str(reviewer), 'adam - Company 1')


class APITestCase(TestCase):
    """
    Tests related to the API.
    """

    fixtures = ['testcase_api.json']

    def test_get_token_sucess(self):
        """
        When provided valid username and password, the View must returns the
        User's Auth Token.
        """
        url = '/api-token-auth/'
        data = {'username': 'adam', 'password': '123'}

        response = Client().post(url, data)
        self.assertEqual(response.status_code, 200)

        # Check if the returned token is the same of User's Token.
        content = json.loads(response.content)
        user = USER_MODEL.objects.get(username='adam')
        self.assertEqual(content['token'], user.auth_token.key)

    def test_get_token_failure(self):
        """
        When provided invalid username and password, the View must returns the
        User's Auth Token.
        """
        url = '/api-token-auth/'
        data = {'username': 'adam', 'password': '321'}

        response = Client().post(url, data)
        self.assertEqual(response.status_code, 400)


class ReviewAPITestCase(TestCase):
    """
    Tests related to the API of Review Model.
    """

    fixtures = ['testcase_review_api.json']

    def test_get_without_token(self):
        """
        When the token information is not passed, the view must return 401
        status code.
        """
        client = Client()
        response = client.get('/reviews/')
        self.assertEqual(response.status_code, 401)

    def test_post_without_token(self):
        """
        When the token information is not passed, the view must return 401
        status code.
        """
        client = Client()
        data = {
            'rating': '1',
            'title': 'Hated It!',
            'summary': 'A little text to say that I hated it!',
            'company': '1'
        }
        response = client.post('/reviews/', data)
        self.assertEqual(response.status_code, 401)

    def test_get_all_reviews_user_1_review(self):
        """
        A user is able to see only your own Reviews.
        """
        # Get the User's Auth Token.
        url = '/api-token-auth/'
        data = {'username': 'adam', 'password': '123'}
        response = Client().post(url, data)
        content = json.loads(response.content)
        user_token = content['token']

        # Prepare the header with the client's token.
        http_authorization = 'Token %s' % user_token
        client = Client(HTTP_AUTHORIZATION=http_authorization)

        # GET the Reviews.
        response = client.get('/reviews/')
        self.assertEqual(response.status_code, 200)

        # Check if only reviews related to the user were retrieved.
        content = json.loads(response.content)
        expected = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': 1,
                    'rating': 5,
                    'title': 'Loved it!',
                    'summary': 'I loved it! Pretty good!',
                    'submission_date': '2020-10-12',
                    'ip_address': '127.0.0.1',
                    'reviewer': 1,
                    'company': 1
                },
            ]
        }
        self.assertDictEqual(content, expected)

    def test_get_all_reviews_user_2_reviews(self):
        """
        A user is able to see only your own Reviews.
        """
        # Get the User's Auth Token.
        url = '/api-token-auth/'
        data = {'username': 'carlos', 'password': '123'}
        response = Client().post(url, data)
        content = json.loads(response.content)
        user_token = content['token']

        # Prepare the header with the client's token.
        http_authorization = 'Token %s' % user_token
        client = Client(HTTP_AUTHORIZATION=http_authorization)

        # GET the Reviews.
        response = client.get('/reviews/')
        self.assertEqual(response.status_code, 200)

        # Check if only reviews related to the user were retrieved.
        content = json.loads(response.content)
        expected = {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': 2,
                    'rating': 3,
                    'title': 'Could be better',
                    'summary': 'I am a little disappointed',
                    'submission_date': '2020-10-12',
                    'ip_address': '127.0.0.1',
                    'reviewer': 2,
                    'company': 1
                },
                {
                    'id': 3,
                    'rating': 2,
                    "title": "Not good",
                    "summary": "I won't buy again!",
                    'submission_date': '2020-10-12',
                    'ip_address': '127.0.0.1',
                    'reviewer': 2,
                    'company': 2
                }
            ]
        }
        self.assertDictEqual(content, expected)

    def test_get_all_reviews_user_0_reviews(self):
        """
        A user is able to see only your own Reviews.
        """
        # Get the User's Auth Token.
        url = '/api-token-auth/'
        data = {'username': 'mary', 'password': '123'}
        response = Client().post(url, data)
        content = json.loads(response.content)
        user_token = content['token']

        # Prepare the header with the client's token.
        http_authorization = 'Token %s' % user_token
        client = Client(HTTP_AUTHORIZATION=http_authorization)

        # GET the Reviews.
        response = client.get('/reviews/')
        self.assertEqual(response.status_code, 200)

        # Check if only reviews related to the user were retrieved.
        content = json.loads(response.content)
        expected = {
            'count': 0,
            'next': None,
            'previous': None,
            'results': []
        }
        self.assertDictEqual(content, expected)

    def test_get_specific_review_sucess(self):
        """
        When a user is request data about his own review, the request must
        return the data.
        """
        # Get the User's Auth Token.
        url = '/api-token-auth/'
        data = {'username': 'adam', 'password': '123'}
        response = Client().post(url, data)
        content = json.loads(response.content)
        user_token = content['token']

        # Prepare the header with the client's token.
        http_authorization = 'Token %s' % user_token
        client = Client(HTTP_AUTHORIZATION=http_authorization)

        # GET the Reviews.
        response = client.get('/reviews/1/')
        self.assertEqual(response.status_code, 200)

        # Check if only reviews related to the user were retrieved.
        content = json.loads(response.content)
        expected = {
            'id': 1,
            'rating': 5,
            'title': 'Loved it!',
            'summary': 'I loved it! Pretty good!',
            'submission_date': '2020-10-12',
            'ip_address': '127.0.0.1',
            'reviewer': 1,
            'company': 1
        }
        self.assertDictEqual(content, expected)

    def test_get_specific_review_failure(self):
        """
        When a user is request data about his own review, the request must
        NOT return the data.
        """
        # Get the User's Auth Token.
        url = '/api-token-auth/'
        data = {'username': 'adam', 'password': '123'}
        response = Client().post(url, data)
        content = json.loads(response.content)
        user_token = content['token']

        # Prepare the header with the client's token.
        http_authorization = 'Token %s' % user_token
        client = Client(HTTP_AUTHORIZATION=http_authorization)

        # GET the Reviews.
        response = client.get('/reviews/2/')
        self.assertEqual(response.status_code, 404)

    def test_post(self):
        """
        When a POST is sent, the server must create a new Review record.
        """
        # Get the User's Auth Token.
        url = '/api-token-auth/'
        data = {'username': 'adam', 'password': '123'}
        response = Client().post(url, data)
        content = json.loads(response.content)
        user_token = content['token']

        # Prepare the header of client with the token.
        http_authorization = 'Token %s' % user_token
        client = Client(
            HTTP_AUTHORIZATION=http_authorization,
            REMOTE_ADDR="200.0.0.1"
        )

        # Prepare data.
        url = '/reviews/'
        data = {
            'rating': '1',
            'title': 'Hated It!',
            'summary': 'A little text to say that I hated it!',
            'company': '1'
        }

        # Before POST the data, check that there isn't any review with the same
        # data.
        self.assertFalse(Review.objects.filter(**data).exists())

        # POST the data.
        response = client.post(url, data)
        self.assertEqual(response.status_code, 201)

        # Check if Review was created with the passed data.
        self.assertTrue(Review.objects.filter(**data).exists())

        # Check if reviewer and ip_address were correctly assigned.
        review = Review.objects.get(**data)
        expected_reviewer = Reviewer.objects.get(user__username='adam')
        self.assertEqual(review.reviewer, expected_reviewer)
        self.assertEqual(review.ip_address, '200.0.0.1')

    def test_post_ip_x_forwarded_for(self):
        """
        When a POST is sent, the server must create a new Review record.
        Tests if IP wil be saved correctly when the information is in
        HTTP_X_FORWARDED_FOR.
        """
        # Get the User's Auth Token.
        url = '/api-token-auth/'
        data = {'username': 'adam', 'password': '123'}
        response = Client().post(url, data)
        content = json.loads(response.content)
        user_token = content['token']

        # Prepare the header of client with the token.
        http_authorization = 'Token %s' % user_token
        client = Client(
            HTTP_AUTHORIZATION=http_authorization,
            HTTP_X_FORWARDED_FOR="200.0.0.2"
        )

        # Prepare data.
        url = '/reviews/'
        data = {
            'rating': '1',
            'title': 'Hated It!',
            'summary': 'A little text to say that I hated it!',
            'company': '1'
        }

        # Before POST the data, check that there isn't any review with the same
        # data.
        self.assertFalse(Review.objects.filter(**data).exists())

        # POST the data.
        response = client.post(url, data)
        self.assertEqual(response.status_code, 201)

        # Check if Review was created with the passed data.
        self.assertTrue(Review.objects.filter(**data).exists())

        # Check if reviewer and ip_address were correctly assigned.
        review = Review.objects.get(**data)
        expected_reviewer = Reviewer.objects.get(user__username='adam')
        self.assertEqual(review.reviewer, expected_reviewer)
        self.assertEqual(review.ip_address, '200.0.0.2')
