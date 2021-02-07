from exceptions import GenericException, APIException


def compute_profile_link():
    return ''


def compute_boolean(bool_str: str) -> bool:
    return bool_str.lower() == 'yes'


def compute_int(int_str: str) -> int:
    return int(int_str)


def query_model(model, id=None):
    try:
        if id is not None:
            result = model.query.get(id)
        else:
            result = model.query.order_by('id').all()

        if not result:
            raise APIException("Resource Not Found", 404)
        
        return result

    except:
        raise APIException("Resource Not Found", 404)


def search_by_name_pattern(model, search_term):
    search = "%{}%".format(search_term.lower())
    matching_by_name_list = model.query.filter(model.name.ilike(search)).order_by('id').all()
    matching_by_description_list = model.query.filter(model.seeking_description.ilike(search)).order_by('id').all()
    matching_list = list(set(matching_by_name_list + matching_by_description_list))

    if not matching_list:
        raise APIException("Resource Not Found", 404)
    
    return matching_list
