query_filmworks_by_modified_date = """
        SELECT
        fw.id,
        fw.title,
        fw.description,
        fw.rating,
        fw.type,
        fw.created,
        fw.modified,
        COALESCE (
            json_agg(
                DISTINCT jsonb_build_object(
                    'genre_id', g.id,
                    'genre_name', g.name
                )
            ) FILTER (WHERE gfw.genre_id is not null),
            '[]'
        ) as genres,
        COALESCE (
            json_agg(
                DISTINCT jsonb_build_object(
                    'person_role', pfw.role,
                    'person_id', p.id,
                    'person_name', p.full_name
                )
            ) FILTER (WHERE p.id is not null),
            '[]'
        ) as persons
        FROM content.film_work fw
        LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
        LEFT JOIN content.person p ON p.id = pfw.person_id
        LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
        LEFT JOIN content.genre g ON g.id = gfw.genre_id
        WHERE fw.modified >= {FILMWORK_ETL_filmwork_last_modified}
        GROUP BY fw.id
        ORDER BY fw.modified;
    """


query_filmworks_by_genres_modified_date = """
        SELECT
        fw.id,
        fw.title,
        fw.description,
        fw.rating,
        fw.type,
        fw.created,
        COALESCE (
            json_agg(
                DISTINCT jsonb_build_object(
                    'genre_id', g.id,
                    'genre_name', g.name
                )
            ) FILTER (WHERE gfw.genre_id is not null),
            '[]'
        ) as genres,
        COALESCE (
            json_agg(
                DISTINCT jsonb_build_object(
                    'person_role', pfw.role,
                    'person_id', p.id,
                    'person_name', p.full_name
                )
            ) FILTER (WHERE p.id is not null),
            '[]'
        ) as persons,
        min(g.modified) as modified
        FROM content.film_work fw
        LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
        LEFT JOIN content.genre g ON g.id = gfw.genre_id
        LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
        LEFT JOIN content.person p ON p.id = pfw.person_id
        WHERE g.modified >= {FILMWORK_ETL_genre_last_modified}
        GROUP BY fw.id
        ORDER BY modified;
    """


query_filmworks_by_person_modified_date = """
        SELECT
        fw.id,
        fw.title,
        fw.description,
        fw.rating,
        fw.type,
        fw.created,
        COALESCE (
            json_agg(
                DISTINCT jsonb_build_object(
                    'genre_id', g.id,
                    'genre_name', g.name
                )
            ) FILTER (WHERE gfw.genre_id is not null),
            '[]'
        ) as genres,
        COALESCE (
            json_agg(
                DISTINCT jsonb_build_object(
                    'person_role', pfw.role,
                    'person_id', p.id,
                    'person_name', p.full_name
                )
            ) FILTER (WHERE p.id is not null),
            '[]'
        ) as persons,
        min(p.modified) as modified
        FROM content.film_work fw
        LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
        LEFT JOIN content.genre g ON g.id = gfw.genre_id
        LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
        LEFT JOIN content.person p ON p.id = pfw.person_id
        WHERE g.modified >= {FILMWORK_ETL_person_last_modified}
        GROUP BY fw.id
        ORDER BY modified;
    """


query_genres_by_modified_date = """
    SELECT DISTINCT g.id, g.name, g.description, g.modified
    FROM content.genre g, content.genre_film_work gfw
    WHERE g.modified >= {GENRE_ETL_last_modified} AND gfw.genre_id = g.id
    ORDER BY g.modified, g.id;
"""


query_persons_by_modified_date = """
    SELECT p.id, p.full_name, p.modified,
    COALESCE (
        json_agg(
            DISTINCT jsonb_build_object(
                'id', pfw.film_work_id,
                'role', pfw.role
            )
        ) FILTER (WHERE pfw.id is not null),
        '[]'
    ) as films
    FROM content.person p, content.person_film_work pfw
    WHERE p.modified >= {PERSON_ETL_last_modified} AND pfw.person_id = p.id
    group by p.id
    order by p.modified, p.id;
"""
