# Fruity Nutters food cooperative

This is an old, old project, running on the Django framework (started in 2008 just as Django version 1.0 dropped!), so it's quite crusty. But it has handled each member's individual food order, and makes it marginally easier for the sterling team of volunteers to collate and submit the massive collective order that results.

I've updated it to the most recent version of Django, so it's a little easier to maintain, and worked out a few of the most egregious kinks (though I'm sure there's still many horrors within).

So, if you want to run a food coop in _exactly the same way_ we do, then this is the old, crusty codebase for you!


## Custom settings

```python
# Email address to send order email from.
ORDER_FORM_SEND_EMAIL = 'mailbot@example.com'

# Email address to set reply_to header to for sent email (set to
# ORDER_FORM_SEND_EMAIL if same).
ORDER_FORM_REPLY_TO_EMAIL = 'friendly_volunteer@example.com'
```
