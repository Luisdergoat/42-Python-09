"""Exercise 1: Alien Contact Logs.

Simple Pydantic model with custom business validation.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, ValidationError, model_validator


class ContactType(str, Enum):
    """Possible types of alien contact."""

    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    """Represents a contact report with custom business rules."""

    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def validate_business_rules(self) -> "AlienContact":
        """Validate complex rules after all fields are parsed."""
        # Wichtige Business-Regel: Contact IDs starten immer mit "AC".
        if not self.contact_id.startswith("AC"):
            raise ValueError('Contact ID must start with "AC"')

        # Physischer Kontakt muss extra geprüft/verifiziert sein.
        if self.contact_type == ContactType.PHYSICAL and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")

        # Telepathischer Kontakt braucht mindestens 3 Zeugen.
        if (
            self.contact_type == ContactType.TELEPATHIC
            and self.witness_count < 3
        ):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
            )

        # Starke Signale sollen immer eine Nachricht enthalten.
        if self.signal_strength > 7.0:
            if self.message_received is None:
                raise ValueError(
                    "Strong signals (> 7.0) should include received messages"
                )
            if not self.message_received.strip():
                raise ValueError(
                    "Strong signals (> 7.0) should include received messages"
                )

        return self


def demonstrate_contact_logs() -> None:
    """Show one valid and one invalid contact report."""
    print("\nAlien Contact Log Validation")
    print("=" * 38)

    # Gültiger Datensatz: dieser Teil sollte funktionieren.
    print("Valid contact report:")
    valid_contact = AlienContact(
        contact_id="AC_2024_001",
        timestamp=datetime(2024, 7, 21, 23, 45),
        location="Area 51, Nevada",
        contact_type=ContactType.RADIO,
        signal_strength=8.5,
        duration_minutes=45,
        witness_count=5,
        message_received="!Greetings from Zeta Reticuli!",
    )

    print(f"ID: {valid_contact.contact_id}")
    print(f"Type: {valid_contact.contact_type.value}")
    print(f"Location: {valid_contact.location}")
    print(f"Signal: {valid_contact.signal_strength}/10")
    print(f"Duration: {valid_contact.duration_minutes} minutes")
    print(f"Witnesses: {valid_contact.witness_count}")
    print(f"Message: {valid_contact.message_received}")
    print("=" * 38)

    # Ungültiger Datensatz: hier provozieren wir bewusst einen Fehler.
    print("Expected validation error:")
    try:
        AlienContact(
            contact_id="AC_2024_099",
            timestamp=datetime(2024, 7, 22, 0, 10),
            location="Mount Shasta",
            contact_type=ContactType.TELEPATHIC,
            signal_strength=6.1,
            duration_minutes=20,
            witness_count=2,
        )
    except ValidationError as error:
        first_error = error.errors()[0]
        ctx_error = first_error.get("ctx", {}).get("error")
        if ctx_error is not None:
            print(str(ctx_error))
        else:
            print(first_error["msg"].replace("Value error, ", ""))


if __name__ == "__main__":
    demonstrate_contact_logs()
