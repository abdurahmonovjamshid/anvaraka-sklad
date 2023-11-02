from django.db.models.signals import post_delete, post_save, pre_save
from . models import Warehouse, Sales, Product
from django.dispatch import receiver


@receiver(post_save, sender=Warehouse)
def add_component_total(sender, instance, created, **kwargs):
    if created:
        component = instance.component
        component.total += instance.quantity
        component.save()


@receiver(pre_save, sender=Warehouse)
def update_component_total_on_edit(sender, instance, **kwargs):
    if instance.pk:
        old_warehouse = Warehouse.objects.get(pk=instance.pk)
        component = instance.component
        component.total = component.total - old_warehouse.quantity + instance.quantity
        component.save()


@receiver(post_delete, sender=Warehouse)
def update_component_total_on_delete(sender, instance, **kwargs):
    component = instance.component
    component.total -= instance.quantity
    component.save()


@receiver(post_save, sender=Sales)
def add_component_total(sender, instance, created, **kwargs):
    if created:
        component = instance.component
        component.total -= instance.quantity
        component.save()


@receiver(pre_save, sender=Sales)
def update_component_total_on_edit(sender, instance, **kwargs):
    if instance.pk:
        old_warehouse = Sales.objects.get(pk=instance.pk)
        component = instance.component
        component.total = component.total + old_warehouse.quantity - instance.quantity
        component.save()


@receiver(post_delete, sender=Sales)
def update_component_total_on_delete(sender, instance, **kwargs):
    component = instance.component
    component.total += instance.quantity
    component.save()
