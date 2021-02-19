## DJANGO LK PROTECC


### Plugging in django-lk-protecc into your application
You'll need to include a few important items in your settings.py
1. `contains_fraud` - function that takes a request as a parameter and returns a boolean
2. `ALLOWED_STRIKES` - an int that determines how many strikes an ip address can have
3. Cloudflare information
    - the request: POST accounts/:account_identifier/rules/lists/:list_id/items
    - for cloudflare you'll need the `ACCOUNT_IDENTIFIER` and your `LIST_ID`
    - for authentication you'll need your `CL_AUTH_EMAIL` and your `CL_AUTH_KEY`
4. `ADMIN_EMAIL` - a string of the email that will receive alerts about fraud

To keep track of a view's fraudulent behavior include the following decorator
- reference: https://docs.djangoproject.com/en/3.1/ref/utils/#django.utils.decorators.decorator_from_middleware
```
@decorator_from_middleware(<path to protecc's middleware class>)
your_view()
```