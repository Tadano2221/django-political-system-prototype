from django.core.management.base import BaseCommand
from django.db import transaction

from country.models import (
    Country,
    Institution,
    Policy,
    InfluenceConnection,
)
class Command(BaseCommand):
    help = "Seed countries, institutions, policies, and influence connections."

    @transaction.atomic
    def handle(self, *args, **options):
        self.seed_united_states()
        self.seed_united_kingdom()
        self.seed_singapore()
        self.seed_china()
        self.seed_russia()

        self.stdout.write(
            self.style.SUCCESS("Political prototype data added successfully.")
        )

    def create_institution(
        self,
        country,
        name,
        layer,
        description,
        authority,
        capacity,
    ):
        institution, _ = Institution.objects.update_or_create(
            country=country,
            name=name,
            defaults={
                "layer": layer,
                "description": description,
                "authority": authority,
                "capacity": capacity,
            },
        )
        return institution

    def seed_united_states(self):
        country, _ = Country.objects.update_or_create(
            name="United States",
            defaults={
                "description": (
                    "A federal presidential system with authority divided "
                    "across Congress, the executive, courts, agencies, and states."
                )
            },
        )

        decision = self.create_institution(
            country,
            "Congressional Committees",
            "decision",
            "Committees examine legislation and determine which bills advance.",
            85,
            80,
        )

        influence = self.create_institution(
            country,
            "Semiconductor Industry Association",
            "influence",
            "An industry organisation providing expertise and policy advocacy.",
            35,
            75,
        )

        implementation = self.create_institution(
            country,
            "CHIPS Program Office",
            "implementation",
            "The administrative body implementing semiconductor funding.",
            70,
            90,
        )

        policy, _ = Policy.objects.update_or_create(
            country=country,
            title="CHIPS and Science Act",
            defaults={
                "public_description": (
                    "National legislation supporting semiconductor "
                    "manufacturing, research, and supply-chain resilience."
                ),
                "status": "implemented",
                "decision_institution": decision,
                "implementation_institution": implementation,
            },
        )

        InfluenceConnection.objects.update_or_create(
            actor=influence,
            policy=policy,
            defaults={
                "influence_type": "Industry advocacy",
                "influence_strength": 75,
                "explanation": (
                    "Industry organisations provided technical information "
                    "and advocated for manufacturing incentives."
                ),
            },
        )

    def seed_united_kingdom(self):
        country, _ = Country.objects.update_or_create(
            name="United Kingdom",
            defaults={
                "description": (
                    "A parliamentary system supported by Cabinet, "
                    "Whitehall departments, Parliament, and the Civil Service."
                )
            },
        )

        decision = self.create_institution(
            country,
            "HM Treasury and Cabinet",
            "decision",
            "Central institutions responsible for financial and executive decisions.",
            85,
            90,
        )

        influence = self.create_institution(
            country,
            "Party Whips and Advisory Networks",
            "influence",
            "Actors shaping parliamentary coordination and policy access.",
            55,
            75,
        )

        implementation = self.create_institution(
            country,
            "Whitehall Departments",
            "implementation",
            "Government departments translating decisions into administration.",
            75,
            90,
        )

        policy, _ = Policy.objects.update_or_create(
            country=country,
            title="Covid Corporate Financing Facility",
            defaults={
                "public_description": (
                    "A government financing programme designed to support "
                    "large businesses affected by the pandemic."
                ),
                "status": "implemented",
                "decision_institution": decision,
                "implementation_institution": implementation,
            },
        )

        InfluenceConnection.objects.update_or_create(
            actor=influence,
            policy=policy,
            defaults={
                "influence_type": "Political access and consultation",
                "influence_strength": 60,
                "explanation": (
                    "Political and business networks attempted to influence "
                    "access to government financial support."
                ),
            },
        )

    def seed_singapore(self):
        country, _ = Country.objects.update_or_create(
            name="Singapore",
            defaults={
                "description": (
                    "A parliamentary system characterised by central "
                    "coordination, statutory boards, and organised consultation."
                )
            },
        )

        decision = self.create_institution(
            country,
            "Parliament and Central Ministries",
            "decision",
            "Institutions responsible for authorising national policy.",
            90,
            95,
        )

        influence = self.create_institution(
            country,
            "Public and Expert Consultation Networks",
            "influence",
            "Citizens, specialists, and advisory bodies shaping policy feedback.",
            45,
            80,
        )

        implementation = self.create_institution(
            country,
            "GovTech and MDDI",
            "implementation",
            "Public institutions responsible for digital policy implementation.",
            80,
            95,
        )

        policy, _ = Policy.objects.update_or_create(
            country=country,
            title="TraceTogether Data Access Restrictions",
            defaults={
                "public_description": (
                    "Legislation restricting law-enforcement access to "
                    "digital contact-tracing information."
                ),
                "status": "implemented",
                "decision_institution": decision,
                "implementation_institution": implementation,
            },
        )

        InfluenceConnection.objects.update_or_create(
            actor=influence,
            policy=policy,
            defaults={
                "influence_type": "Public feedback",
                "influence_strength": 70,
                "explanation": (
                    "Public concern regarding data access contributed "
                    "to legislative restrictions."
                ),
            },
        )

    def seed_china(self):
        country, _ = Country.objects.update_or_create(
            name="China",
            defaults={
                "description": (
                    "A Party-state system in which Communist Party bodies "
                    "set strategic direction and state institutions execute policy."
                )
            },
        )

        decision = self.create_institution(
            country,
            "CPC Central Committee",
            "decision",
            "The central Party institution directing major political reforms.",
            98,
            95,
        )

        influence = self.create_institution(
            country,
            "Policy Consultation Networks",
            "influence",
            "Research institutes, specialists, and controlled consultative bodies.",
            40,
            85,
        )

        implementation = self.create_institution(
            country,
            "State Council and Provincial Administrations",
            "implementation",
            "State institutions implementing central policy across China.",
            90,
            95,
        )

        policy, _ = Policy.objects.update_or_create(
            country=country,
            title="2023 Party and State Institutional Reform",
            defaults={
                "public_description": (
                    "A national reform reorganising Party and state institutions "
                    "responsible for finance, technology, and administration."
                ),
                "status": "implemented",
                "decision_institution": decision,
                "implementation_institution": implementation,
            },
        )

        InfluenceConnection.objects.update_or_create(
            actor=influence,
            policy=policy,
            defaults={
                "influence_type": "Controlled consultation",
                "influence_strength": 55,
                "explanation": (
                    "Specialists and consultative organisations provided "
                    "opinions before formal adoption."
                ),
            },
        )

    def seed_russia(self):
        country, _ = Country.objects.update_or_create(
            name="Russia",
            defaults={
                "description": (
                    "A presidential system in which administration and elite "
                    "networks are organised closely around the presidency."
                )
            },
        )

        decision = self.create_institution(
            country,
            "Presidential Executive Office",
            "decision",
            "The institution preparing presidential decisions and instructions.",
            95,
            90,
        )

        influence = self.create_institution(
            country,
            "Security Council",
            "influence",
            "A senior security body advising the presidency.",
            80,
            90,
        )

        implementation = self.create_institution(
            country,
            "Federal Ministries and Regional Administrations",
            "implementation",
            "Institutions carrying presidential decisions across the federation.",
            80,
            85,
        )

        policy, _ = Policy.objects.update_or_create(
            country=country,
            title="Recognition of Donetsk and Lugansk Entities",
            defaults={
                "public_description": (
                    "Presidential orders recognising the Donetsk and Lugansk "
                    "entities in February 2022."
                ),
                "status": "authorized",
                "decision_institution": decision,
                "implementation_institution": implementation,
            },
        )

        InfluenceConnection.objects.update_or_create(
            actor=influence,
            policy=policy,
            defaults={
                "influence_type": "Security consultation",
                "influence_strength": 85,
                "explanation": (
                    "The Security Council participated in consultation "
                    "before the public presidential orders."
                ),
            },
        )