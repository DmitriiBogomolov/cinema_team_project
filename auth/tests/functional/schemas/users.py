

schema_user_output = {
    '$schema': 'https://json-schema.org/draft/2020-12/schema',
    'type': 'object',
    'required': ['id', 'email', 'password', 'is_active', 'is_superuser', 'roles', 'created', 'updated'],
    'properties': {
        'created': {
            'type': 'string',
            'pattern': '202[3-9]-\d{2}-\d{2}T\d{2}:\d{2}:\d+'
        },
        'updated': {
            'type': 'string',
            'pattern': '202[3-9]-\d{2}-\d{2}T\d{2}:\d{2}:\d+'
        },
        'password': {
            'type': 'string'
        },
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
        'is_superuser': {
            'type': 'boolean'
        },
        'roles': {
            'type': 'array',
            'items': {
                'type': 'object',
                'required': ['id', 'name', 'description'],
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
                    }
                }
            }
        }
    },
    'additionalProperties': False
}
