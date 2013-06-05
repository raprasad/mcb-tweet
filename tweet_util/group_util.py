from django.contrib.auth.models import Group

def is_user_in_group(request, group_name):
    """
    (1) Pull the Group object by it's name
    (2) Look for the user in the Request object
    (3) Check if the user belongs to the group
    """
    if not (request and request.user):
        return False

    try:
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
            return False

    for user in group.user_set.get_query_set():
        if request.user == user:
            return True

    return False
