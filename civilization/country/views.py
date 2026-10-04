from django.shortcuts import get_object_or_404, render

from .models import Country, InfluenceConnection, Institution


def repair_singapore_placeholder(country):
    """
    Replace the old Singapore test record with a real policy example.
    This runs only when the placeholder still exists, so it is safe on redeploys
    that restore the repository's SQLite database.
    """
    if country.name != "Singapore":
        return

    placeholder = country.policies.filter(title="HHFJHB$Ff").first()
    if placeholder is None:
        return

    decision = country.institutions.filter(
        name="Parliament and Central Ministries",
        layer="decision",
    ).first()

    if decision is None:
        decision = Institution.objects.create(
            country=country,
            name="Parliament and Central Ministries",
            layer="decision",
            description="Institutions responsible for authorising national policy.",
            authority=90,
            capacity=95,
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

    placeholder.title = "Platform Workers Act 2024"
    placeholder.public_description = (
        "Legislation strengthening protections for platform workers through "
        "work injury compensation, CPF contributions, and representation rights."
    )
    placeholder.status = "implemented"
    placeholder.decision_institution = decision
    placeholder.implementation_institution = implementation
    placeholder.save()

    placeholder.influences.all().delete()
    InfluenceConnection.objects.create(
        actor=influence,
        policy=placeholder,
        influence_type="Tripartite recommendations",
        influence_strength=75,
        explanation=(
            "Recommendations from the Advisory Committee on Platform Workers "
            "informed the protections later implemented through the Act."
        ),
    )

    old_minister = country.institutions.filter(name="Minister").first()
    if old_minister is not None:
        if (
            not old_minister.authorized_policies.exists()
            and not old_minister.implemented_policies.exists()
            and not old_minister.influence_connections.exists()
        ):
            old_minister.delete()


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
    repair_singapore_placeholder(country)

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
    repair_singapore_placeholder(country)

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
