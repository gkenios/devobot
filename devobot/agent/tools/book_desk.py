import re
from typing import Annotated

from langchain_core.tools import tool, InjectedToolArg
import requests


@tool
def book_desk(
    date: str,
    people: int,
    city: str | None,
    floor: int | None,
    desk_name: str | None,
    client_id: Annotated[str, InjectedToolArg],
    client_secret: Annotated[str, InjectedToolArg],
    company_id: Annotated[str, InjectedToolArg],
    user_email: Annotated[str, InjectedToolArg],
) -> str:
    """Creates a desk reservation (or multiple) for a user on a given date.

    Args:
        date: The date of the reservation in the format "YYYY-MM-DD".
        people: The number of people to book desks for.
        city: The city where the office is located.
        floor: The floor number where the desk is located.
        desk_name: The name of the desk to book. It can be in:
          - dual monitor
          - single monitor
          - bar
          - lounge
          - round table
          The default value is single monitor.
    """
    token = get_token(client_id, client_secret)
    user_id, is_admin = get_user_id(token, company_id, user_email)
    building_id, floor_id = get_location(token, company_id, city, floor)

    if not is_admin:
        people = 1

    for _ in range(people):
        seat_id = get_desk_slots(token, building_id, floor_id, date, desk_name)
        create_desk_reservation(token, company_id, user_id, seat_id, date)
    return f"Desk(s) booked for {people} people on {date}."


# JOAN API functions
def get_token(client_id, secret):
    response = requests.post(
        "https://portal.getjoan.com/api/token/",
        data={"grant_type": "client_credentials", "scope": "read write"},
        auth=(client_id, secret),
    )
    return response.json()["access_token"]


def get_user_id(token: str, company_id: str, email: str) -> tuple[str, bool]:
    response = requests.get(
        f"https://portal.getjoan.com/api/2.0/desk/company/{company_id}/users",
        headers={"Authorization": f"Bearer {token}"},
    )
    for user in response.json():
        if user["email"] == email:
            user_id = user["id"]
            is_admin = user["groups"] != ["portal_user"]
            return (user_id, is_admin)


def get_locations(token: str, company_id: str) -> list[dict]:
    response = requests.get(
        f"https://portal.getjoan.com/api/2.0/desk/company/{company_id}/desk",
        headers={"Authorization": f"Bearer {token}"},
    ).json()

    buildings = []
    # Used [:-1] to exclude G Cloud building
    for building in response["locations"][:-1]:
        for floor in building["maps"]:
            try:
                level = int(re.search(r"\d+", floor["name"]).group())
            except AttributeError:
                level = 0
            building_data = {
                "building_id": building["id"],
                "floor_id": floor["id"],
                "floor": level,
                "city": building["address"][
                    "street"
                ].lower(),  # #devoteam_data_quality
            }
            buildings.append(building_data)
    return buildings


def get_location(
    token: str,
    company_id: str,
    city: str | None = None,
    floor: int | None = None,
) -> dict:
    all_locations = get_locations(token, company_id)
    if city:
        city = city.lower()

    for location in all_locations:
        if city and city in location["city"]:
            if floor is not None and floor != location["floor"]:
                continue
            else:
                return location["building_id"], location["floor_id"]
    return all_locations[0]["building_id"], all_locations[0]["floor_id"]


def create_desk_reservation(
    token: str,
    company_id: str,
    user_id: str,
    seat_id: str,
    date: str,
    from_time: str = "09:00",
    to_time: str = "17:00",
) -> dict:
    response = requests.post(
        f"https://portal.getjoan.com/api/2.0/desk/v2/company/{company_id}/reservation",
        json={
            "date": date,
            "from": from_time,
            "to": to_time,
            "tz": "Europe/Amsterdam",
            "seat_id": seat_id,
            "user_id": user_id,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    return response.json()


def get_desk_slots(
    token: str,
    building_id: str,
    floor_id: str,
    date: str,
    desk_name: str | None = None,
    time_from: str = "09:00",
    time_to: str = "17:00",
) -> dict:
    response = requests.get(
        "https://portal.getjoan.com/api/2.0/portal/desks/",
        params={
            "date": date,
            "from": time_from,
            "to": time_to,
            "tz": "Europe/Amsterdam",
            "building_id": building_id,
            "floor_id": floor_id,
        },
        headers={"Authorization": f"Bearer {token}"},
    ).json()
    results = response["results"]

    # No available desks
    if not results:
        return

    # If desk_name is not provided, get the first available desk
    if not desk_name:
        return results[0]["id"]

    # If desk_name is provided, get the first available desk that matches
    desk_name = desk_name.lower()
    for desk in results:
        if desk_name in desk["name"].lower():
            return desk["id"]

    # If no desk_name was matched, then get the first available desk
    return results[0]["id"]
