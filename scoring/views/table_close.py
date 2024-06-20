from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from ..models import Table


@require_http_methods(["POST"])
@login_required(login_url="/accounts/login")
def table_close(request: HttpRequest, table_pk: int):
    table = Table.objects.get(pk=table_pk)
    # Only the owner can close the table
    if table.owner.username != request.user.username:
        return HttpResponseForbidden()

    table.close()
    send_mail(
        subject="Table closed",
        message=f"Your table {table} has been closed.",
        from_email="dancab.messenger.bot@gmail.com",
        recipient_list=["danielcaballero88@gmail.com"],
        fail_silently=False,
    )
    return HttpResponseRedirect(reverse("scoring:table_detail", args=[table_pk]))
