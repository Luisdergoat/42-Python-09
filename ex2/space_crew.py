"""Exercise 2: Space Crew Management.

Simple nested Pydantic models with mission safety rules.
"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, ValidationError, model_validator


class Rank(str, Enum):
    """All allowed crew ranks."""

    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    """One person in the mission crew."""

    # Dieses Modell ist verschachtelt in SpaceMission.
    # Pydantic validiert jedes CrewMember automatisch.

    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    """Mission data with nested crew members."""

    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def validate_mission_rules(self) -> "SpaceMission":
        """Validate mission safety rules after normal field checks."""
        # Rule 1: mission id should start with M.
        if not self.mission_id.startswith("M"):
            raise ValueError('Mission ID must start with "M"')

        # Rule 2: mission needs a commander or captain.
        # any(...) ist True, sobald mindestens eine Person passt.
        has_leader = any(
            member.rank in (Rank.COMMANDER, Rank.CAPTAIN)
            for member in self.crew
        )
        if not has_leader:
            raise ValueError(
                "Mission must have at least one Commander or Captain"
            )

        # Rule 3: long missions need 50% experienced crew (5+ years).
        if self.duration_days > 365:
            # True zählt hier als 1, False als 0.
            experienced_count = sum(
                member.years_experience >= 5 for member in self.crew
            )
            if experienced_count < len(self.crew) / 2:
                raise ValueError(
                    "Long missions (> 365 days) need 50% experienced crew"
                )

        # Rule 4: all crew members must be active.
        if any(not member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")

        return self


def demonstrate_space_crew() -> None:
    """Show one valid mission and one expected validation failure."""
    print("Space Mission Crew Validation")
    print("=" * 41)

    # Gültige Mission mit kompletter Crew.
    print("Valid mission created:")
    valid_mission = SpaceMission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date=datetime(2027, 5, 1, 9, 30),
        duration_days=900,
        budget_millions=2500.0,
        crew=[
            CrewMember(
                member_id="CM001",
                name="Sarah Connor",
                rank=Rank.COMMANDER,
                age=41,
                specialization="Mission Command",
                years_experience=15,
            ),
            CrewMember(
                member_id="CM002",
                name="John Smith",
                rank=Rank.LIEUTENANT,
                age=34,
                specialization="Navigation",
                years_experience=8,
            ),
            CrewMember(
                member_id="CM003",
                name="Alice Johnson",
                rank=Rank.OFFICER,
                age=29,
                specialization="Engineering",
                years_experience=6,
            ),
        ],
    )

    print(f"Mission: {valid_mission.mission_name}")
    print(f"ID: {valid_mission.mission_id}")
    print(f"Destination: {valid_mission.destination}")
    print(f"Duration: {valid_mission.duration_days} days")
    print(f"Budget: ${valid_mission.budget_millions}M")
    print(f"Crew size: {len(valid_mission.crew)}")
    print("Crew members:")
    for member in valid_mission.crew:
        print(
            f"- {member.name} ({member.rank.value}) - "
            f"{member.specialization} "
        )

    print("=" * 41)
    print("Expected validation error:")

    # Ungültige Mission: kein Commander und kein Captain.
    try:
        SpaceMission(
            mission_id="M2024_FAIL",
            mission_name="Test Deep Space Mission",
            destination="Europa",
            launch_date=datetime(2028, 1, 15, 13, 0),
            duration_days=120,
            budget_millions=800.0,
            crew=[
                CrewMember(
                    member_id="CM101",
                    name="Mark Lee",
                    rank=Rank.LIEUTENANT,
                    age=31,
                    specialization="Navigation",
                    years_experience=7,
                ),
                CrewMember(
                    member_id="CM102",
                    name="Nina Park",
                    rank=Rank.OFFICER,
                    age=27,
                    specialization="Science",
                    years_experience=4,
                ),
            ],
        )
    except ValidationError as error:
        first_error = error.errors()[0]
        ctx_error = first_error.get("ctx", {}).get("error")
        if ctx_error is not None:
            print(str(ctx_error))
        else:
            print(first_error["msg"].replace("Value error, ", ""))


if __name__ == "__main__":
    demonstrate_space_crew()
