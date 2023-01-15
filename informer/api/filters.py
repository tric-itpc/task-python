from datetime import datetime


def time_filter(queryset, request):
    params = request.GET
    if not params.get('start-time') and not params.get('end-time'):
        return queryset
    start = datetime(1970, 1, 1)
    end = datetime.now()
    if params.get('start-time'):
        try:
            start = datetime.fromisoformat(params.get('start-time'))
        except Exception:
            pass

    if params.get('end-time'):
        try:
            end = datetime.fromisoformat(params.get('end-time'))
        except Exception:
            pass
    return queryset.filter(time_stamp__range=(start, end))


def shifts_filter(queryset, request):
    params = request.GET
    if not params.get('shifts_only') or (
            params.get('shifts_only').lower() == 'false' or 
            '/sla' in request.path):
        return queryset

    shifts_ids = [queryset[0].id, ]
    for num, elem in enumerate(queryset):
        if num == 0:
            continue
        prev_elem = queryset[num - 1]
        if elem.status != prev_elem.status:
            shifts_ids.append(elem.id)
    return queryset.filter(id__in=shifts_ids)
