from django.contrib import admin
from .models import Framework, Obligation, Clause, Control, Evidence


@admin.register(Framework)
class FrameworkAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'tenant', 'effective_from')
    search_fields = ('name', 'version')


@admin.register(Obligation)
class ObligationAdmin(admin.ModelAdmin):
    list_display = ('id', 'framework')


@admin.register(Clause)
class ClauseAdmin(admin.ModelAdmin):
    list_display = ('id', 'obligation')


@admin.register(Control)
class ControlAdmin(admin.ModelAdmin):
    list_display = ('id',)

#Evidence

@admin.register(Evidence)
class EvidenceAdmin(admin.ModelAdmin):
    list_display = ("id", "control", "created_at")