
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
                    'person_role', pfw.role,
                    'person_id', p.id,
                    'person_name', p.full_name
                )
            ) FILTER (WHERE p.id is not null),
            '[]'
        ) as persons,
        array_agg(DISTINCT g.name) as genres
        FROM content.film_work fw
        LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
        LEFT JOIN content.person p ON p.id = pfw.person_id
        LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
        LEFT JOIN content.genre g ON g.id = gfw.genre_id
        WHERE fw.modified >= {last_modified}
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
                    'person_role', pfw.role,
                    'person_id', p.id,
                    'person_name', p.full_name
                )
            ) FILTER (WHERE p.id is not null),
            '[]'
        ) as persons,
        array_agg(DISTINCT g.name) as genres,
        min(g.modified) as modified
        FROM content.film_work fw
        LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
        LEFT JOIN content.genre g ON g.id = gfw.genre_id
        LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
        LEFT JOIN content.person p ON p.id = pfw.person_id
        WHERE g.modified >= {last_modified}
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
                    'person_role', pfw.role,
                    'person_id', p.id,
                    'person_name', p.full_name
                )
            ) FILTER (WHERE p.id is not null),
            '[]'
        ) as persons,
        array_agg(DISTINCT g.name) as genres,
        min(p.modified) as modified
        FROM content.film_work fw
        LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
        LEFT JOIN content.genre g ON g.id = gfw.genre_id
        LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
        LEFT JOIN content.person p ON p.id = pfw.person_id
        WHERE g.modified >= {last_modified}
        GROUP BY fw.id
        ORDER BY modified;
    """
