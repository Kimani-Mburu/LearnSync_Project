from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def profile_view(request):
    user = request.user
    # Retrieve additional profile information or perform any other necessary operations
    # You can customize this view based on your requirements

    context = {
        'user': user,
    }
    return render(request, 'profile.html', context)
