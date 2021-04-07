from .base import CodeStore


class MeasureRepresentation(CodeStore):
    ABSOLUTE, ABSOLUTE_ID = 'ABSOLUTE', 'A'
    ANNUAL_PERCENTAGE_RATE, ANNUAL_PERCENTAGE_RATE_ID = 'ANNUAL_PERCENTAGE_RATE', 'N'
    INTERPERIOD_PERCENTAGE_RATE, INTERPERIOD_PERCENTAGE_RATE_ID = (
        'INTERPERIOD_PERCENTAGE_RATE',
        'I',
    )
    ANNUAL_PUNTUAL_RATE, ANNUAL_PUNTUAL_RATE_ID = 'ANNUAL_PUNTUAL_RATE', 'M'
    INTERPERIOD_PUNTUAL_RATE, INTERPERIOD_PUNTUAL_RATE_ID = (
        'INTERPERIOD_PUNTUAL_RATE',
        'J',
    )

    CODES = {
        ABSOLUTE_ID: ABSOLUTE,
        ANNUAL_PERCENTAGE_RATE_ID: ANNUAL_PERCENTAGE_RATE,
        INTERPERIOD_PERCENTAGE_RATE_ID: INTERPERIOD_PERCENTAGE_RATE,
        ANNUAL_PUNTUAL_RATE_ID: ANNUAL_PUNTUAL_RATE,
        INTERPERIOD_PUNTUAL_RATE_ID: INTERPERIOD_PUNTUAL_RATE,
    }

    UNIT_MULTIPLIER = {'MILLIONS': 1_000_000, 'THOUSANDS': 1_000, 'HUNDREDS': 100}

    @classmethod
    def get_unit_multiplier(cls, unit_multiplier_code):
        return cls.UNIT_MULTIPLIER.get(unit_multiplier_code.upper(), 1)


MeasureRepresentation.build_swapped_codes()
