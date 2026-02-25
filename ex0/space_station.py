from __future__ import annotations

from datetime import datetime
from typing import Optional
# Sicherstellen, dass pydantic installiert ist mit pip install pydantic
# oder mit brew install pydantic, wenn Homebrew verwendet wird.
from pydantic import BaseModel, Field ,ValidationError

    
class SpaceStation(BaseModel):

    station_id: str = Field(..., min_length=3,
                            max_length=10, alias='id')
    name: str = Field(..., min_length=1, max_length=50)
    crew_size: int = Field(..., ge=0.0, le=1000.0)
    power_level: float = Field(..., ge=0.0, le=100.0)
    oxygen_level: float = Field(..., ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: Optional[str] = Field(default=None, max_length=200)


def main():
    print("Space Station Data Validation Example")
    print("=" * 40)


    station = SpaceStation(
        id="ISS001",
        name="International Space Station",
        crew_size=6,
        power_level=85.5,
        oxygen_level=92.3,
        last_maintenance="2026-02-20T12:30:00",
        notes="All systems nominal."
        )

    print("Valid Space Station created successfully:")
    print(f"ID: {station.station_id}")
    print(f"Name: {station.name}")
    print(f"Crew Size: {station.crew_size}")
    print(f"Power Level: {station.power_level}%")
    print(f"Oxygen Level: {station.oxygen_level}%")
    print(f"Last Maintenance: {station.last_maintenance}")
    print(f"Notes: {station.notes}")

    print("=" * 40)

    try:
        SpaceStation(
            station_id="BAD001",
            name="Broken Station",
            crew_size=21,
            power_level=50.0,
            oxygen_level=50.0,
            last_maintenance=datetime.now(),
        )
    except ValidationError as e:
        print("Validation error occurred while creating a space station:")
        print(e)


if __name__ == "__main__":
    main()
