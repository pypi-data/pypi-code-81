'''
# Terraform CDK external Provider ~> 2.1

This repo builds and publishes the Terraform external Provider bindings for [cdktf](https://cdk.tf).

Current build targets are:

* npm
* Pypi
* Nuget
* Maven

## Docs

Find auto-generated docs for this provider here: [./API.md](./API.md)

## Versioning

This project is explicitly not tracking the Terraform external Provider version 1:1. In fact, it always tracks `latest` of `~> 2.1` with every release. If there scenarios where you explicitly have to pin your provider version, you can do so by generating the [provider constructs manually](https://cdk.tf/imports).

These are the upstream dependencies:

* [Terraform CDK](https://cdk.tf)
* [Terraform external Provider](https://github.com/terraform-providers/terraform-provider-external)
* [Terraform Engine](https://terraform.io)

If there are breaking changes (backward incompatible) in any of the above, the major version of this project will be bumped. While the Terraform Engine and the Terraform external Provider are relatively stable, the Terraform CDK is in an early stage. Therefore, it's likely that there will be breaking changes.

## Features / Issues / Bugs

Please report bugs and issues to the [terraform cdk](https://cdk.tf) project:

* [Create bug report](https://cdk.tf/bug)
* [Create feature request](https://cdk.tf/feature)

## Contributing

## projen

This is mostly based on [projen](https://github.com/eladb/projen), which takes care of generating the entire repository.

## cdktf-provider-project based on projen

There's a custom [project builder](https://github.com/terraform-cdk-providers/cdktf-provider-project) which encapsulate the common settings for all `cdktf` providers.

## provider version

The provider version can be adjusted in [./.projenrc.js](./.projenrc.js).
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import cdktf
import constructs


class DataExternal(
    cdktf.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-external.DataExternal",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        program: typing.List[builtins.str],
        query: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        working_dir: typing.Optional[builtins.str] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param program: A list of strings, whose first element is the program to run and whose subsequent elements are optional command line arguments to the program. Terraform does not execute the program through a shell, so it is not necessary to escape shell metacharacters nor add quotes around arguments containing spaces.
        :param query: A map of string values to pass to the external program as the query arguments. If not supplied, the program will receive an empty object as its input.
        :param working_dir: Working directory of the program. If not supplied, the program will run in the current directory.
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        '''
        config = DataExternalConfig(
            program=program,
            query=query,
            working_dir=working_dir,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(DataExternal, self, [scope, id, config])

    @jsii.member(jsii_name="resetQuery")
    def reset_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuery", []))

    @jsii.member(jsii_name="resetWorkingDir")
    def reset_working_dir(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkingDir", []))

    @jsii.member(jsii_name="result")
    def result(self, key: builtins.str) -> builtins.str:
        '''
        :param key: -
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "result", [key]))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="programInput")
    def program_input(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "programInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="queryInput")
    def query_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "queryInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="workingDirInput")
    def working_dir_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workingDirInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="program")
    def program(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "program"))

    @program.setter
    def program(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "program", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="query")
    def query(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "query"))

    @query.setter
    def query(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        jsii.set(self, "query", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="workingDir")
    def working_dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workingDir"))

    @working_dir.setter
    def working_dir(self, value: builtins.str) -> None:
        jsii.set(self, "workingDir", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-external.DataExternalConfig",
    jsii_struct_bases=[cdktf.TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "program": "program",
        "query": "query",
        "working_dir": "workingDir",
    },
)
class DataExternalConfig(cdktf.TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List[cdktf.ITerraformDependable]] = None,
        lifecycle: typing.Optional[cdktf.TerraformResourceLifecycle] = None,
        provider: typing.Optional[cdktf.TerraformProvider] = None,
        program: typing.List[builtins.str],
        query: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        working_dir: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param program: A list of strings, whose first element is the program to run and whose subsequent elements are optional command line arguments to the program. Terraform does not execute the program through a shell, so it is not necessary to escape shell metacharacters nor add quotes around arguments containing spaces.
        :param query: A map of string values to pass to the external program as the query arguments. If not supplied, the program will receive an empty object as its input.
        :param working_dir: Working directory of the program. If not supplied, the program will run in the current directory.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = cdktf.TerraformResourceLifecycle(**lifecycle)
        self._values: typing.Dict[str, typing.Any] = {
            "program": program,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if query is not None:
            self._values["query"] = query
        if working_dir is not None:
            self._values["working_dir"] = working_dir

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[cdktf.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[cdktf.ITerraformDependable]], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[cdktf.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[cdktf.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[cdktf.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[cdktf.TerraformProvider], result)

    @builtins.property
    def program(self) -> typing.List[builtins.str]:
        '''A list of strings, whose first element is the program to run and whose subsequent elements are optional command line arguments to the program.

        Terraform does not execute the program through a shell, so it is not necessary to escape shell metacharacters nor add quotes around arguments containing spaces.
        '''
        result = self._values.get("program")
        assert result is not None, "Required property 'program' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def query(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of string values to pass to the external program as the query arguments.

        If not supplied, the program will receive an empty object as its input.
        '''
        result = self._values.get("query")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def working_dir(self) -> typing.Optional[builtins.str]:
        '''Working directory of the program.

        If not supplied, the program will run in the current directory.
        '''
        result = self._values.get("working_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataExternalConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExternalProvider(
    cdktf.TerraformProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-external.ExternalProvider",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        alias: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param alias: Alias name.
        '''
        config = ExternalProviderConfig(alias=alias)

        jsii.create(ExternalProvider, self, [scope, id, config])

    @jsii.member(jsii_name="resetAlias")
    def reset_alias(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlias", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="aliasInput")
    def alias_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aliasInput"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "alias", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-external.ExternalProviderConfig",
    jsii_struct_bases=[],
    name_mapping={"alias": "alias"},
)
class ExternalProviderConfig:
    def __init__(self, *, alias: typing.Optional[builtins.str] = None) -> None:
        '''
        :param alias: Alias name.
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if alias is not None:
            self._values["alias"] = alias

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''Alias name.'''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DataExternal",
    "DataExternalConfig",
    "ExternalProvider",
    "ExternalProviderConfig",
]

publication.publish()
