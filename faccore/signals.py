from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import ReservationType, MachineModel, TrainingLevel


@receiver(post_save, sender=MachineModel)
def build_reservation_on_machinmodel_creation(sender, instance, created, **kwargs):
    """
    When a new model of machine is added, 
    a reservation type with the same name is created
    and a traininglevel is created for each user
    """
    if created:
        res = ReservationType(name=instance.name)
        res.save()
        res.needs.add(instance)
        res.save()
        tls = []
        for user in get_user_model().objects.all():
            tl = TrainingLevel(machine_model=instance,user=user)
            tls.append(tl)
        TrainingLevel.objects.bulk_create(tls)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def build_traininglevel_on_person_creation(sender, instance, created, **kwargs):
    """
    When a new Person is added, create training level for all machine model
    """
    if created:
        tls = []
        for mm in MachineModel.objects.all():
            tl = TrainingLevel(machine_model=mm,user=instance)
            tls.append(tl)
        TrainingLevel.objects.bulk_create(tls)

