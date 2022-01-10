from django.shortcuts import render

from ecommerce.inventory import models


def home(request):
    return render(request, 'index.html')


def category(request):
    data = models.Category.objects.all()

    return render(request, 'categories.html', {'data': data})


def product_by_category(request, category):
    current_category = models.Category.objects.get(slug=category)
    data = models.Product.objects.filter(category__name=category).values(
        'id', 'name', 'slug', 'category__name', 'product__store_price'
    )
    context = {
        'current_category': current_category,
        'data': data,
    }
    return render(request, 'product_by_category.html', context)


def product_detail(request, slug):

    filter_arguments = []





    current_product = models.ProductInventory.objects.filter(product__slug=slug)
    current_category = models.Category.objects.get(product__slug=slug)

    # If parameters in url bar (?color=red&size=5), show this, else, show that
    if request.GET:
        for value in request.GET.values():
            filter_arguments.append(value)

        from django.db.models import Count

        data = models.ProductInventory.objects.filter(product__slug=slug).\
            filter(attribute_values__attribute_value__in=filter_arguments).\
            annotate(num_tags=Count('attribute_values')).\
            filter(num_tags=len(filter_arguments)).\
            values('id', 'sku', 'product__name', 'store_price', 'product_inventory__units')
    else:
        data = models.ProductInventory.objects.filter(product__slug=slug).filter(is_default=True).\
            values('id', 'sku', 'product__name', 'store_price', 'product_inventory__units')




    y = models.ProductInventory.objects.filter(product__slug=slug).distinct().values(
        'attribute_values__product_attribute__name', 'attribute_values__attribute_value'
    )

    z = models.ProductTypeAttribute.objects.filter(product_type__product_type__product__slug=slug).values(
        'product_attribute__name').distinct()

    context = {
        'current_product': current_product,
        'current_category': current_category,
        'data': data,
        'y': y,
        'z': z,
    }
    return render(request, 'product_detail.html', context)
