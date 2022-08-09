from django.core.paginator import Paginator
from django.db.models import Q
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
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
