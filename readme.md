## Potential bug in gevent pywsgi

### Reproduction

```
$ pip install -r requirements.txt
$ python -m example
```

### Result

This minimal example in the repo crashes with a core dump whenever there is any kind of exception thrown in the WSGIServer logic.

The stack overflow looks like this:
https://gist.github.com/LefterisJP/7da6ee215160915de8eddc8c7e181a78

It seems like a logging error that causes a stack overflow and ends up segfaulting the interpreter.

Indeed if in the `start()` function we don't provide the `error_log` argument:

https://github.com/LefterisJP/geventpywsgibug/blob/1bd50adb94c14e5e1eae4d361862c9ff5ac41480/example/api.py#L48-L52

Then we get the expected behaviour:

```$ python -m example
[2019-01-07 11:39:13,157] ERROR in app: Exception on /api/1/test_case [GET]
Traceback (most recent call last):
  File "/home/lefteris/.virtualenvs/wsgicrash/lib/python3.7/site-packages/flask/app.py", line 1612, in full_dispatch_request
    rv = self.dispatch_request()
  File "/home/lefteris/.virtualenvs/wsgicrash/lib/python3.7/site-packages/flask/app.py", line 1598, in dispatch_request
    return self.view_functions[rule.endpoint](**req.view_args)
  File "/home/lefteris/.virtualenvs/wsgicrash/lib/python3.7/site-packages/flask_restful/__init__.py", line 480, in wrapper
    resp = resource(*args, **kwargs)
  File "/home/lefteris/.virtualenvs/wsgicrash/lib/python3.7/site-packages/flask/views.py", line 84, in view
    return self.dispatch_request(*args, **kwargs)
  File "/home/lefteris/.virtualenvs/wsgicrash/lib/python3.7/site-packages/flask_restful/__init__.py", line 595, in dispatch_request
    resp = meth(*args, **kwargs)
  File "/home/lefteris/.virtualenvs/wsgicrash/lib/python3.7/site-packages/webargs/core.py", line 449, in wrapper
    return func(*args, **kwargs)
  File "/home/lefteris/w/pythonbug_reproduction/example/v1/resources.py", line 24, in get
    return self.rest_api.test_case(**kwargs)
  File "/home/lefteris/w/pythonbug_reproduction/example/api.py", line 66, in test_case
    raise ValueError('This will trigger stack overflow error and segfault python interpreter')
ValueError: This will trigger stack overflow error and segfault python interpreter
127.0.0.1 - - [2019-01-07 11:39:13] "GET /api/1/test_case HTTP/1.1" 500 164 0.001653
Finished succesfully
```

