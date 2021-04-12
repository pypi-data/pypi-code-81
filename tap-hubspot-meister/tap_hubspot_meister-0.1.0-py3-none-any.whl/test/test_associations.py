"""associations = hubspot.crm.associations.batch_api.read(
    ObjectType.CONTACTS,
    ObjectType.COMPANIES,
    batch_input_public_object_id=BatchInputPublicObjectId(inputs=contact_ids),
)
inputs = []
if associations.results:
    for company in associations.results:
        console.log(company)
        inputs = [
            SimplePublicObjectId(id=company.id) for company in associations.results
        ]
associated_contacts = hubspot.crm.contacts.batch_api.read(
    batch_read_input_simple_public_object_id=BatchReadInputSimplePublicObjectId(
        inputs=inputs
    )
)
console.log(associated_contacts)"""
