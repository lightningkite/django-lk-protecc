## DJANGO LK PROTECC

### Installation
```
pip install git+https://github.com/lightningkite/django-lk-protecc
                                or
pip install git+ssh://github.com/lightningkite/django-lk-protecc
```

### Plugging in django-lk-protecc into your application
You'll need to include a few important items in your settings.py
1. `contains_fraud` - function that takes a request as a parameter and returns a tuple. 
    - You must return a tuple of (boolean, dictionary(nullable)), the boolean represents if the request contains fraud, the dictionary contains optional attributes for the FraudTracker model.
        - example:
        ```
            contains_fraud(request, *args, **kwargs):
                order = args[0]
                return True, {'user_email': order.email}
        ``` 
        or
        ```
            contains_fraud(request, *args, **kwargs):
                return True, None
        ```
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

### Available Models
- FraudTracker
    - fields:
        - user
        - request_url
        - created_at
        - ip_address
        - user_email (this is optional, passed through the optional attrs in `contains_fraud`)
- WhiteListTracker
    - fields
        - user
        - ip_address
        - user_email (optional)

### Getting your information
- It is likely that you are a normal human being and you do not know how to get arbitrary information from cloudflare. Turns out that cloudflare is one of the least friendly websites to navigate!
#### here are some steps I found useful:
how to get your account id (`CL_ACCOUNT_ID`): 
- go to the home page https://dash.cloudflare.com/
- click on your account (listed as emails)
- click on workers under the home section
- your account id will be on the right 

how to get your api key (`CL_AUTH_KEY`):
https://dash.cloudflare.com/profile/api-tokens
- go to the api KEYS section, there will probably be a token section too, do NOT use that one

how to get your list id (`CL_LIST_ID`):
```
curl -X GET "https://api.cloudflare.com/client/v4/accounts/<insert account id here>/rules/lists" \
     -H "X-Auth-Email: <insert your account email here>" \
     -H "X-Auth-Key: <insert your auth key here>" \
     -H "Content-Type: application/json"
 ```
- the problem with the call is that it doesn't use the list name, which it should because that's how they display it, but no, they use this arbitrary number that you have to use an api call to find (at least I couldn't find another way to get it)
- Fire off this call and get the id from the list you want, they should be displayed and it will be easy enough to find the one you want.

You think you got it? Go ahead, test it out:
```
curl -X POST "https://api.cloudflare.com/client/v4/accounts/<account id>/rules/lists/<list id>/items" \
     -H "X-Auth-Email: <account email>" \
     -H "X-Auth-Key: <api key>" \
     -H "Content-Type: application/json" \
     --data '[{"ip":"10.0.0.1","comment":"Private IP address"}]'
```
