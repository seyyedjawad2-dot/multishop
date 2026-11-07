from django.shortcuts import render
from django.views.generic import DetailView, TemplateView,ListView

from product.models import Product, Category,Color,Size


class ProductDetailView(DetailView):
    template_name = "product/product_detail.html"
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] =self.object.category.all()
        return context


class NavbarPartialView(TemplateView):
    template_name = 'includes/navbar.html'

    def get_context_data(self, **kwargs):
        context = super(NavbarPartialView,self).get_context_data()
        context['categories'] = Category.objects.all()
        return context




class ProductListView(ListView):
    model = Product
    template_name = 'product/product_list.html'
    context_object_name = 'products'
    paginate_by = 2

    def get_queryset(self):
        queryset = Product.objects.all()

        colors = self.request.GET.getlist('color')
        sizes = self.request.GET.getlist('size')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        category_slug = self.request.GET.get('category')

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        if colors:
            queryset = queryset.filter(color__title__in=colors).distinct()


        if sizes:
            queryset = queryset.filter(size__title__in=sizes).distinct()

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)


        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['colors'] = Color.objects.all()
        context['sizes'] = Size.objects.all()
        context['categories'] = Category.objects.all()
        return context



