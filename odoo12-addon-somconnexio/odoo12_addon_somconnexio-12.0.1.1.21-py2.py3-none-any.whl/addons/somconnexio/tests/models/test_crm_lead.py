from ..sc_test_case import SCTestCase


class CRMLeadTest(SCTestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)

        self.partner_id = self.browse_ref('somconnexio.res_partner_2_demo')
        self.crm_lead_iban = 'ES6000491500051234567891'
        self.crm_lead = self.env['crm.lead'].create(
            [{
                'name': 'Test Lead',
                'partner_id': self.partner_id.id,
            }]
        )

    def test_crm_lead_action_set_won(self):
        self.assertNotEqual(self.crm_lead.stage_id, self.browse_ref('crm.stage_lead4'))
        self.crm_lead.action_set_won()
        self.assertEquals(self.crm_lead.stage_id, self.browse_ref('crm.stage_lead4'))

    def test_ensure_crm_lead_iban_in_partner(self):
        self.crm_lead.write({'iban': self.crm_lead_iban})

        self.assertEquals(len(self.partner_id.bank_ids), 1)
        self.assertNotEqual(self.crm_lead_iban,
                            self.partner_id.bank_ids[0].sanitized_acc_number)

        self.crm_lead.action_set_won()

        self.assertEquals(len(self.partner_id.bank_ids), 2)
        self.assertEquals(self.crm_lead_iban,
                          self.partner_id.bank_ids[1].sanitized_acc_number)

    def test_crm_lead_partner_email(self):
        self.assertEquals(self.crm_lead.email_from, self.partner_id.email)

    def test_crm_lead_subscription_request_email(self):
        subscription_request_id = self.browse_ref(
            'somconnexio.sc_subscription_request_2_demo')

        crm_lead = self.env['crm.lead'].create(
            [{
                'name': 'New Test Lead',
                'subscription_request_id': subscription_request_id.id,
            }]
        )
        self.assertEquals(crm_lead.email_from, subscription_request_id.email)

    def test_crm_lead_new_email(self):
        new_email = "new.email@demo.net"
        crm_lead = self.env['crm.lead'].create(
            [{
                'name': 'New Test Lead',
                'partner_id': self.partner_id.id,
                'email_from': new_email,
            }]
        )
        self.assertEquals(crm_lead.email_from, new_email)
