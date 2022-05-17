=====
Django Microservices Authentication 
=====

DMA is an application that allows you to create a user authentication service while preserving 
the Django concept and preserving the authenticated user instance\

Quick start
-----------

1. Add "authx" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        "authx",
    ]
    
2. Add "authx.authentication.TokenAuthentication" to your REST_FRAMEWORK setting like this::

    REST_FRAMEWORK = {
        "DEFAULT_AUTHENTICATION_CLASSES": [
            "authx.authentication.TokenAuthentication",
            ...
        ],
        ...
    }
    
    AUTH_USER_TABLE = "<User table name from authorization system>"

3. Include the authx URLconf in your project urls.py like this::

    path('', include("authx.urls")),

4. Run ``python manage.py migrate`` to create the polls models.

5. Add to settings::
        AUTH_USER_MODEL = "authx.CustomUser"
        
        AUTH_DB = 'primary_db'  
        DATABASE_ROUTERS = ["authx.dbrouter.AuthRouter"]
        AUTH_SERVER_PREFIX = "<Authorization service url>"
        DATABASES = {
            "default": {
                ...
            },
            "primary_db": {
                "ENGINE": "<Data to authorization service database>",
                "NAME": "<Data to authorization service database>",
                "USER": "<Data to authorization service database>",
                "PASSWORD": "<Data to authorization service database>",
                "HOST": "<Data to authorization service database>",
                "PORT": "<Data to authorization service database>",
            }
        }
