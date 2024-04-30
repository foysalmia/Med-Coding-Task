from django.views import generic
from product.models import Variant,Product,ProductVariantPrice


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context

class ProductListView(generic.ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    ordering = ['id']
    paginate_by = 5  # Number of items per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_data = []
        for product in context['products']:
            variants = ProductVariantPrice.objects.filter(product=product)
            variant_data = []
            for variant in variants:
                variant_data.append({
                    'title': f"{variant.product_variant_one} | {variant.product_variant_two} | {variant.product_variant_three}",
                    'price': variant.price,
                    'stock': variant.stock
                })
            product_data.append({
                'id' : product.id,
                'title': product.title,
                'description': product.description,
                'variants': variant_data
            })
        context['products'] = product_data
        return context