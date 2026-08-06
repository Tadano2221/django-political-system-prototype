from django.db import models

# Create your models here.
from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Institution(models.Model):
    LAYER_CHOICES = [
        ("decision", "Decision Institution"),
        ("influence", "Influence Network"),
        ("implementation", "Implementation System"),
    ]

    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="institutions",
    )

    name = models.CharField(max_length=150)

    layer = models.CharField(
        max_length=30,
        choices=LAYER_CHOICES,
    )

    description = models.TextField()

    authority = models.PositiveIntegerField(
        default=50,
        help_text="Relative institutional authority from 0 to 100.",
    )

    capacity = models.PositiveIntegerField(
        default=50,
        help_text="Relative implementation capacity from 0 to 100.",
    )

    def __str__(self):
        return f"{self.country.name}: {self.name}"


class Policy(models.Model):
    STATUS_CHOICES = [
        ("proposed", "Proposed"),
        ("processed", "Processed"),
        ("authorized", "Authorized"),
        ("implemented", "Implemented"),
    ]

    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="policies",
    )

    title = models.CharField(max_length=150)
    public_description = models.TextField()
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="proposed",
    )

    decision_institution = models.ForeignKey(
        Institution,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="authorized_policies",
    )

    implementation_institution = models.ForeignKey(
        Institution,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="implemented_policies",
    )

    def __str__(self):
        return self.title

class InfluenceConnection(models.Model):
    actor = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE,
        related_name="influence_connections",
    )

    policy = models.ForeignKey(
        Policy,
        on_delete=models.CASCADE,
        related_name="influences",
    )

    influence_type = models.CharField(max_length=100)

    influence_strength = models.PositiveIntegerField(
        default=50,
        help_text="Relative influence from 0 to 100.",
    )

    explanation = models.TextField(blank=True)

    def __str__(self):
        return f"{self.actor.name} → {self.policy.title}"