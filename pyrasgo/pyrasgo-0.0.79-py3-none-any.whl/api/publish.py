import pandas as pd
from pathlib import Path
from typing import List, Optional
import yaml

from .connection import Connection
from .error import APIError, ParameterValueError
from .create import Create
from .get import Get
from .match import Match
from .save import Save
from .update import Update


from pyrasgo.primitives.enums import Granularity, ModelType
from pyrasgo.primitives.collection import Collection
from pyrasgo.primitives.feature import Feature, FeatureList
from pyrasgo.primitives.feature_set import FeatureSet
from pyrasgo.primitives.source import DataSource
from pyrasgo.storage import DataWarehouse, SnowflakeDataWarehouse
from pyrasgo.utils import dataframe, ingestion, naming
from pyrasgo.utils.monitoring import track_usage
from pyrasgo import schemas as api


class Publish(Connection):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_warehouse: SnowflakeDataWarehouse = DataWarehouse.connect()
        self.get = Get(api_key=self._api_key)
        self.match = Match(api_key=self._api_key)
        self.create = Create(api_key=self._api_key)
        self.update = Update(api_key=self._api_key)
        self.save = Save(api_key=self._api_key)

    @track_usage
    def features(self, features_dict: dict) -> FeatureSet:
        f"""
        Creates or updates Features based on metadata provided in the dict

        params:
            features_dict: Valid Rasgo dict (see below)

        return:
            Rasgo FeatureSet

        Valid Rasgo dict format:
        -----------------------
        {ingestion.RASGO_DICT}
        """
        # TODO need to publish docs on granularity and data types
        return self.save.feature_set_dict(features_dict)

    @track_usage
    def features_from_df(self, 
                         df: pd.DataFrame, 
                         dimensions: List[str], 
                         features: List[str],
                         granularity: List[str] = [], 
                         tags: List[str] = [], 
                         sandbox: bool = True) -> FeatureSet:
        """
        Creates a Feature Set from a pandas dataframe

        :dataframe: Pandas DataFrame containing all columns that will be registered with Rasgo
        :param dimensions: List of columns in df that should be used for joins to other featursets
        :param features: List of columns in df that should be registered as features in Rasgo
        :param granularity: List of grains that describe the form of the data. Common values are: 'day', 'week', 'month', 'second'
        :param tags: List of tags to be added to all features in the df
        :return: description of the featureset created
        """
        # Type checking
        if not isinstance(dimensions, list) and all([isinstance(dimension, str) for dimension in dimensions]):
            raise TypeError('Dimensions must be provided as a list of strings, naming the columns within the dataframe')
        if not isinstance(features, list) and all([isinstance(feature, str) for feature in features]):
            raise TypeError('Features must be provided as a list of strings, naming the columns within the dataframe')
        if not isinstance(granularity, list):
            if isinstance(granularity, str):
                granularity = [granularity]
            else:
                raise TypeError("granularity must be provided as a list of strings")
        if not isinstance(tags, list):
            if isinstance(tags, str):
                tags = [tags]
            else:
                raise TypeError("tags must be provided as a list of strings")
        if len(granularity) > len(dimensions):
            raise APIError("Number of granularities cannot exceed number of dimensions." 
                           "Dimensions are the index fields your data should join on and group by."
                           "Granularity is an attribute that describes precision of your dimensions."
                           "Consider passing more dimensions or fewer granularities.")

        org_id = self._profile.get('organizationId', None)
        timestamp = naming.make_timestamp()
        featureset_name = f"pandas_by_{'_'.join(dimensions)}_{timestamp}"
        data_source = self.save.data_source(name="PANDAS", table=featureset_name, domain="PANDAS", source_type="DataFrame")

        # Convert all strings to work with Snowflake
        # Confirm each named dimension and feature exists in the dataframe.
        dataframe.confirm_df_columns(df, dimensions, features)

        # Create a table in the data warehouse with the subset of columns we want, name table after featureset.
        all_columns = dimensions + features
        exportable_df = df[all_columns].copy()
        self.data_warehouse.write_dataframe_to_table(exportable_df, table_name=featureset_name)
        self.data_warehouse.grant_table_ownership(table=featureset_name, role=self.data_warehouse.publisher_role)
        self.data_warehouse.grant_table_access(table=featureset_name, role=self.data_warehouse.reader_role)

        # Add a reference to the FeatureSet
        featureset = self.create.feature_set(name=featureset_name, data_source_id=data_source.id,
                                             table_name=featureset_name, organization_id=org_id, granularity=', '.join(granularity),
                                             file_path=None)
        schema = dataframe.build_schema(df)

        # Add references to all the dimensions
        for d in dimensions:
            column = schema[d]
            data_type = column["type"]
            dimension_name = column["name"]
            dim_granularity = granularity.pop(0) if len(granularity) > 1 else granularity[0]
            self.save.dimension(organization_id=org_id, feature_set_id=featureset.id, name=dimension_name, data_type=data_type, dimension_type=None, granularity=dim_granularity)

        # Add references to all the features
        tags.append("Pandas")
        for f in features:
            column = schema[f]
            data_type = column["type"]
            code = column["name"]
            feature_name = f"PANDAS_{code}_{timestamp}"
            status = "Sandboxed" if sandbox else "Productionized"
            self.save.feature(organization_id=org_id, feature_set_id=featureset.id, name=feature_name, data_type=data_type, code=code, description=None, granularity=granularity[0], status=status, tags=tags, git_repo=None)
        
        self.create.feature_set_stats(featureset.id)
        return self.get.feature_set(featureset.id)

    @track_usage
    def features_from_source(self, 
                             data_source_id: int,
                             features: List[str], 
                             dimensions: List[str], 
                             granularity: List[str] = [], 
                             tags: List[str] = [],
                             feature_set_name: str = None,
                             sandbox: bool = True, 
                             if_exists: str = 'fail') -> FeatureSet:
        """
        Publishes a FeatureSet from an existing DataSource table

        params:
            data_source_id: ID to a Rasgo DataSource
            features: List of column names that will be features
            dimensions: List of column names that will be dimensions
            granularity: List of grains that describe the form of the data. Common values are: 'day', 'week', 'month', 'second'
            tags: List of tags to be added to all features
            feature_set_name: Optional name for the FeatureSet (if not passed a random string will be assigned)

            if_exists:  fail - returns an error message if a featureset already exists against this table
                        return - returns the featureset without operating on it
                        edit - edits the existing featureset
                        new - creates a new featureset

        return:
            Rasgo FeatureSet
        """
        # V1 Trade-offs / Possible Future Enhancements
        # --------------
        # Constucting a featureset using v0 method - cut over to v1
        # We aren't adding display names, descriptions to features
        # Do we allow running a script agasint the data_source table in this step?

        # Check for valid DataSource
        data_source = self.get.data_source(data_source_id)
        if not data_source.table:
            raise ValueError(f"DataSource {data_source_id} is not usable. Please make sure it exists and has a valid table registered.")
        if not isinstance(dimensions, list) and all([isinstance(dimension, str) for dimension in dimensions]):
            raise TypeError('Dimensions must be provided as a list of strings.')
        if not isinstance(features, list) and all([isinstance(feature, str) for feature in features]):
            raise TypeError('Features must be provided as a list of strings.')
        if not isinstance(granularity, list):
            if isinstance(granularity, str):
                granularity = [granularity]
            else:
                raise TypeError("granularity must be provided as a list of strings")
        if not isinstance(tags, list):
            if isinstance(tags, str):
                tags = [tags]
            else:
                raise TypeError("tags must be provided as a list of strings")
        if len(granularity) > len(dimensions):
            raise APIError("Number of granularities cannot exceed number of dimensions." 
                           "Dimensions are the index fields your data should join on and group by."
                           "Granularity is an attribute that describes precision of your dimensions."
                           "Consider passing more dimensions or fewer granularities.")

        db = data_source.tableDatabase.upper() if data_source.tableDatabase else None 
        schema = data_source.tableSchema.upper() if data_source.tableSchema else None
        table = data_source.table.split(".")[-1] if data_source.table.count(".") > 0 else data_source.table
        
        # Handle if FeatureSet already exists
        feature_set = self.match.feature_set(table_name=table)
        if feature_set and if_exists == 'fail':
            raise APIError(f"A featureset ({feature_set.id} - {feature_set.name}) is already built against this table. "
                            "Pass parameter if_exists = 'edit', 'new', or 'return' to continue.")
        
        columns = self.data_warehouse.get_source_columns(table=table, database=db, schema=schema)
        if columns.empty:
            raise APIError("The table associated with this DataSource is not accessible.")
        dataframe.confirm_list_columns(columns["COLUMN_NAME"].values.tolist(), dimensions, features)

        # Publish Featureset V0
        timestamp = naming.make_timestamp()
        org_id = self._profile.get("organizationId") 
        feature_set = self.save.feature_set(name=feature_set_name or data_source.name+"_"+timestamp,
                                                      data_source_id=data_source.id,
                                                      table_name=data_source.table,
                                                      granularity=', '.join(granularity),
                                                      organization_id=org_id,
                                                      if_exists=if_exists)

        for _i, row in columns.iterrows():
            if row["COLUMN_NAME"] in dimensions:
                dim_granularity = granularity.pop(0) if len(granularity) > 1 else granularity[0]
                self.save.dimension(organization_id=org_id,
                                              feature_set_id=feature_set.id,
                                              name=row["COLUMN_NAME"],
                                              data_type=naming._snowflakify_data_type(row["DATA_TYPE"]),
                                              granularity=dim_granularity,
                                              if_exists=if_exists)
            
            if row["COLUMN_NAME"] in features:
                self.save.feature(organization_id=org_id,
                                            feature_set_id=feature_set.id,
                                            name=row["COLUMN_NAME"],
                                            data_type=naming._snowflakify_data_type(row["DATA_TYPE"]),
                                            description=f"Feature {row['COLUMN_NAME']} created from DataSource {data_source.table}",
                                            code=row["COLUMN_NAME"],
                                            granularity=granularity[0],
                                            tags=tags,
                                            status="Sandboxed" if sandbox else "Productionized",
                                            if_exists=if_exists)

        self.create.feature_set_stats(feature_set.id)
        return self.get.feature_set(feature_set.id)

    @track_usage
    def features_from_yml(self, 
                          yml_file: str, 
                          sandbox: Optional[bool] = True, 
                          git_repo: Optional[str] = None) -> FeatureSet:
        """
        Publishes metadata about a FeatureSet to Pyrasgo

        :param yml_file: Rasgo compliant yml file that describes the featureset(s) being created
        :param sandbox: Status of the features (True = 'Sandboxed' | False = 'Productionized')
        :param git_repo: Filepath string to these feature recipes in git
        :return: description of the featureset created
        """
        with open(yml_file) as fobj:
            contents = yaml.load(fobj, Loader=yaml.SafeLoader)
        if isinstance(contents, list):
            raise APIError("More than one feature set found, please pass in only one feature set per yml")
        else:
            feature_set = self.save.feature_set_dict(contents)
        return feature_set

    @track_usage
    def source_data(self, 
                    source_type: str, 
                    file_path: Optional[Path] = None, 
                    df: Optional[pd.DataFrame] = None, 
                    table: Optional[str] = None, table_database:Optional[str] = None, table_schema: Optional[str] = None,
                    data_source_name: Optional[str] = None, data_source_domain: Optional[str] = None, 
                    data_source_table_name: Optional[str] = None, parent_data_source_id: Optional[int] = None, 
                    if_exists: Optional[str] = 'fail'
                    ) -> DataSource:
        """
        Push a csv, Dataframe, or table to a Snowflake table and register it as a Rasgo DataSource (TM)

        NOTES: csv files will import all columns as strings

        params:
            source_type: Values: ['csv', 'dataframe', 'table']
            df: pandas DataFrame (only use when passing source_type = 'dataframe')
            file_path: full path to a file on your local machine (only use when passing source_type = 'csv')
            table: name of a valid Snowflake table in your Rasgo account (only use when passing source_type = 'table')
            table_database: Optional: name of the database of the table passed in 'table' param (only use when passing source_type = 'table')
            table_schema: Optional: name of the schema of the table passed in 'table' param (only use when passing source_type = 'table')
            
            data_source_name: Optional name for the DataSource (if not provided a random string will be used)
            data_source_table_name: Optional name for the DataSource table in Snowflake (if not provided a random string will be used)
            data_source_domain: Optional domain for the DataSource (default is NULL)
            parent_data_source_id: Optional ID of a valid Rasgo DataSource that is a parent to this DataSource (default is NULL)

            if_exists: Values: ['fail', 'append', 'replace'] directs the function what to do if a DataSource already exists with this table name  (defaults to fail)

        return:
            Rasgo DataSource
        """
        # V1 Trade-offs / Possible Future Enhancements
        # --------------
        # csv's upload with all columns as string data type
        # uploading csv locally vs. calling the post/data-source/csv endpoint

        # Validate inputs
        vals = ["csv", "dataframe", "table"]
        if source_type.lower() not in vals:
            raise ParameterValueError("sourceType", vals)
        if source_type.lower() == "csv" and not Path(file_path).exists():
            raise FileNotFoundError("Please pass in a valid file path using the file_path parameter")
        if source_type.lower() == "dataframe" and df.empty:
            raise ImportError("Please pass in a valid DataFrame using the df parameter")
        if source_type.lower() == "table":
            if not table:
                raise ValueError("Please pass in a valid table using the table parameter")
            try:
                src_table = self.data_warehouse.get_source_table(table_name=table, database=table_database, schema=table_schema, record_limit=10)
                if src_table.empty:
                    raise APIError(f"Source table {table} is empty or this role does not have access to it.")
            except:
                raise APIError(f"Source table {table} does not exist or this role does not have access to it.")
        if data_source_table_name == "":
            raise ParameterValueError("data_source_table_name", "a valid SQL table name")

        # Determine the source table based on user inputs
        if source_type in ["csv", "dataframe"]:
            table_name = data_source_table_name or naming.random_table_name()
        else: #source_type == "table":
            table_name = table
        table_name = table_name.upper()
        table_database = table_database if table == table_name else None
        table_schema = table_schema if table == table_name else None
       
        # Check if a DataSource already exists
        data_source = self.match.data_source(table=table_name)
        if data_source:
            # If it does, override to the existing table
            table_name = data_source.table
            table_database = data_source.tableDatabase
            table_schema = data_source.tableSchema
            
            # Then handle input directives
            vals = ["append", "fail", "replace"]
            msg = f"DataSource {data_source.id} already exists. "
            if data_source.organizationId != self._profile.get('organizationId'):
                raise APIError(msg+"This API key does not have permission to replace it.")
            if data_source.sourceType != source_type:
                raise APIError(msg+"Your input parameters would edit the source_type. To change DataSource attributes, use the update_data_source method. To update this source table, ensure your input parameters match the DataSource definition.")
            if if_exists not in vals:
                raise ParameterValueError("if_exists", vals)
            if if_exists == 'fail':
                raise APIError(msg+"Pass if_exists='replace' or 'append' to proceed.")

        # Determine operation to perform: [create, append, replace, register, no op]
        table_fqtn = f"{table_database}.{table_schema}.{table_name}"
        _operation = self._source_table_operation(source_type, if_exists, table_fqtn)
        print(f"Proceeding with operation {_operation}")
        # we'll want this function for future when we support more complex table operations
        # for now, its sole purpose is to check table existence, raise directive errors

        # Upload to Snowflake
        # Path: csv & dataframe
        if source_type.lower() in ["csv", "dataframe"]:
            if source_type.lower() == "csv":
                df = pd.read_csv(file_path, prefix="COL")
            print("Uploading to table:", table_name)
            dataframe._snowflakify_dataframe(df)
            self.data_warehouse.write_dataframe_to_table(df, table_name=table_name, append=True if if_exists=="append" else False)
            self.data_warehouse.grant_table_ownership(table=table_name, role=self.data_warehouse.publisher_role)
            self.data_warehouse.grant_table_access(table=table_name, role=self.data_warehouse.reader_role)

        # Path: table            
        if source_type.lower() == "table":
            print(f"Granting read access on table {table_name} to {self.data_warehouse.reader_role.upper()}")
            # NOTE: grant_table_acess is intentional here
            # In other methods, we create a table with the rasgo user role and want to hand if off to the reader role
            # In this case, the table is likely part of a pre-existing rbac model and we just want to grant rasgo access
            self.data_warehouse.grant_table_access(table=table_name, role=self.data_warehouse.reader_role, database=table_database, schema=table_schema)

        # Publish DataSource
        data_source = self.save.data_source(name=data_source_name or table_name,
                                                      table=table_name,
                                                      domain=data_source_domain,
                                                      source_type=source_type,
                                                      parent_source_id=parent_data_source_id,
                                                      if_exists='edit')
        if data_source:
            self.create.data_source_stats(data_source.id)
            return data_source
        else:
            raise APIError("DataSource failed to upload")

    def _source_table_operation(self, 
                                source_type: str, 
                                if_exists: str, 
                                to_fqtn: str, 
                                from_fqtn: Optional[str] = None):
        """
        Called by publish_source_data: 
            Given a source_type and tables, return the operation that should be performed to publish this table
        """
        to_database = to_fqtn.split(".")[0]
        to_schema = to_fqtn.split(".")[1]
        to_table = to_fqtn.split(".")[-1]
        data_source_exists = True if self.match.data_source(table=to_table) is not None else False

        try: 
            dest_table = self.data_warehouse.get_source_table(table_name=to_table, database=to_database, schema=to_schema, record_limit=10)
            is_dest_table_empty = dest_table.empty
        except:
            is_dest_table_empty = True

        if source_type in ["csv", "dataframe"]:
            if not data_source_exists:
                if is_dest_table_empty:
                    return "create"
                else: #not is_dest_table_empty
                    raise APIError(f"A table named {to_fqtn} already exists, but is not registered as a Rasgo DataSource. " 
                                   f"Try running this function with params: source_type='table', table='{to_table}'. "
                                    "If this wasn't an intentional match, run this function again to generate a new table name.")
            elif data_source_exists:
                if is_dest_table_empty:
                    return "create"
                else: #not is_dest_table_empty
                    return if_exists
            else:
                raise APIError("Could not determine what operation to perform.")
        elif source_type == "table":
            if not data_source_exists:
                return "register"
            elif not is_dest_table_empty and if_exists in ["append", "replace"]:
                print(f"pyRasgo does not support {if_exists} operations on tables yet.")
            return "no op"
        else:
            raise APIError("Could not determine what operation to perform.")