from django.contrib.auth import login


def login_user(request, user):
    user.update_last_login()
    login(request, user)
