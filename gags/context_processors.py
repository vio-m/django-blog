from .models import Category


def add_variable_to_context(request):
    categories = Category.objects.all()
    context = {'category_list': categories}
    return context

