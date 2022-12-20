

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, Log





# ------------------------- auto create profile for user -------------------------
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# ------------------------- /auto create profile for user -------------------------

# ------------------------- auto create delete user when it's profile deleted -------------------------
@receiver(post_delete, sender=Profile)
def delete_profile_user(sender, instance, **kwargs):
    # ------------------------- get request -------------------------
    #instance.user.save()
    import inspect
    for frame_record in inspect.stack():
        if frame_record[3]=='get_response':
            request = frame_record[0].f_locals['request']
            break

    else:
        request = None

    # ------------------------- /get request -------------------------

    # ------------------------ add time and date -----------------------
    import jdatetime
    time_deleted = jdatetime.datetime.now()
    print(time_deleted)
    # ------------------------ /add time and date -----------------------

    #---------------------add delete log-----------------------
    new_log = Log()
    new_log.description = f"profile with id {instance.id} and username {instance.user.username} deleted by {request.user} with id {request.user.id} in" + str(time_deleted)
    new_log.save()
    #--------------------/add delete log-----------------------
    
    instance.user.delete()

# ------------------------- /auto create delete user when it's profile deleted -------------------------

# ------------------------- auto update user when it's profile updated -------------------------
@receiver(post_save, sender=Profile)
def update_profile_user(sender, instance, **kwargs):
    instance.user.save()

# ------------------------- /auto update user when it's profile updated -------------------------

# ------------------------- auto create log for create user when it's profile or user is create by another user -------------------------
@receiver(post_save, sender=Profile)
def log_create_profile_user(sender, instance, **kwargs):
    # ------------------------- get request -------------------------
    #instance.user.save()
    import inspect
    for frame_record in inspect.stack():
        if frame_record[3]=='get_response':
            request = frame_record[0].f_locals['request']
            break

    else:
        request = None

    # ------------------------- /get request -------------------------

    # ------------------------ add time and date -----------------------
    import jdatetime
    time_created = jdatetime.datetime.now()
    print(time_created)
    # ------------------------ /add time and date -----------------------

    #---------------------add delete log-----------------------
    new_log = Log()
    new_log.description = f"profile with id {instance.id} and username {instance.user.username} created by {request.user} with id {request.user.id} in" + str(time_created)
    new_log.save()
    #--------------------/add delete log-----------------------
    
    instance.user.save()
# ------------------------- /auto create log for create user when it's profile or user is create by another user -------------------------

