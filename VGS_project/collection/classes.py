def return_index(request, render):

    if request.user.is_authenticated:
        return render(request, "collection/index.html", request.session['context'])
    else:
        return render(request, "collection/index.html")

def list_cleaning(item):

    item = item.split("-", 3)
    game_name = item[0].rstrip()
    game_plat = item[1].lstrip()
    game_plat = game_plat.rstrip()
    game_reg = item[2].lstrip()
    game_reg = game_reg.rstrip()
    return game_name, game_plat, game_reg, item
