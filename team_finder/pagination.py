from django.core.paginator import Paginator

DEFAULT_PAGE_SIZE = 12


def paginate_queryset(request, queryset, page_size=DEFAULT_PAGE_SIZE):
    paginator = Paginator(queryset, page_size)
    return paginator.get_page(request.GET.get("page"))
