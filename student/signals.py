from django.dispatch import receiver
from django.db.models.signals import pre_save
from student.models import Student

@receiver(pre_save,sender=Student)
def get_uppercase(sender,instance,**kwargs):
    instance.name=instance.name.upper()
    