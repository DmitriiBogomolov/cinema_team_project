
schema_role_output = {
    '$schema': 'https://json-schema.org/draft/2020-12/schema',
    '$id': 'https://localhost:5000/schema/role',
    'type': 'object',
    'required': ['created', 'description', 'id', 'name', 'updated'],
    'additionalProperties': False,
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
        'created': {
            'type': 'string',
            'pattern': '202[3-9]-\d{2}-\d{2}T\d{2}:\d{2}:\d+'
        },
        'updated': {
            'type': 'string',
            'pattern': '202[3-9]-\d{2}-\d{2}T\d{2}:\d{2}:\d+'
        }
    }
}

schema_list_roles = {
    '$schema': 'https://json-schema.org/draft/2020-12/schema',
    '$id': 'https://localhost:5000/schema/list_roles',
    'type': 'array',
    'items': {
        'type': 'object',
        'required': ['created', 'description', 'id', 'name', 'updated'],
        'additionalProperties': False,
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
            'created': {
                'type': 'string',
                'pattern': '202[3-9]-\d{2}-\d{2}T\d{2}:\d{2}:\d+'
            },
            'updated': {
                'type': 'string',
                'pattern': '202[3-9]-\d{2}-\d{2}T\d{2}:\d{2}:\d+'
            }
        }
    }
}
