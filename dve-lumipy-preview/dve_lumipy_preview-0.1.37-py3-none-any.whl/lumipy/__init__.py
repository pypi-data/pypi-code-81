from lumipy.navigation.atlas import Atlas
from lumipy.client import Client
from lumipy.drive.drive import Drive
from typing import Optional

from lumipy.query.expression.variable.scalar_variable import DateScalar
from lumipy.query.expression.variable.scalar_variable import DateTimeScalar


def get_client(secrets: Optional[str] = None) -> Client:
    """Get luminesce web API client instance.

    Args:
        secrets (Optional[str]): path to secrets file. If not supplied authentication information will be retrieved
        from the environment.

    Returns:
        Client: the web API client instance.
    """
    return Client(secrets)


def get_atlas(secrets: Optional[str] = None) -> Atlas:
    """Get luminesce data provider atlas instance.

    Args:
        secrets (Optional[str]): path to secrets file. If not supplied authentication information will be retrieved
        from the environment.

    Returns:
        Atlas: the atlas instance.
    """
    return Client(secrets).get_atlas()


def get_drive(lumi_secrets: Optional[str] = None, drive_secrets: Optional[str] = None) -> Drive:
    """Get drive instance.

    Args:
        lumi_secrets (Optional[str]): path to lumipy secrets file. If not supplied authentication information will be
        retrieved from the environment.
        drive_secrets (Optional[str]): path to drive secrets file. If not supplied authentication information will be
        retrieved from the environment.

    Returns:
        Drive: the drive instance.
    """
    atlas = get_atlas(lumi_secrets)
    return Drive(atlas, drive_secrets)


def datetime_now(delta_days: Optional[int] = 0) -> DateTimeScalar:
    """Get a scalar variable representing the current date with an optional offset.

    Args:
        delta_days (Optional[int]): time delta in days. Defaults to 0.

    Returns:
        DateTimeScalar: Datetime scalar variable expression.
    """
    return DateTimeScalar('now', delta_days)


def date_now(delta_days: Optional[int] = 0) -> DateScalar:
    """Get a scalar variable representing the current datetime with an optional offset.

    Args:
        delta_days (Optional[int]): time delta in days. Defaults to 0.

    Returns:
        DateScalar: Date scalar variable expression.
    """
    return DateScalar('now', delta_days)
