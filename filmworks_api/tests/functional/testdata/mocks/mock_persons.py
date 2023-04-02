from uuid import UUID

TEST_PERSONS = [
    dict(
        id=UUID('ed63a508-4f7c-4dc6-84c3-482f4d08a582'),
        full_name='Abraham Benrubi',
        films=[
            dict(
                id=UUID('830857b7-64d2-4a95-98c4-b03351daff52'),
                roles=['actor']
            ),
            dict(
                id=UUID('d1099968-805e-4a2b-a2ec-18bbde1201ac'),
                roles=['actor']
            ),
            dict(
                id=UUID('d77e45fc-2b84-442f-b652-caf31cb07c80'),
                roles=['actor']
            )
        ]
    ),
    dict(
        id=UUID('4b3662a9-bb59-46bb-b422-fda62c9891b5'),
        full_name='Aaron Barzman',
        films=[]
    ),
    dict(
        id=UUID('cbdb2ba5-39c9-4093-b2bd-95f4e62bdb6d'),
        full_name='Aaron Contreras',
        films=[]
    ),
    dict(
        id=UUID('4959e5b7-d157-4cdf-bc4f-5eb3cf8bd57f'),
        full_name='Aaron Ginn-Forsberg',
        films=[]
    ),
    dict(
        id=UUID('f00ac91a-b19a-4511-b510-fd05a4a52cbb'),
        full_name='Aaron Malchow',
        films=[]
    ),
    dict(
        id=UUID('2570419f-0ec7-4aac-8af6-f322e41e02fb'),
        full_name='Aaron de Orive',
        films=[]
    ),
    dict(
        id=UUID('e5fa268b-62ad-4d49-95e1-dbfc8df6124d'),
        full_name='Hank Aaron',
        films=[]
    )
]

RESPONSE_REFS = {
    'response_ref': {
        'uuid': 'ed63a508-4f7c-4dc6-84c3-482f4d08a582',
        'full_name': 'Abraham Benrubi',
        'films': [
            {
                'uuid': '830857b7-64d2-4a95-98c4-b03351daff52',
                'roles': [
                    'actor'
                ]
            },
            {
                'uuid': 'd1099968-805e-4a2b-a2ec-18bbde1201ac',
                'roles': [
                    'actor'
                ]
            },
            {
                'uuid': 'd77e45fc-2b84-442f-b652-caf31cb07c80',
                'roles': [
                    'actor'
                ]
            }
        ]
    },
    'films_ref': [
        {
            'uuid': '830857b7-64d2-4a95-98c4-b03351daff52',
            'title': 'Robot Chicken: Star Wars III',
            'imdb_rating': 8.1
        },
        {
            'uuid': 'd1099968-805e-4a2b-a2ec-18bbde1201ac',
            'title': 'Robot Chicken: Star Wars Episode II',
            'imdb_rating': 8.1
        },
        {
            'uuid': 'd77e45fc-2b84-442f-b652-caf31cb07c80',
            'title': 'Robot Chicken: Star Wars',
            'imdb_rating': 8.1
        }
    ]
}
