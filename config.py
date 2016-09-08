# -*- coding: utf-8 -*-

import platform

WTF_CSRF_ENABLED = True

SECRET_KEY = 'fa51ea7ed90c8fc9523c042b2c3093165cdc736883df6b33'

host_name = platform.node()
host = "127.0.0.1" if host_name == 'sid-hdb' else "52.58.251.227"

SQLALCHEMY_DATABASE_URI = 'hana://SYSTEM:a5_hS3aZ#@{}:30015'.format(host)
# SQLALCHEMY_DATABASE_URI = 'hana://SYSTEM:Abcd1234@localhost:30015'

SQLALCHEMY_TRACK_MODIFICATIONS = False
