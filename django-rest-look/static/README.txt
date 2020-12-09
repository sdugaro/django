#---------------------------------------------------------------------------

# needed to in config/settings.py to override rest_framework
# css and js scripts from within our own project folders

# Static files (CSS, JavaScript, Images)                                                             
# https://docs.djangoproject.com/en/3.1/howto/static-files/                                          
# Build paths inside the project like this: BASE_DIR / 'subdir'.                                     
# STATIC_ROOT:                                                                                       
#   the folder where static files will be stored after using                                         
#   ./manage.py collectstatic (copy to directory)                                                    
#   this does nothing for development, only required for deployment                                  
# STATICFILES_DIRS:                                                                                  
#   the list of folders where Django will search for additional                                      
#   static files                                                                                     
# STATIC_URL:                                                                                        
#   the url, relative to which, static files will be served                                          
#                                                                                                    
                                                                                                     
STATIC_URL = '/static/'                                                                              
#STATIC_ROOT = BASE_DIR / 'static'                                                                   
STATICFILES_DIRS = [BASE_DIR / "static"]  # for loc   


# When overriding templates from another project such as the                                         
# rest_framework api.html tempate, Djangos template loader                                           
# will search DIRS before APP_DIRS in order to pick it up                                            
TEMPLATES = [                                                                                        
    {                                                                                                
        'BACKEND': 'django.template.backends.django.DjangoTemplates',                                
        # app override of reset_framework/templates                                                  
        'DIRS': [BASE_DIR / 'templates'],                                                            
        #'DIRS': [],                                                                                 
        'APP_DIRS': True, # search app level templates (no worky?)                                                                            
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

