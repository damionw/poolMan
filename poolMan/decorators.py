#==============================================================================
#                             Global Imports
#==============================================================================
from functools import wraps

import logging

#==============================================================================
#                                Logging
#==============================================================================
LOG = logging.getLogger(__name__)

#==============================================================================
#                            Decorators
#==============================================================================
def cast(type_reference):
    """ Cast the passed in value to the specified type """
    def cast_decorator(call_reference):
        @wraps(call_reference)
        def cast_wrapper(*args, **kwargs):
            return type_reference(call_reference(*args, **kwargs))

        return cast_wrapper

    return cast_decorator

def cached(function_reference):
    """ Allows caching of object method return values

        Note: Since it stores the cached values in an object's context,
              it is only valid when used on object methods
    """

    @wraps(function_reference)
    def wrapper(object_reference, *args, **kwargs):
        """ Wrap a cacheable method

            Ensures that iterable contents are turned into a list
            before caching.

            NOTE: There is currently no nice way to invalidate the
                  cache, other than removing the specific key from
                  object_reference._cached_method_results[]
        """
        method_name = function_reference.__name__
        instance_id = id(wrapper)

        if not hasattr(object_reference, "_cached_method_results"):
            object_reference._cached_method_results = dict()

        if instance_id not in object_reference._cached_method_results:
            cached_value = function_reference(object_reference, *args, **kwargs)

            # Handle generator case by consuming all of the data
            if hasattr(cached_value, 'next') or hasattr(cached_value, '__next__'):
                cached_value=list(cached_value)

            #LOG.debug("Storing results for method {method_name}, id {instance_id}".format(method_name=method_name, instance_id=instance_id))
            object_reference._cached_method_results[instance_id] = cached_value
        else:
            #LOG.debug("Using cached results for method {method_name}, id {instance_id}".format(method_name=method_name, instance_id=instance_id))
            cached_value = object_reference._cached_method_results[instance_id]

        return cached_value

    return wrapper

def subscripted(function_reference):
    @wraps(function_reference)
    def wrapper(obj, *args, **kwargs):
        class subscripter(object):
            def __getitem__(self, key):
                return function_reference(obj, key)

        return subscripter()

    return property(wrapper)
