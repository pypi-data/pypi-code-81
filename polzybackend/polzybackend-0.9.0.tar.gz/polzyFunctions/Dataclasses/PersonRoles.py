from dataclasses import dataclass


@dataclass()
class Role:
    role: str
    roleName: str


@dataclass()
class Roles:
    """
    Role short texts and long texts
    """
    # Versicherungsnehmer, Policyholder. Usually only one, but may be multiple persons or companies
    VN = Role("VN", "Policy holder")

    # Prämienzahler, Premium Payer
    PZ = Role("PZ", "Premium payer")

    # Versicherte Person, Insured Person. Depending on the product and tarif variant may be mutiple persons.
    VP = Role("VP", "Insured person")

    # Betriebsleiter, Head of department (only valid in BUFT) and not a real role in the backend, more
    # like a special kind of role "VP".
    BL = Role("BL", "Operations manager")

    # Beauftragter, Assignee (various forms of people who act in place of the VN)
    BA = Role("BA", "Representative")