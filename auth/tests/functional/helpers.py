def clear(d: dict) -> dict:
    n = d.copy()
    if 'id' in n:
        del n['id']
    if 'created' in n:
        del n['created']
    if 'updated' in n:
        del n['updated']
    return n
