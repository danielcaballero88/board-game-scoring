from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render

from scoring.mocks.user import get_user_tables


@login_required(login_url="/accounts/login")
def index(request: HttpRequest):
    username = request.user.username
    previous_scores = get_user_tables(username)

    context = {"previous_scores": previous_scores}
    return render(request, "scoring/index.html", context)
