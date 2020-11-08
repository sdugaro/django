from django.db import models
from datetime import datetime

# Create your models here.
# In Django, the MEDIA_ROOT setting is where we define the location of all user uploaded items.
# MEDIA_ROOT is the absolute filesystem path to the directory for user-uploaded files
# MEDIA_URL is the URL we can use in our templates for the files
# by default MEDIA_ROOT and MEDIA_URL are empty and not displayed so add them
# config/settings.py
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# create /media/images at the project root alongside the app directory
# If we wanted to use a regular file here the only difference could be to change ImageField to FileField.
# upload_to specifies the directory relative to $MEDIA_ROOT where posted images
# are save on disk relative to the project directory.

# A TextField is a type of field, which when used by a ModelForm
# uses the Textarea widget by default. Fields deal with backend
# storage, while widgets with front end editing and rendering.
# you can specify widget look configuration in forms.py. 
# As far as initializing the field for the backend, those args can be passed
# into the Field initializers here. providing null=True tells Django to stoer
# empty values as null in the databse. Avoid using null on string based fields
# as that would mean there are two possible values for 'no data' that will
# have to be handled. Some options are  default= which could be a callable
# which will be executed each time a new object is created.

def callback():
    print("---> Constructed a Post TextField: [{}]".format(str(datetime.now())))
    return "default"

class Post(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    summary = models.TextField(default=callback, max_length=100)

    def __str__(self):
        return self.title

