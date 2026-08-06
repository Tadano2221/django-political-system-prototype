from django.contrib import admin

from .models import (
    Country,
    Institution,
    Policy,
    InfluenceConnection,
)


class InstitutionInline(admin.TabularInline):
    model = Institution
    extra = 0

    fields = (
        "name",
        "layer",
        "authority",
        "capacity",
    )

    show_change_link = True


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "institution_count",
        "policy_count",
    )

    search_fields = (
        "name",
        "description",
    )

    ordering = ("name",)

    inlines = [
        InstitutionInline,
    ]

    @admin.display(description="Institutions")
    def institution_count(self, obj):
        return obj.institutions.count()

    @admin.display(description="Policies")
    def policy_count(self, obj):
        return obj.policies.count()


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "country",
        "layer",
        "authority",
        "capacity",
    )

    list_filter = (
        "country",
        "layer",
    )

    search_fields = (
        "name",
        "country__name",
        "description",
    )

    ordering = (
        "country",
        "layer",
        "name",
    )

    list_editable = (
        "authority",
        "capacity",
    )

    fieldsets = (
        (
            "Institution Identity",
            {
                "fields": (
                    "country",
                    "name",
                    "layer",
                )
            },
        ),
        (
            "Institutional Description",
            {
                "fields": (
                    "description",
                )
            },
        ),
        (
            "Institutional Strength",
            {
                "fields": (
                    "authority",
                    "capacity",
                )
            },
        ),
    )


class InfluenceConnectionInline(admin.TabularInline):
    model = InfluenceConnection
    extra = 1

    autocomplete_fields = (
        "actor",
    )

    fields = (
        "actor",
        "influence_type",
        "influence_strength",
        "explanation",
    )


@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "country",
        "status",
        "decision_institution",
        "implementation_institution",
    )

    list_filter = (
        "country",
        "status",
    )

    search_fields = (
        "title",
        "public_description",
        "country__name",
        "decision_institution__name",
        "implementation_institution__name",
    )

    ordering = (
        "country",
        "-id",
    )

    autocomplete_fields = (
        "country",
        "decision_institution",
        "implementation_institution",
    )

    inlines = [
        InfluenceConnectionInline,
    ]

    fieldsets = (
        (
            "Public Policy Output",
            {
                "fields": (
                    "country",
                    "title",
                    "public_description",
                    "status",
                )
            },
        ),
        (
            "View Layer: Decision Institution",
            {
                "fields": (
                    "decision_institution",
                )
            },
        ),
        (
            "Model Layer: Implementation System",
            {
                "fields": (
                    "implementation_institution",
                )
            },
        ),
    )


@admin.register(InfluenceConnection)
class InfluenceConnectionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "actor",
        "policy",
        "influence_type",
        "influence_strength",
    )

    list_filter = (
        "actor__country",
        "influence_type",
    )

    search_fields = (
        "actor__name",
        "policy__title",
        "influence_type",
        "explanation",
    )

    autocomplete_fields = (
        "actor",
        "policy",
    )

    ordering = (
        "policy",
        "-influence_strength",
    )

    list_editable = (
        "influence_strength",
    )