from django.shortcuts import get_object_or_404, render

from .models import Country


def index(request):
    countries = Country.objects.all().order_by("name")

    return render(
        request,
        "country/index.html",
        {
            "countries": countries,
        },
    )


def public_state(request, country_id):
    country = get_object_or_404(Country, id=country_id)

    visible_institutions = country.institutions.filter(
        layer="decision",
    ).order_by("name")

    visible_policies = (
        country.policies
        .filter(status__in=["authorized", "implemented"])
        .select_related(
            "decision_institution",
            "implementation_institution",
        )
        .order_by("-id")
    )

    return render(
        request,
        "country/public_state.html",
        {
            "country": country,
            "institutions": visible_institutions,
            "policies": visible_policies,
        },
    )


def system_view(request, country_id):
    country = get_object_or_404(Country, id=country_id)

    decision_institutions = country.institutions.filter(
        layer="decision"
    ).order_by("name")

    influence_institutions = country.institutions.filter(
        layer="influence"
    ).order_by("name")

    implementation_institutions = country.institutions.filter(
        layer="implementation"
    ).order_by("name")

    policies = (
        country.policies
        .select_related(
            "decision_institution",
            "implementation_institution",
        )
        .prefetch_related(
            "influences__actor",
        )
        .order_by("-id")
    )

    return render(
        request,
        "country/system_view.html",
        {
            "country": country,
            "decision_institutions": decision_institutions,
            "influence_institutions": influence_institutions,
            "implementation_institutions": implementation_institutions,
            "policies": policies,
        },
    )