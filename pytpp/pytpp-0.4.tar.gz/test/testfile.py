from pytpp import Features, Authenticate, logger
import time


logger.start()
api = Authenticate(
    host='10.100.209.41',
    username='admin',
    password='newPassw0rd!'
)

features = Features(api)
name = f'tyler_test_{time.strftime("%H%M%S")}'
print(name)
rule = features.placement_rules.create(
    name=name,
    conditions=[
        features.placement_rule_condition.country.matches('US'),
        features.placement_rule_condition.common_name.matches_regex('.*my_host\\.com'),
    ],
    device_location_dn='\VED\Policy\Certificates',
    certificate_location_dn='\VED\Policy\Devices'
)
features.placement_rules.update(
    rule=rule,
    conditions=[
        features.placement_rule_condition.hostname.matches('CA')
    ],
    rule_type='SSH',
)
