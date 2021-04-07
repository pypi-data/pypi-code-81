def chunk_queryset(source_qs, chunk_size, query_log=None):
    """
    Yield pages of a queryset.
    """
    pk = None
    has_fields = hasattr(source_qs, "_fields") and source_qs._fields
    if has_fields:
        if "pk" not in source_qs._fields:
            raise Exception("The values() call must include the `pk` field")  # noqa

    field = source_qs.model._meta.pk
    # set the correct field name:
    # for ForeignKeys, we want to use `model_id` field, and not `model`,
    # to bypass default ordering on related model
    order_by_field = field.attname

    source_qs = source_qs.order_by(order_by_field)
    queryset = source_qs
    while True:
        if pk:
            queryset = source_qs.filter(pk__gt=pk)
        page = queryset[:chunk_size]
        if query_log is not None:
            query_log.write("{page.query}\n".format(page=page))
        page = list(page)
        nb_items = len(page)

        if nb_items == 0:
            return

        last_item = page[-1]
        # source_qs._fields exists *and* is not none when using "values()"
        if has_fields:
            pk = last_item["pk"]
        else:
            pk = last_item.pk

        yield page

        if nb_items < chunk_size:
            return
