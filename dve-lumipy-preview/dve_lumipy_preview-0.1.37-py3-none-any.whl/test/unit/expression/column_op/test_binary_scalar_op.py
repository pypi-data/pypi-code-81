import unittest

from lumipy.query.expression.column.source_column import SourceColumn
from lumipy.query.expression.sql_value_type import SqlValType, numerics
from test.test_utils import make_test_atlas


class TestColumnBinaryScalarOp(unittest.TestCase):

    def test_is_in_variants(self):

        atlas = make_test_atlas()

        appreq = atlas.lusid_logs_apprequest.get_class()()
        other = appreq.select(appreq.request_id).where(
            appreq.duration > 1000
        ).to_table_var('other')

        is_in_sql = appreq.request_id.is_in(other.select(other.request_id)).get_sql()

        test_sql = appreq.select('^').where(
            appreq.request_id.is_in(
                other.select(other.request_id)
            )
        ).get_sql()
        pass

    def test_new_scalar_op_base(self):

        atlas = make_test_atlas()
        appreq = atlas.lusid_logs_apprequest.get_class()()

        duration = appreq.duration
        test = (duration + 1) + 100
        test_sql = test.get_sql()

        self.assertEqual(test_sql, '([Duration] + 1) + 100')

    def test_is_in_with_list(self):

        atlas = make_test_atlas()
        appreq = atlas.lusid_logs_apprequest.get_class()()
        is_in_sql = appreq.application.is_in(['shrine', 'lusid']).get_sql()
        self.assertEqual(is_in_sql, "[Application] in ('shrine', 'lusid')")

    def test_membership_container(self):

        from lumipy.query.expression.column.collection import CollectionExpression

        atlas = make_test_atlas()
        appreq = atlas.lusid_logs_apprequest.get_class()()
        container1 = CollectionExpression(appreq.select(appreq.duration))
        container1_sql = container1.get_sql()
        self.assertEqual(container1_sql, "(select [Duration] from Lusid.Logs.AppRequest)")

        container2 = CollectionExpression(*["a", "b", "c"])
        container2_sql = container2.get_sql()

        self.assertEqual(container2_sql, "('a', 'b', 'c')")

    def test_is_in_prefixing_reconstruction(self):

        atlas = make_test_atlas()
        appreq = atlas.lusid_logs_apprequest.get_class()()
        rtrace = atlas.lusid_logs_requesttrace.get_class()()

        appreq_alias = appreq.with_alias('test')
        rtrace_alias = rtrace.with_alias('RT')

        is_in = appreq.application.is_in(['shrine', 'lusid'])
        prfx_is_in = appreq_alias.apply_prefix(is_in)

        sql_prfx_is_in = prfx_is_in.get_sql()
        self.assertEqual(sql_prfx_is_in, "test.[Application] in ('shrine', 'lusid')")

        rids = appreq.select('*').where(appreq.duration > 10000).to_table_var('rids').with_alias('RIDS')

        cndn = rtrace.request_id.is_in(rids.select(rids.request_id))
        prfx_cndn = rids.apply_prefix(rtrace_alias.apply_prefix(cndn))

        prfx_cndn_sql = prfx_cndn.get_sql()
        self.assertEqual(prfx_cndn_sql, 'RT.[RequestId] in (select RIDS.[RequestId] from @rids as RIDS)')

    # noinspection SpellCheckingInspection
    def test_numeric_binary_op_source_and_literal_cols(self):

        atlas = make_test_atlas()
        const = 2.0
        test_ops = {
            'mul': lambda x: x * const,
            'div': lambda x: x / const,
            'add': lambda x: x + const,
            'sub': lambda x: x - const,
            'mod': lambda x: x % const,
        }

        for p_description in atlas.list_providers():

            p_hash = hash(p_description)

            for c_description in p_description.list_columns():

                if c_description.data_type in numerics:
                    for name, op in test_ops.items():
                        col = SourceColumn(c_description, p_hash)
                        expr = op(col)

                        self.assertTrue(name in expr.get_name())
                        self.assertEqual(expr.source_table_hash(), col.source_table_hash())
                        self.assertEqual(len(expr.get_lineage()), 2)

                if c_description.data_type == SqlValType.Text:
                    col = SourceColumn(c_description, p_hash)
                    expr = col.concat('_ABCD')

                    self.assertTrue('_conc_' in expr.get_name())
                    self.assertEqual(expr.source_table_hash(), col.source_table_hash())
                    self.assertEqual(len(expr.get_lineage()), 2)

    def test_numeric_binary_op_two_source_cols(self):

        atlas = make_test_atlas()

        test_ops = {
            'mul': lambda x, y: x * y,
            'div': lambda x, y: x / y,
            'add': lambda x, y: x + y,
            'sub': lambda x, y: x - y,
            'mod': lambda x, y: x % y,
        }

        for p_description in atlas.list_providers():
            p_hash = hash(p_description)
            numeric_fields = [SourceColumn(c, p_hash) for c in p_description.list_columns() if c.data_type in numerics]
            for col1 in numeric_fields:
                for col2 in numeric_fields:
                    for name, op in test_ops.items():
                        expr = op(col1, col2)
                        self.assertTrue(name in expr.get_name())
                        self.assertEqual(expr.source_table_hash(), col1.source_table_hash())
                        self.assertEqual(len(expr.get_lineage()), 2)

    def test_degenerate_expression_args_bug(self):

        atlas = make_test_atlas()
        provider1 = atlas.lusid_logs_apprequest.get_class()()
        provider2 = atlas.lusid_logs_apprequest.get_class()()
        v1 = provider1.duration / 2
        v2 = provider2.duration / 2

        v3 = v1 + v2
        self.assertEqual(v3.get_sql(), f"({v1.get_sql()}) + ({v2.get_sql()})")
