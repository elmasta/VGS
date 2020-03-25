from django.contrib import admin
from collection.models import Plateform, SubPlateform, PlateformAddon,\
    Compilation, Games, GameDLC

@admin.register(Plateform)
class PlateformAdmin(admin.ModelAdmin):
    pass

@admin.register(SubPlateform)
class SubPlateformAdmin(admin.ModelAdmin):
    pass

@admin.register(PlateformAddon)
class PlateformAddonAdmin(admin.ModelAdmin):
    pass

@admin.register(Compilation)
class CompilationAdmin(admin.ModelAdmin):
    pass

@admin.register(Games)
class GamesAdmin(admin.ModelAdmin):
    pass

@admin.register(GameDLC)
class GameDLCAdmin(admin.ModelAdmin):
    pass
