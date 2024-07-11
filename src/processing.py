def filter_by_state(list_for_filter: list, state: str = 'EXECUTED') -> list:
    """Принемает список словарей и возвращает новый список словарей,
    содержащий только те словари, у которых ключ state"""
    new_list = []
    for elem in list_for_filter:
        if elem.get("state") == state:
            new_list.append(elem)
    return new_list


def sort_by_date(list_for_sort: list, ascending: bool = True) -> list:
    """Сортирует список словарей по ключу date. Возвращает новый список по убыванию, опционально для ascending"""
    sorted_list = sorted(list_for_sort, key=lambda x: x["date"], reverse=ascending)
    return sorted_list
