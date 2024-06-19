from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from ..models import Table


@require_http_methods(["POST"])
@login_required(login_url="/accounts/login")
def table_reopen(request: HttpRequest, table_pk: int):
    table = Table.objects.get(pk=table_pk)
    # Only the owner can reopen the table
    if table.owner.username != request.user.username:
        return HttpResponseForbidden()

    table.open()
    return HttpResponseRedirect(reverse("scoring:table_detail", args=[table_pk]))
