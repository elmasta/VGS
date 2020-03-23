from collections import Counter
from operator import itemgetter
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from collection.tokens import account_activation_token
from django.template.loader import render_to_string

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

def send_email(email, template, mail_subject, User):

    user = User.objects.get(email=email)
    message = render_to_string(
        template, {
            "user": user,
            "uid": urlsafe_base64_encode(force_bytes(user.id)),
            "token":account_activation_token.make_token(user)
        })
    to_email = EmailMessage(
        mail_subject, message, to=[email]
    )
    to_email.send()
