from cerberus import Validator

# gitlab model

pipeline_statuses = ['created',
                     'waiting_for_resource',
                     'preparing',
                     'pending',
                     'running',
                     'success',
                     'failed',
                     'canceled',
                     'skipped',
                     'manual',
                     'scheduled', ]

job_statuses = ['created',
                'pending',
                'running',
                'failed',
                'success',
                'canceled',
                'skipped',
                'manual', ]

environment_statuses = ['available', 'stopped']

# schemas

trigger_schema = {'project_id': {'type': 'integer', 'required': True},
                  'ref':        {'type': 'string'},
                  'branch':     {'type': 'string'}, # deprecated in favor of `ref`
                  'variables':  {'type':        'dict',
                                 'keysrules':   {'type': ['string', 'boolean', 'date', 'datetime', 'number']},
                                 'valuesrules': {'type': ['string', 'boolean', 'date', 'datetime', 'number']}
                                 }
                  }

assertions_schema = {'pipeline_status':    {'type':     'string',
                                            'allowed':  pipeline_statuses,
                                            'required': True},
                     'job_count':          {'type': 'integer'},
                     'job_status':         {'type':        'dict',
                                            'keysrules':   {'type': 'string'},
                                            'valuesrules': {'type':    'string',
                                                            'allowed': job_statuses}},
                     'artifact_count':     {'type': 'integer'},
                     'environment_status': {'type':        'dict',
                                            'keysrules':   {'type': 'string'},
                                            'valuesrules': {'type':    'string',
                                                            'allowed': environment_statuses},
                                            },
                     }

test_schema = {'trigger':    {'type': 'dict', 'schema': trigger_schema, },
               'assertions': {'type': 'dict', 'schema': assertions_schema, }, }


def validate_test(test):
    validator = Validator()
    return validator.validate(test, test_schema), validator.errors
