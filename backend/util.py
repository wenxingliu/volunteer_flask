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
