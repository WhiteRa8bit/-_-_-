def filter_by_state(list_for_filter: list, state: str) -> list:
    """Принемает список словарей и возвращает новый список словарей,
    содержащий только те словари, у которых ключ state"""
    new_list = []
    for elem in list_for_filter:
        if elem.get('state') == state:
            new_list.append(elem)
    return new_list


def sort_by_date(list_for_sort: list, reverse_sort: bool = True) -> list:
    """Сортирует список словарей по ключу date. Возвращает новый список по убыванию, опционально для reverse_sort"""
    sorted_list = sorted(list_for_sort, key=lambda x: x["date"], reverse=reverse_sort)
    return sorted_list
