#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = ["Benjamin Fuchs", "Jan Buschmann", "Felix Nitsch"]
__copyright__ = "Copyright 2020, German Aerospace Center (DLR)"
__credits__ = []

__license__ = "MIT"
__version__ = "1.0.2"
__maintainer__ = "Felix Nitsch"
__email__ = "ioProc@dlr.de"
__status__ = "Production"


general_schema = {
    'workflow': {
        'required': True,
        'type': 'list',
        'schema': {
            'type': 'dict',
            'valueschema': {
                'type': 'dict',
                'schema': {
                    'project': {
                        'type': 'string',
                        'required': True,
                    },
                    'call': {
                        'type': 'string',
                        'required': True,
                    },
                    'data': {
                        'required': False,
                    },
                    'args': {
                        'required': False,
                    },
                    'tag': {
                        'required': False,
                    },
                },
           }
        }
    },
    'actionFolder': {
        'type': 'string',
        'required': True,
    },
    'debug': {
        'type': 'dict',
        'schema': {
            'timeit': {
                'type': 'boolean',
            },
            'enable development mode': {
                'type': 'boolean',
            }
        }
    },
    'fromCheckPoint': {
        'type': ['string', 'integer'],
    }
}


action_schema = {
    'action': {
        'type': 'dict',
        'keyschema': {
            'type': 'string',
        },
        'valueschema': {
            'type': 'dict',
            'schema': {
                'project': {
                    'type': 'string',
                    'required': True,
                },
                'call': {
                    'type': 'string',
                    'required': True,
                },
                'data': {
                    'required': True,
                    'schema': {
                        'read_from_dmgr': {
                            'nullable': True,
                            'type': ['string', 'list', 'dict'],
                            'required': True,
                            'forbidden': ['None', 'none'],
                        },
                        'write_to_dmgr': {
                            'nullable': True,
                            'type': ['string', 'list', 'dict'],
                            'required': True,
                            'forbidden': ['None', 'none'],
                        },
                    }
                },
                'args': {
                    'type': 'dict',
                    'required': False,
                }
            }
        }
    }
}


checkpoint_schema = {
    'action': {
        'type': 'dict',
        'keyschema': {
            'type': 'string',
        },
        'valueschema': {
            'type': 'dict',
            'schema': {
                'project': {
                    'type': 'string',
                    'required': True,
                },
                'call': {
                    'type': 'string',
                    'required': True,
                },
                'tag': {
                    'type': ['string', 'integer'],
                    'required': True,
                }
            }
        }
    }
}
