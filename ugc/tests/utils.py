def compare(d1: dict | list, d2: dict | list) -> bool:
    if not isinstance(d1, d2):
        return False
    elif isinstance(d1, dict):
        return (
            {k: v for k, v in d1.items() if k not in ('_id', 'created_at')}
            ==
            {k: v for k, v in d2.items() if k not in ('_id', 'created_at')}
        )
    elif isinstance(d1, list):
        d1 = [{k: v for k, v in d.items() if k not in ('_id', 'created_at')}
              for d in d1]

        d2 = [{k: v for k, v in d.items() if k not in ('_id', 'created_at')}
              for d in d2]

        if len(d1) != len(d2):
            return False

        return all(d in d2 for d in d1)
