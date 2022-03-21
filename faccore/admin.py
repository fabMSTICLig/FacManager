from django.contrib import admin
from .models import MachineModel, Machine, TrainingLevel, Supply, SupplyUsage, Manager, Reservation, ReservationType, Availability
# Register your models here.

class TrainingLevelInline(admin.TabularInline):
    model = TrainingLevel
    extra = 0

@admin.register(MachineModel)
class MachineModelAdmin(admin.ModelAdmin):
    inlines = (TrainingLevelInline,)


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    pass


@admin.register(Supply)
class SupplyAdmin(admin.ModelAdmin):
    pass


@admin.register(SupplyUsage)
class SupplyUsageAdmin(admin.ModelAdmin):
    pass


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    pass


@admin.register(ReservationType)
class ReservationTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    pass


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    pass
