from django.conf import settings # import the settings file

def website_title(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'WEBSITE_TITLE': settings.WEBSITE_TITLE}