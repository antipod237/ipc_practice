import datetime
from calendar import monthrange


class GinoQueryHelper:
    LTE = '<='
    GTE = '>='

    @staticmethod
    def pagination(query_params, current_query):
        if 'page' in query_params and 'perPage' in query_params:
            page = int(query_params['page']) - 1
            per_page = int(query_params['perPage'])
            return current_query.limit(per_page).offset(page * per_page)
        return current_query

    """
    columns_map = {
       "column_name": Model.column,
    }
    """
    @staticmethod
    def order(query_params, current_query, columns_map):
        def _get_column(column_name, asc=True):
            if asc:
                return columns_map[column_name]
            return columns_map[column_name].desc()

        if 'order' in query_params and 'field' in query_params:
            return current_query.order_by(
                _get_column(
                    query_params['field'],
                    query_params['order'] == 'ASC'
                )
            )

        return current_query

    @staticmethod
    def search(field, value, current_query, total_query):
        return (
            current_query.where(field.ilike(f'%{value}%')),
            total_query.where(field.ilike(f'%{value}%'))
        )

    @staticmethod
    def equal(field, value, current_query, total_query):
        return (
            current_query.where(field == value),
            total_query.where(field == value)
        )

    @staticmethod
    def in_(field, values, current_query, total_query,):
        return (
            current_query.where(field.in_(values)),
            total_query.where(field.in_(values))
        )

    @staticmethod
    def month_year_cond(field, value, c_type, current_query, total_query):
        custom_date = GinoQueryHelper.prepare_custom_date(value, c_type)

        if c_type == GinoQueryHelper.LTE:
            return (
                current_query.where(field <= custom_date),
                total_query.where(field <= custom_date)
            )
        else:
            return (
                current_query.where(field >= custom_date),
                total_query.where(field >= custom_date)
            )

    @staticmethod
    def prepare_custom_date(date_str, c_type=None):
        date_list = date_str.split('-')

        year = int(date_list[0])
        month = int(date_list[1])

        if len(date_list) > 2:
            day = int(date_list[2])
        elif not c_type or c_type == GinoQueryHelper.GTE:
            day = 1
        else:
            day = monthrange(year, month)[1]

        return datetime.date(year, month, day)
