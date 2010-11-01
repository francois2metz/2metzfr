# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response

from django.conf import settings

from django_wsgi import django_view

from wsgidav.fs_dav_provider import FilesystemProvider
from wsgidav.wsgidav_app import DEFAULT_CONFIG, WsgiDAVApp

from django.contrib.auth import authenticate

from os import path

def index(request):
    return render_to_response('metz/index.html', {}, RequestContext(request))

def default_index(request):
    return render_to_response('metz/default.html', {}, RequestContext(request))

def index_dav(request):
    return default_index(request)

class DjangoDomainController(object):
    def __init__(self, login):
        self.login = login

    def __repr__(self):
        return self.__class__.__name_

    def getDomainRealm(self, inputURL, environ):
        return "Dav Auth"

    def requireAuthentication(self, realmname, environ):
        return True

    def isRealmUser(self, realmname, username, environ):
        return True

    def getRealmUserPassword(self, realmname, username, environ):
        pass

    def authDomainUser(self, realmname, username, password, environ):
        if self.login != username:
            return False
        user = authenticate(username=username, password=password)
        if user is not None:
            return True
        return False

def dav_for_user(request, login):
    provider = FilesystemProvider(path.join(settings.DAV_ROOT, login) + "/")
    config = DEFAULT_CONFIG.copy()
    config.update({
        "provider_mapping": {"/"+login: provider},
        "verbose": 1,
        "enable_loggers": [],
        "acceptdigest": False,
        "propsmanager": True,      # True: use property_manager.PropertyManager                    
        "locksmanager": True,      # True: use lock_manager.LockManager                   
        "domaincontroller": DjangoDomainController(login),  # None: domain_controller.WsgiDAVDomainController(user_mapping)
        })
    return django_view(WsgiDAVApp(config))(request)
