from simple_ddl_parser import DDLParser


ddl = """
CREATE TYPE box (
    INTERNALLENGTH = 16,
    INPUT = my_box_in_function,
    OUTPUT = my_box_out_function
);
"""

result = DDLParser(ddl).run(group_by_type=True)
import pprint

pprint.pprint(result)
