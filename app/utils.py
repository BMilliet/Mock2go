
def is_same_route(path1, path2):
    path2 = path2.split('/')
    path1 = path1.split('/')
    if len(path1) != len(path2):
        return False
    diff_list = list(set(path2).difference(path1))
    return len(diff_list) == 1 and diff_list[0] == 'PARAMETER'


def search_path_in(searched_path, paths):

    paths = sorted(paths, key=str.lower)

    start = 0
    end = len(paths) - 1

    while start <= end:

        middle = int((start + end) / 2)
        list_mid = paths[middle]

        if list_mid > searched_path:
            end = middle - 1
        elif list_mid < searched_path:
            start = middle + 1
        else:
            return list_mid


def search_path_with_param_in(searched_path, paths):

    paths = sorted(paths, key=str.lower)

    start = 0
    end = len(paths) - 1

    while start <= end:

        middle = int((start + end) / 2)
        list_mid = paths[middle]

        if is_same_route(searched_path, list_mid):
            return list_mid

        if _has_substring(list_mid, searched_path):
            return _range_search(len(paths), middle, searched_path, paths)

        if list_mid > searched_path:
            end = middle - 1
        elif list_mid < searched_path:
            start = middle + 1
        else:
            return list_mid


def _range_search(max_len, first_occurence, searched_path, paths):

    for p in paths[first_occurence:max_len]:
        if not _has_substring(p, searched_path):
            break

        if is_same_route(searched_path, p):
            return p

    for p in reversed(paths[0:first_occurence]):
        if not _has_substring(p, searched_path):
            break

        if is_same_route(searched_path, p):
            return p

    return None


def _has_substring(string1, string2):
    return string2.split('/')[0] in string1.split('PARAMETER')[0]
