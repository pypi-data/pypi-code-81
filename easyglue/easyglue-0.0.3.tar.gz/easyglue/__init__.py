from easyglue.EasyDynamicFrameReader import EasyDynamicFrameReader

from awsglue.context import GlueContext


def read(self):  # Have to add self since this will become a method
    return EasyDynamicFrameReader(glue_context=self)


setattr(GlueContext, 'read', read)
