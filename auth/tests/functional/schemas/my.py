
schema_data_user = {
    '$schema': 'https://json-schema.org/draft/2020-12/schema',
    'type': 'object',
    'required': ['id', 'email', 'roles'],
    'additionalProperties': False,
    'properties': {
        'id': {
            'type': 'string',
            'format': 'uuid'
        },
        'email': {
            'type': 'string',
            'format': 'email'
        },
        'is_active': {
            'type': 'boolean'
        },
        'roles': {
            'type': 'array',
            'items': {
                'type': 'object',
                'required': ['name', 'description', 'id'],
                'properties': {
                    'id': {
                        'type': 'string',
                        'format': 'uuid'
                    },
                    'name': {
                        'type': 'string'
                    },
                    'description': {
                        'type': 'string'
                    },
                }
            }
        }
    }
}

schema_history = {
    '$schema': 'https://json-schema.org/draft/2020-12/schema',
    'type': 'object',
    'required': ['data', 'meta'],
    'additionalProperties': False,
    'properties': {
        'data': {
            'type': 'array',
            'items': {
                'type': 'object',
                'required': ['id', 'remote_addr', 'user_agent', 'user_id', 'created'],
                'additionalProperties': False,
                'properties': {
                    'id': {
                        'type': 'string',
                        'format': 'uuid'
                    },
                    'remote_addr': {
                        'type': 'string',
                        'format': 'ipv4'
                    },
                    'user_agent': {
                        'type': 'string'
                    },
                    'user_id': {
                        'type': 'string',
                        'format': 'uuid'
                    },
                    'created': {
                        'type': 'string',
                        'pattern': '202[3-9]-\d{2}-\d{2}T\d{2}:\d{2}:\d+'
                    },
                }
            }
        },
        'meta': {
            'type': 'object',
            'required': ['has_next', 'has_prev', 'next_page', 'page', 'pages', 'prev_page', 'total_count'],
            'additionalProperties': False,
            'properties': {
                'has_next': {'type': 'boolean'},
                'has_prev': {'type': ['integer', 'null']},
                'next_page': {'type': ['integer', 'null']},
                'page': {'type': 'integer'},
                'pages': {'type': 'integer'},
                'prev_page': {'type': ['integer', 'null']},
                'total_count': {'type': 'integer'}
            }
        }
    }
}

schema_allowed_devices = {
    '$schema': 'https://json-schema.org/draft/2020-12/schema',
    'type': 'array',
    'items': {
        'type': 'object',
        'required': ['id', 'user_agent', 'user_id'],
        'additionalProperties': False,
        'properties': {
            'id': {
                'type': 'string',
                'format': 'uuid'
            },
            'user_agent': {
                'type': 'string'
            },
            'user_id': {
                'type': 'string',
                'format': 'uuid'
            }
        }
    }
}
