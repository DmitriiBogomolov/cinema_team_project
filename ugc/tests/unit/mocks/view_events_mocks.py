EVENT_MOCKS = {
    'correct': {
        "movie_id": "a0546844-18d8-11ee-be56-0242ac120002",
        "duration": 1000,
        "lenght_movie": 10000
    },
    'no_movie_id': {
        "duration": 1000,
        "lenght_movie": 10000
    },
    'no_duration': {
        "duration": 1000,
        "lenght_movie": 10000
    },
    'no_lenght_movie': {
        "movie_id": "a0546844-18d8-11ee-be56-0242ac120002",
        "duration": 1000,
    },
    'incorrect_movie_id': {
        "movie_id": "a0546844-18d8-11ee",
        "duration": 1000,
        "lenght_movie": 10000
    },
    'duration_out_of_range': {
        "movie_id": "a0546844-18d8-11ee-be56-0242ac120002",
        "duration": -100,
        "lenght_movie": 10000
    },
    'lenght_movie_out_of_range': {
        "movie_id": "a0546844-18d8-11ee-be56-0242ac120002",
        "duration": 1000,
        "lenght_movie": -10000
    },
    'icorrect_duration': {
        "movie_id": "a0546844-18d8-11ee-be56-0242ac120002",
        "duration": 100000,
        "lenght_movie": 100
    },
}
