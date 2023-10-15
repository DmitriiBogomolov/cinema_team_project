default_event = {
    'valid': {
        'initiating_service_name': 'auth_service',
        'initiating_user_id': '6b7aae84-517d-11ee-be56-0242ac120002',
        'description': 'some_description',
        'event_name': 'test_event',
        'priority': 0,
        'user_ids': ['6b7aae84-517d-11ee-be56-0242ac120002']
    },
    'invalid': [
        {
            'initiating_user_id': '6b7aae84-517d-11ee-be56-0242ac120002',
            'description': 'some_description',
            'event_name': 'test_event',
            'priority': 0,
            'user_ids': ['6b7aae84-517d-11ee-be56-0242ac120002']
        },
        {
            'initiating_service_name': 'auth_service',
            'initiating_user_id': '6b7aae84-517d-11ee-be56-0242ac120002',
            'description': 'some_description',
            'event_name': 'wrong',
            'priority': 0,
            'user_ids': ['6b7aae84-517d-11ee-be56-0242ac120002']
        }
    ]
}

manual_mailing = {
    'valid': {
        'initiating_service_name': 'auth_service',
        'initiating_user_id': '6b7aae84-517d-11ee-be56-0242ac120002',
        'description': 'some_description',
        'event_name': 'review_comment_received',
        'priority': 0,
        'user_ids': ['6b7aae84-517d-11ee-be56-0242ac120002'],
        'topic_message': 'hello',
        'email': 'Hello {{user.email}}'
    },
    'invalid': [
        {
            'initiating_user_id': '6b7aae84-517d-11ee-be56-0242ac120002',
            'description': 'some_description',
            'event_name': 'review_comment_received',
            'priority': 0,
            'user_ids': ['6b7aae84-517d-11ee-be56-0242ac120002'],
            'topic_message': 'hello',
            'email': 'Hello {{user.email}}'
        },
        {
            'initiating_service_name': 'auth_service',
            'initiating_user_id': '6b7aae84-517d-11ee-be56-0242ac120002',
            'event_name': 'review_comment_received',
            'priority': 0,
            'user_ids': ['6b7aae84-517d-11ee-be56-0242ac120002'],
            'topic_message': 'hello',
            'email': 'Hello {{user.email}}'
        }
    ]
}
