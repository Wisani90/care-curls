from django.shortcuts import render

from django.views.generic import TemplateView

from haircare.models import Tag, Product, Item, HairType, HairProfile



def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_products = Product.objects.all().count()
    num_haittype = HairType.objects.all().count()
    
    context = {
        'num_products': num_products,
        'num_haittype': num_haittype,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

def home(request):
    context = {}
    template = 'haircare/home.html'
    return render(request, template, context)

def dashboard(request):

    user = request.user
    profile = None
    # hair = HairProfile.get_hair_profile(owner=user)

    history = []


    try:
        profile = request.user.userprofile
    except Exception as e:
        profile = None
            
    context = {

        'profile': profile,
        'hair': None,
        'history': history
    }
    print(profile.__dict__.keys())

    return render(request, 'profiles/dashboard.html', context=context)



class IndexPageView(TemplateView):
    template_name = 'main/index.html'

class ChangeLanguageView(TemplateView):
    template_name = 'main/change_language.html'