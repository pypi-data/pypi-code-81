from enum import Enum

class CommonFieldnames(Enum):
    """
    Common Fieldnames, that are used in many products (it not all).

    """
    policyBeginDate = "Versicherungsbeginn"
    policyEndDate = "Versicherungsende"
    mainDueDate = "Hauptfälligkeit"
    businessCaseType = "GeschäftsfallArt"
    previousPolicyNumber = "Vorpolizzennummer"
    premium = "premium"
    paymentFrequency = "Zahlungsfrequenz"
    expertMode = "Erweitern"    # "ExpertenModus"
    commissionAccount = "ProvKto"

    ## Person fields:
    Partner = "Partner"
    partnerName = "partnerName"
    partnerNumber = "partnerNumber"
    birthDate = "birthDate"
    gender = "gender"
    lastName = "lastName"
    firstName = "firstName"

    ## Company fields
    companyName = "companyName"
    companyType = "companyType"
    registrationNumber = "registrationNumber"

    ## Address fields:
    addressDict = "addressDict"
    addressID = "addressID"           # official addressID in Backend-System
    addressNumber = "addressNumber"   # Polzy-Internal, temporary addressNumber
    country = "country"
    postCode = "postCode"
    city = "city"
    street = "street"
    streetNumber = "streetNumber"
    houseNumber = "houseNumber"
    telefon = "telefon"
    email = "email"

    # Fields for "Senden-An-Bestand"
    underWriterWarnings = "AnnahmeTexte"
    policyNumber = "policyNumber"
    applicationNumber = "applicationNumber"
    pac = "pac"