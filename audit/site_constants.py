import environ
from django.conf import settings
env=environ.Env()
environ.Env().read_env()
def export_vars(request):
    data={
            'site_name':env('SITE_NAME'),
            'site_url':env('SITE_URL'),
     	    'designer_link':env('SITE_DESIGNER_LINK'),
            'designer_name':env('SITE_DESIGNER_NAME'),
            'designer portfolio':env('SITE_DESIGNER_NAME'),
            'facebook_link':env('FACEBOOK_LINK'),
            'twitter_link':env('TWITTER_LINK'),
            'instagram_link':env('INSTAGRAM_LINK'),
            'whatsapp_link':env('WHATSAPP_LINK'),
            'linkedin_link':env('LINKEDIN_LINK'),
    }
    return data