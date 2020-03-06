def return_index(request, render):

    if request.user.is_authenticated:
        return render(request, "collection/index.html", request.session['context'])
    else:
        return render(request, "collection/index.html")
