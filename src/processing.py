def filter_by_state(list_for_filter: list, state: str) -> list:
    """Принемает список словарей и возвращает новый список словарей,
    содержащий только те словари, у которых ключ state"""
    new_list = []
    for elem in list_for_filter:
        if elem.get("state") == state:
            new_list.append(elem)
    return new_list
