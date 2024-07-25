def filter_by_state(list_for_filter: list, state: str = "EXECUTED") -> list:
    if not all(isinstance(elem, dict) for elem in list_for_filter):
        raise ValueError("Список должен содержать только словари.")

    new_list = []
    for elem in list_for_filter:
        if elem.get("state") == state:
            new_list.append(elem)
    return new_list


def sort_by_date(list_for_sort: list, ascending=True) -> list:
    if not all(isinstance(elem, dict) for elem in list_for_sort):
        raise ValueError("Список должен содержать только словари.")
    if not all("date" in elem for elem in list_for_sort):
        raise ValueError("В каждом словаре должно быть поле 'date'.")

    sorted_list = sorted(list_for_sort, key=lambda x: x["date"], reverse=not ascending)
    return sorted_list
