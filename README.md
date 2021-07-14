## DJANGO LK PROTECC

### Installation
```
pip install git+https://github.com/lightningkite/django-lk-protecc
                                or
pip install git+ssh://github.com/lightningkite/django-lk-protecc
```

### Plugging in django-lk-protecc into your application
You'll need to include a few important items in your settings.py
1. `contains_fraud` - function that takes a request as a parameter and returns a boolean
2. `ALLOWED_STRIKES` - an int that determines how many strikes an ip address can have
3. Cloudflare information
    - the request: POST accounts/:account_identifier/rules/lists/:list_id/items
    - for cloudflare you'll need the `CL_ACCOUNT_ID` and your `CL_LIST_ID`
    - for authentication you'll need your `CL_AUTH_EMAIL` and your `CL_AUTH_KEY`
4. `ADMIN_EMAIL` - a string of the email that will receive alerts about fraud
5. `SITE_NAME` - a string of the name of your application that will appear in the email

To keep track of a view's fraudulent behavior include the following decorator
- reference: https://docs.djangoproject.com/en/3.1/ref/utils/#django.utils.decorators.decorator_from_middleware
```
@decorator_from_middleware(<path to protecc's middleware class>)
your_view()
```
- there are two middleware classes available
    - ProteccFraudViewMiddleware
        - this uses process_view() which will fire off before the view is called
            - this is useful if you want to use the view's arguments
    - ProteccFraudRequestMiddleware
        - this uses process_request() which will purely be passing in the request and its contents

### Developing in the package
- to run tests run `tox`
- to make migrations run `python dev_make_migrations.py`


### Getting your information
- it is likely that you are a normal human being and you do not know how to get arbitrary information from cloud flare. Turns out that cloudflare is one of the least friendly websites to navigate!
- here's some steps I found useful:
how to get your account id (`CL_ACCOUNT_ID`): 
- go to the home page https://dash.cloudflare.com/
- click on your account (listed as emails)
- click on workers under the home section
- your account id will be on the right 

how to get your api key (`CL_AUTH_KEY`):
https://dash.cloudflare.com/profile/api-tokens
- go to the api KEYS section, there will probably be a token section too, do NOT use that one
