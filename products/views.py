from django.core.paginator import Paginator, InvalidPage
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView
from products import models, forms


class PostList(ListView):

    """PostListView Definition"""

    model = models.Product
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "products"

    def get_queryset(self):
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
        keyword = self.request.GET.get("keyword", None)
        if keyword is not None:
            queryset = models.Product.objects.filter(
                Q(brand__name__icontains=keyword)
                | Q(model_number=keyword)
                | Q(name_en__icontains=keyword)
                | Q(name_kr__icontains=keyword)
            ).order_by(*ordering)
        else:
            queryset = models.Product.objects.all().order_by(*ordering)

        return queryset

    def paginate_queryset(self, queryset, page_size):
        """Paginate the queryset, if needed."""
        paginator = self.get_paginator(
            queryset,
            page_size,
            orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty(),
        )
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        try:
            page_number = int(page)
        except ValueError:
            if page == "last":
                page_number = paginator.num_pages
            else:
                raise Http404(
                    ("Page is not “last”, nor can it be converted to an int.")
                )
        try:
            page = paginator.get_page(page_number)
            return (paginator, page, page.object_list, page.has_other_pages())
        except InvalidPage as e:
            raise Http404(
                ("Invalid page (%(page_number)s): %(message)s")
                % {"page_number": page_number, "message": str(e)}
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        page = int(self.request.GET.get(self.page_kwarg, 1))
        page_obj = context["page_obj"]
        last_page = page_obj.paginator.num_pages
        if page > last_page:
            page = last_page
        paginate_by = self.paginate_by
        context["page"] = (page - 1) * paginate_by
        return context


class ProductDetail(DetailView):
    model = models.Product


class SearchView(View):
    def get(self, request):

        form = forms.SearchForm(request.GET)

        if form.is_valid():
            keyword = form.cleaned_data.get("keyword", None)
            brands = form.cleaned_data.get("brands")
            price = form.cleaned_data.get("price")
            q = Q()
            filter_args = {}
            if keyword is not None and keyword != "":
                q.add(
                    Q(brand__name__icontains=keyword)
                    | Q(model_number=keyword)
                    | Q(name_en__icontains=keyword)
                    | Q(name_kr__icontains=keyword),
                    q.AND,
                )
            if len(price) > 0:
                if "-100000" in price:
                    q.add(Q(released_price__lte=100000), q.OR)
                if "200000-300000" in price:
                    q.add(
                        Q(released_price__gte=200000, released_price__lte=300000), q.OR
                    )
                if "300000-500000" in price:
                    q.add(
                        Q(released_price__gte=300000, released_price__lte=500000), q.OR
                    )
                if "500000-" in price:
                    q.add(Q(released_price__gte=500000), q.OR)
            if brands.exists():
                filter_args["brand__pk__in"] = brands.values_list("pk", flat=True)

            qs = models.Product.objects.filter(q, **filter_args).order_by("-created")

            paginator = Paginator(qs, 10, orphans=5)

            page = request.GET.get("page", 1)

            products = paginator.get_page(page)
            return render(
                request, "products/search.html", {"form": form, "products": products}
            )
        else:
            form = forms.SearchForm()
        return render(
            request,
            "products/search.html",
            {
                "form": form,
            },
        )
