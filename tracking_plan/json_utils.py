def parse_json_property(name, property_json, required=[]):
    p_types = property_json.get('type')
    if not isinstance(p_types, (list,)):
        p_types = [p_types] #sometimes this is not a list, just make it one
    p = {
        'name': name,
        'description': property_json.get('description'),
        'type': p_types[0]
    }
    allow_null = len(p_types) > 1 and p_types[1] == 'null'
    if allow_null:
        p['allowNull'] = True
    if name in required:
        p['required'] = True

    return p

def parse_json_event(event_json):
    event_labels = event_json.get('rules').get('labels')
    event_area = event_labels.get('area')
    event_product = event_labels.get('product')

    event_obj = {
        'name': event_json.get('name'),
        'description': event_json.get('description'),
        'area': event_area
    }
    if event_product:
        event_obj['product'] = event_product

    properties = (event_json.get('rules')
                    .get('properties')
                    .get('properties')
                    .get('properties'))

    required = (event_json.get('rules')
                .get('properties')
                .get('properties')
                .get('required', []))

    event_obj_properties = []
    for name, prop in properties.items():
        p = parse_json_property(name, prop, required)
        event_obj_properties.append(p)

    event_obj['properties'] = event_obj_properties

    return event_obj
