from collections import Counter
from operator import itemgetter

def return_index(request, render):
    """Return the index page with or without the context"""

    #Person.objects.values('optional_first_name').annotate(c=Count('optional_first_name')).order_by('-c')
    if request.user.is_authenticated:
        return render(request, "collection/index.html",
                      request.session["context"])
    else:
        return render(request, "collection/index.html")

def user_plateforms(request, user_owned_game, plateform, ELEM):
    """Called to refresh the list of officialy owned plateforms. Useful for
    the plateforms links on the base template"""

    user_platfor_list = []
    user_plateform_list = user_owned_game.objects.values_list(
        "plateform_id", flat=True).filter(user=request.user.id)
    counter = Counter(user_plateform_list)
    for item in counter:
        if item is not None:
            user_plateform_list = plateform.objects.get(id=item)
            region_name = ELEM[user_plateform_list.region - 1]
            user_plateform_list = (user_plateform_list.name, region_name)
            user_plateform_list = " - ".join(user_plateform_list)
            user_platfor_list.append({"plid": item,
                                      "pname": user_plateform_list})
    user_platfor_list.sort(key=itemgetter("pname"))
    context = request.session["context"]
    context["platfor_user"] = user_platfor_list
    return context
