from overrides_extension import final


class SomeClass(object):
    def somewhat_fun_method(self) -> str:
        """LULZ"""
        return "LOL"

    @final
    def somewhat_finalized_method(self) -> str:
        return "some_final"
