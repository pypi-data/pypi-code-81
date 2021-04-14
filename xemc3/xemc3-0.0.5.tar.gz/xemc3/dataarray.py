# Without having the coordinates fixed, there is no point working on xr.da
# @xr.register_dataarray_accessor("emc3")
# class EMC3DataarrayAccessor:
#     def __init__(self, da):
#         self.data = da
#         self.metadata = da.attrs.get("metadata")  # None if just grid file
#         self.load = load
