from django.shortcuts import get_object_or_404, render

from .models import Country, InfluenceConnection, Institution


def normalize_singapore_policy(country):
    """
    Keep Singapore comparable with the other country cases by using one
    canonical policy pathway only: the Platform Workers Act 2024.
    The function is idempotent and also cleans older placeholder/duplicate
    Singapore records that may still exist in the deployed SQLite database.
    """
    if country.name != "Singapore":
        return

    decision, _ = Institution.objects.update_or_create(
        country=country,
        name="Parliament and Central Ministries",
        defaults={
            "layer": "decision",
            "description": "Institutions responsible for authorising national policy.",
            "authority": 90,
            "capacity": 95,
        },
    )

    influence, _ = Institution.objects.update_or_create(
        country=country,
        name="Advisory Committee on Platform Workers",
        defaults={
            "layer": "influence",
            "description": (
                "A tripartite advisory committee whose recommendations informed "
                "stronger protections for platform workers."
            ),
            "authority": 45,
            "capacity": 80,
        },
    )

    implementation, _ = Institution.objects.update_or_create(
        country=country,
        name="Ministry of Manpower and CPF Board",
        defaults={
            "layer": "implementation",
            "description": (
                "Public institutions responsible for administering platform-worker "
                "protections and CPF contribution requirements."
            ),
            "authority": 80,
            "capacity": 95,
        },
    )

    platform_policy, _ = country.policies.update_or_create(
        title="Platform Workers Act 2024",
        defaults={
            "public_description": (
                "Legislation strengthening protections for platform workers through "
                "work injury compensation, CPF contributions, and representation rights."
            ),
            "status": "implemented",
            "decision_institution": decision,
            "implementation_institution": implementation,
        },
    )

    # Remove the former placeholder and the older second Singapore policy so that
    # Singapore has one policy case, matching the structure of the other countries.
    country.policies.exclude(pk=platform_policy.pk).delete()

    # Keep one influence relationship for the canonical Singapore policy.
    platform_policy.influences.exclude(actor=influence).delete()
    InfluenceConnection.objects.update_or_create(
        actor=influence,
        policy=platform_policy,
        defaults={
            "influence_type": "Tripartite recommendations",
            "influence_strength": 75,
            "explanation": (
                "Recommendations from the Advisory Committee on Platform Workers "
                "informed the protections later implemented through the Act."
            ),
        },
    )

    # Remove old Singapore-only institutions that belonged to the placeholder,
    # TraceTogether case, or earlier duplicated variants.
    keep_institutions = [decision.pk, influence.pk, implementation.pk]
    country.institutions.exclude(pk__in=keep_institutions).delete()


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
    normalize_singapore_policy(country)

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
    normalize_singapore_policy(country)

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
