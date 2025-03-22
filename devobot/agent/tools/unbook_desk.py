from typing import Annotated

from langchain_core.tools import tool, InjectedToolArg
import requests


@tool
def unbook_desk(
    date: str,
    client_id: Annotated[str, InjectedToolArg],
    client_secret: Annotated[str, InjectedToolArg],
    company_id: Annotated[str, InjectedToolArg],
    user_email: Annotated[str, InjectedToolArg],
) -> str:
    """Deletes a desk reservation (or multiple) for a user on a given date.

    Args:
        date: The date of the reservation in the format "YYYY-MM-DD".
    """
    token = get_token(client_id, client_secret)
    user_id, _ = get_user_id(token, company_id, user_email)
    if not user_id:
        return "User not found."

    delete_desk_reservation(token, company_id, user_id, date)
    return f"Desk reservation(s) deleted for {date}."


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
    return None, False


def get_desk_reservation(
    token: str,
    company_id: str,
    user_id: str,
    date: str,
) -> list[str] | None:
    response = requests.get(
        f"https://portal.getjoan.com/api/2.0/desk/v2/company/{company_id}/reservation",
        params={
            "from": f"{date} 00:00:00",
            "to": f"{date} 23:59:59",
            "tz": "Europe/Amsterdam",
            "user_id": user_id,
        },
        headers={"Authorization": f"Bearer {token}"},
    ).json()
    if response:
        return [desk["id"] for desk in response]


def delete_desk_reservation(
    token: str,
    company_id: str,
    user_id: str,
    date: str,
) -> str | None:
    reservation_ids = get_desk_reservation(token, company_id, user_id, date)
    if not reservation_ids:
        return None

    for reservation_id in reservation_ids:
        requests.delete(
            f"https://portal.getjoan.com/api/2.0/desk/v2/reservation/{reservation_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
    return "Reservations deleted"
