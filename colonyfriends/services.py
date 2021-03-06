from typing import List

from django.db.models import Q

from colonyfriends.models import Person


def get_common_friends(people: List[Person], eye_colour_filter=None, has_died_filter=None):
    """Get Common Friends Given a List of Person. Additional Filters are available to use if you wish. Eye Colour and Has Died

    Keyword arguments:
    people -- Must be a list of more than 1 of type models.Person
    eye_colour_filter -- E.g. blue (default None)
    has_died_filter -- E.g 1 (default None)
    """

    assert len(people) > 1

    eye_colour_query = Q()
    if eye_colour_filter:
        eye_colour_query = Q(eye_colour=eye_colour_filter)

    has_died_query = Q()
    if has_died_filter is not None:
        has_died_query = Q(has_died=has_died_filter)

    first_query = people.pop().friends.filter(eye_colour_query & has_died_query)

    friends_intersection = []
    for p in people:
        friends_intersection.append(
            p.friends.filter(eye_colour_query & has_died_query)
        )

    return first_query.intersection(*friends_intersection)