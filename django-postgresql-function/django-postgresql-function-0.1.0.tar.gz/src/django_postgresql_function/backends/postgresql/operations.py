
from django.db.backends.postgresql.operations import DatabaseOperations


# class ExtendedDatabaseOperations(DatabaseOperations):
#
#     def age_from_current_sql(self, field_name, tzname):
#         """Возвращает Возраст от текущего времени"""
#         field_name = self._convert_field_to_tz(field_name, tzname)
#
#         return "AGE('%s')" % field_name
#
#     def age_from_date_sql(self, field_name, tzname):
#         """Возвращает Возраст от"""
