CREATE TABLE IF NOT EXISTS views (
    id uuid PRIMARY KEY,
    user_id uuid,
    movie_id uuid,
    duration int,
    lenght_movie int,
    event_time timestamp
);
