from django.db.models import Func


class Age(Func):
    # TODO сделать с обработкой Timezone
    function = 'AGE'


class BaseDateDiff(Func):

    function = 'DATE_PART'
    lookup_name = None

    def __init__(self, *expressions, output_field=None, **extra):
        if len(expressions) != 2:
            raise TypeError(
                f"Должно быть перадано 2 аргумента. Передано {len(expressions)}"
            )
        super().__init__(*expressions, output_field=None, **extra)

    @property
    def template(self):
        return f"%(function)s('{self.lookup_name}', AGE(%(expressions)s))"


class YearsDateDiff(BaseDateDiff):
    lookup_name = 'year'


class MonthsDateDiff(BaseDateDiff):
    lookup_name = 'month'


class DaysDateDiff(BaseDateDiff):
    lookup_name = 'day'

