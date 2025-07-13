from importlib import import_module


def get_serializer_class(model_name):
    """
    The model name need to be as is from the view
    any alteration breaks its and it returns none
    which we dont want
    """
    try:
        mod = import_module("professions.professions_reader.serializers")
        return getattr(mod, f"{model_name}Serializer")
    except (ModuleNotFoundError, AttributeError):
        return None
