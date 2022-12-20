
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import CartItems, Log
from accounts.models import Profile



# ------------------------- auto create profile for user -------------------------

@receiver(post_save, sender=CartItems)
def order_log(sender, instance, **kwargs):

    import inspect
    for frame_record in inspect.stack():
        if frame_record[3]=='get_response':
            request = frame_record[0].f_locals['request']
            break

    else:
        request = None

    import jdatetime
    time_created = jdatetime.datetime.now()
    print(time_created)
    
    if instance.status == "Delivered":
        note = f"and it is delivered in {instance.delivery_date} by {request.user}"
    else:
        note = f"but it is not delivered yet"

    new_log = Log()
    new_log.description = f"profile by username {instance.user.username} ordered {instance.item} in" + str(time_created) + note
    new_log.save()
    
    instance.user.save()