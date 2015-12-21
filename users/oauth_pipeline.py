def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'sitcon':
        #for ( key, value ) in response['profile'].items():
        #    if key in ('bio', 'display_name', 'title'):
        #        setattr(user.profile, key, value)
        #    elif key == 'avatar':
        #        if value.startswith('http'):
        #            setattr(user.profile, key, value)
        user.profile.bio = response['profile']['bio']
        user.profile.display_name = response['profile']['display_name']
        user.profile.title = response['profile']['title']
        #if response['profile']['avatar'].startswith('http'): # copy gravatar url
        #    user.profile.avatar = response['profile']['avatar']
        # TODO: fetch photo from staff
        user.profile.save()
    else:
        raise NotImplementedError
