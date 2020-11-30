from requests import request, HTTPError
from django.core.files.base import ContentFile


def save_image(user, image_url, params):
    try:
        response = request('GET', image_url, params=params)
        response.raise_for_status()
    except HTTPError:
        pass
    else:
        user.avatar.save(
            '{0}.jpg'.format(user.id),
            ContentFile(response.content))
        user.save()


def save_avatar(backend, user, response, details,
                         is_new=False, *args, **kwargs):
    if is_new:
        if backend.name == 'facebook':
            image_url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
            save_image(user, image_url, {'type': 'large'})
        elif backend.name == 'google-oauth2':
            image_url = response['picture']
            save_image(user, image_url, {})
