from django.shortcuts import render

def controlpanel(request):
	return render(request, 'controlpanel/base.html')