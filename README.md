# reviews

This is a project of a simple API that allows users to post and retrieve their reviews.
It was built using Django and django-rest-framework.

<hr />

## How to setup the project

1. Download the project:

    ```sh
    $ git clone https://github.com/matheusdemicheli/reviews.git reviews
    ```

2. [Create a virtual environment](https://docs.python.org/3/library/venv.html) and install the requirements:

    ```sh
    $ pip install -r requirements.txt
    ```

3. Define environment variables

    You must define REVIEWS_SECRET_KEY in your environment with any value to be used inplace of Django SECRET_KEY variable:

    ```sh
    $ export REVIEWS_SECRET_KEY=1234567890
    ```

    Also, REVIEWS_DEBUG can be defined optionally to be used inplace of Django DEBUG variable (default value is False):

    ```sh
    $ export REVIEWS_DEBUG=True
    ```

4. Go to reviews/reviews and run migrations:

    ```sh
    $ cd reviews/reviews
    $ ./manage.py migrate
    ```

5. Load test data (optional)

    ```sh
    $ ./manage.py loaddata test_data.json
    ```

    This will create some Users, Tokens, Reviewers and Reviews into the database (SQLite by default). <br>
    The following users will be created:

    | Username | Password | Super User |
    | ------ | ------ | ------ |
    | admin | admin | yes |
    | john | 123 | no |
    | mary | 321 | no |
    | carlos | 123 | no |

6. Start the Django development environment:

    ```sh
    $ ./manage.py runserver 0:8000
    ```

<hr />

## List of Availables URLs

The API only accepts requests using GET and POST methods. Here is all available URLs and the description for each method.

### POST

* **/api-token-auth/** <br>
Returns the User's Auth Token if username and password are correct. The Auth Token is essencial once the API uses it to confirm the authentication of an user. This token must be sent in the header of every request.

    | Parameter | Type | Required | Description |
    | ------ | ------ | ------ | ------ |
    | username | str | yes | Username for login |
    | password | str | yes | Password for login |


* **/reviews/** <br>
Creates a Review for the logged user.

    | Parameter | Type | Required | Description |
    | ------ | ------ | ------ | ------ |
    | rating | int | yes | Rating of the Review. Possible values are: 1, 2, 3, 4 or 5 |
    | title | str | yes | Title of the Review |
    | summary | str | yes | Summary of the Review |
    | company | int | yes | Company's primary key |


### GET

* **/reviews/** <br>
Retrieve all reviews of the logged user

* **/reviews/[id]/** <br>
Retrieve one specific review only if that review was sent by the logged user

**Besides these URLs, there is /admin/ which a superuser can access and see all the reviews of any user.**

 <hr />

## Practical Example

Here is a example in Python and Shell of how to use this project.

### 1. Getting the User's Auth Token.

```sh
# Shell

curl --location --request POST 'http://localhost:8000/api-token-auth/' \
--form 'username=mary' \
--form 'password=321'
```

```py
# Python

import json
import requests

url = "http://localhost:8000/api-token-auth/"

payload = {
    'username': 'mary',
    'password': '321'
}
response = requests.request("POST", url, data=payload)
token = json.loads(reponse.content)['token']
```

### 2. Posting a Review.

Lets assume that the Auth Token obtained in last step is equals to b007232d5762fec21602dffea8cbfa10d8330393.

```sh
# Shell

curl --location --request POST 'http://localhost:8000/reviews/' \
--header 'Authorization: Token b007232d5762fec21602dffea8cbfa10d8330393' \
--form 'rating=1' \
--form 'title=Hated it!' \
--form 'summary=A little text to say that I hated it!' \
--form 'company=1'
```

```py
url = "http://localhost:8000/reviews/"

payload = {
    'rating': '1',
    'title': 'Hated it!',
    'summary': 'A little text to say that I hated it!',
    'company': '1'
}
headers = {
  'Authorization': 'Token b007232d5762fec21602dffea8cbfa10d8330393'
}
response = requests.request("POST", url, headers=headers, data=payload)
```

### 3. Seeing all User's Review.

```sh
# Shell

curl --location --request GET 'http://localhost:8000/reviews/' \
--header 'Authorization: Token b007232d5762fec21602dffea8cbfa10d8330393' \
```

```py
# Python

url = "http://localhost:8000/reviews/"

headers = {
  'Authorization': 'Token b007232d5762fec21602dffea8cbfa10d8330393'
}
response = requests.request("GET", url, headers=headers)
```

### 4. Seeing a Specific Review.

To see a specific review, the id of review must be passed at URL. The API will retrieve the information only if the logged user (represented by the token) is the same of the Review's creator.

```sh
# Shell

curl --location --request GET 'http://localhost:8000/reviews/1/' \
--header 'Authorization: Token b007232d5762fec21602dffea8cbfa10d8330393' \
```

```py
# Python

url = "http://localhost:8000/reviews/1/"

headers = {
  'Authorization': 'Token b007232d5762fec21602dffea8cbfa10d8330393'
}
response = requests.request("GET", url, headers=headers)
```
