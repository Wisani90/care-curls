from django.shortcuts import render



def dashboard(request):

    user = request.user
    profile = None
    hair = None

    history = []

    if request.method == 'GET':
    	try:
	        profile = user.profile
	        hair = get_hair_profile(user)
	    except Exception as e:
	    	profile = None
	    	hair = None
	    	
        context = {

            'profile': profile,

            'hair': hair,

            'history': history
        }

    return render(request, 'dashboard.html', context=context)

