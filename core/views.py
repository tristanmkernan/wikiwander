from django.views.generic import ListView

from core.models import WikiPage


class IndexView(ListView):
    template_name = "core/index.html"
    model = WikiPage
    queryset = WikiPage.objects.order_by("-created_at")[:5]


class WikiPageHistoryPartialView(ListView):
    template_name = "core/wikipage/partials/history-list.html"
    model = WikiPage
    queryset = WikiPage.objects.order_by("-created_at")[:5]
