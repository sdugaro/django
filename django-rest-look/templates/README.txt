# needed to override rest_framework templates with our own apps {% block content %}
# https://docs.djangoproject.com/en/3.1/howto/overriding-templates/

TEMPLATES = [                                                                                        
    {                                                                                                
        'BACKEND': 'django.template.backends.django.DjangoTemplates',                                
        # app override of reset_framework/templates                                                  
        'DIRS': [BASE_DIR / 'templates'],                                                            
        #'DIRS': [],                                                                                 
        'APP_DIRS': True,                                                                            
        'OPTIONS': {                                                                                 
            'context_processors': [                                                                  
                'django.template.context_processors.debug',                                          
                'django.template.context_processors.request',                                        
                'django.contrib.auth.context_processors.auth',                                       
                'django.contrib.messages.context_processors.messages',                               
            ],                                                                                       
        },                                                                                           
    },                                                                                               
]   

