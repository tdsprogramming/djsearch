def django_search_serializer(obj):
    if 'link' in obj.djresult_output.keys():
        link = obj.djresult_output['link']
    else:
        try:
            link = obj.get_absolute_url()
        except:
            link = ''

    serialized_data = {
        'link': link,
        'fields': {}
    }
    
    for f in obj.djresult_output['fields']:
        serialized_data['fields'][f] = obj.__dict__[f]
    return serialized_data
