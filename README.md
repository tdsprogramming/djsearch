# djsearch

This is a pluggable app to add a search feature to your Django project.

## How to Use
1. First, you need to include the `djsearch.urls` in your main project `urls.py`.

```
import djsearch

...

urlpatterns = [
    ...
    path('search/', include('djsearch.urls'))
    ...
]
```
This will enable you to use the API for queries structured as
`localhost:8000/search/?q=myquery`.

2. You will need to specify in your models that you want searched as an attribute in your model object called `djsearch_fields`.

You will then need to define a `djresult_output` which will end up sending the list of the fields you specify in your model.

For example:

```python
class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    djsearch_fields = [
        'first_name',
        'last_name'
    ]

    djresult_output = {
        'fields': [
            'first_name',
            'last_name'
        ]
    }

    def __str__(self):
        return "{}, {}".format(self.last_name, self.first_name)

    def get_absolute_url(self):
        return reverse('persons:detail', args=[self.pk])

```

If you have an entry in your database of "John Smith", you can visit `localhost:8000/search/?q=smith` and you will receive the following JsonResponse:

```json
    {
        "results": {
            "Smith, John": {
                "link": "/persons/detail/1/",
                "fields": {
                    "first_name": "John",
                    "last_name": "Smith"
                }
            }
        }
    }
```

3. By default, the link will be defined by your model's `get_absolute_url` method, if defined, unless you define `link` in your `djresult_output`, by doing the following:

```python
djresult_output = {
    'link': 'some/other/link/',
    'fields':[
        ...
    ]
}
```
You can use the link as the `href` attribute in your search results page for each search result.

If neither `djresult_output['link']` or `get_absolute_url` is defined, the `djresult_output['link']` will return as an empty string.
