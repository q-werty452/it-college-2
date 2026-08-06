from .models import Contacts, SocialLink

def global_contacts(request):
    return {
        'contacts': Contacts.objects.first(),
        'socials': SocialLink.objects.filter(is_active=True)
    }