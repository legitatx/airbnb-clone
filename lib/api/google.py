import googlemaps
from os import getenv
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow

maps = googlemaps.Client(getenv("GOOGLE_GEOCODE_KEY"))

flow = Flow.from_client_secrets_file(
    "../../client_secret.json",
    scopes=[
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
    ],
)
flow.redirect_uri = "https://ryanbnb.herokuapp.com/login"


def generate_auth_url():
    url, state = flow.authorization_url(
        access_type="online", include_granted_scopes="true"
    )
    return url


def login(code: str):
    flow.fetch_token(code=code)
    credentials = flow.credentials

    peopleApi = build("people", "v1", credentials=credentials)
    profile = peopleApi.people().get(
        "people/me", personFields="emailAddresses,names,photos"
    )
    return profile


async def geocode(address: str):
    results = await maps.geocode(address)
    return parse_address(results[0]["address_components"])


def parse_address(address_components):
    country = ""
    admin = ""
    city = ""

    for components in address_components:
        for component in components:
            types = component["types"]

            if "country" in types:
                country = component["long_name"]
            if "administrative_area_level_1" in types:
                admin = component["long_name"]
            if "locality" in types or "postal_town" in types:
                city = component["long_name"]

            return {"country": country, "admin": admin, "city": city}
