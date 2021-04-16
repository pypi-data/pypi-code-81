'''
# cdk8s-argocd-resources

Has the ability to synth ArgoCD Application, and AppProject manifests. See example.

## Overview

### example

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from constructs import Construct
from cdk8s import App, Chart, ChartProps
import opencdk8s.cdk8s_argocd_resources as argo

class MyChart(Chart):
    def __init__(self, scope, id, *, namespace=None, labels=None):
        super().__init__(scope, id, namespace=namespace, labels=labels)

        argo.ArgoCdApplication(self, "DemoApp",
            metadata={
                "name": "demo",
                "namespace": "argocd"
            },
            spec={
                "project": "default",
                "source": {
                    "repo_uRL": "example-git-repo",
                    "path": "examplepath",
                    "target_revision": "HEAD"
                },
                "destination": {
                    "server": "https://kubernetes.default.svc"
                },
                "sync_policy": {
                    "sync_options": ["ApplyOutOfSyncOnly=true"
                    ]
                }
            }
        )

        argo.ArgoCdProject(self, "DemoProject",
            metadata={
                "name": "demo",
                "namespace": "argocd"
            },
            spec={
                "description": "demo project",
                "source_repos": ["*"
                ],
                "destination": [{
                    "namespace": "default",
                    "server": "https://kubernetes.default.svc"
                }]
            }
        )

app = App()
MyChart(app, "asd")
app.synth()
```

<details>
<summary>demo.k8s.yaml</summary>

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: demo
  namespace: argocd
spec:
  destination:
    server: https://kubernetes.default.svc
  project: default
  source:
    path: examplepath
    repoURL: example-git-repo
    targetRevision: HEAD
  syncPolicy:
    syncOptions:
      - ApplyOutOfSyncOnly=true
---
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: demo
  namespace: argocd
spec:
  description: demo project
  destination:
    - namespace: default
      server: https://kubernetes.default.svc
  sourceRepos:
    - "*"
```

</details>

## Installation

### TypeScript

Use `yarn` or `npm` to install.

```sh
$ npm install @opencdk8s/cdk8s-argocd-resources
```

```sh
$ yarn add @opencdk8s/cdk8s-argocd-resources
```

### Python

```sh
$ pip install cdk8s-argocd-resources
```

## Contribution

1. Fork ([link](https://github.com/opencdk8s/cdk8s-argocd-resources/fork))
2. Bootstrap the repo:

   ```bash
   npx projen   # generates package.json
   yarn install # installs dependencies
   ```
3. Development scripts:
   |Command|Description
   |-|-
   |`yarn compile`|Compiles typescript => javascript
   |`yarn watch`|Watch & compile
   |`yarn test`|Run unit test & linter through jest
   |`yarn test -u`|Update jest snapshots
   |`yarn run package`|Creates a `dist` with packages for all languages.
   |`yarn build`|Compile + test + package
   |`yarn bump`|Bump version (with changelog) based on [conventional commits]
   |`yarn release`|Bump + push to `master`
4. Create a feature branch
5. Commit your changes
6. Rebase your local changes against the master branch
7. Create a new Pull Request (use [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) for the title please)

## Licence

[Apache License, Version 2.0](./LICENSE)

## Author

[Hunter-Thompson](https://github.com/Hunter-Thompson)
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

import cdk8s
import constructs
from .k8s import EnvVar as _EnvVar_490cd9ba, ObjectMeta as _ObjectMeta_29e57f6b


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argocd-resources.ApplicationDestination",
    jsii_struct_bases=[],
    name_mapping={"namespace": "namespace", "server": "server"},
)
class ApplicationDestination:
    def __init__(
        self,
        *,
        namespace: typing.Optional[builtins.str] = None,
        server: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param namespace: 
        :param server: 

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if namespace is not None:
            self._values["namespace"] = namespace
        if server is not None:
            self._values["server"] = server

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("server")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argocd-resources.ApplicationDirectory",
    jsii_struct_bases=[],
    name_mapping={"recurse": "recurse"},
)
class ApplicationDirectory:
    def __init__(self, *, recurse: typing.Optional[builtins.bool] = None) -> None:
        '''
        :param recurse: 

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if recurse is not None:
            self._values["recurse"] = recurse

    @builtins.property
    def recurse(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("recurse")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationDirectory(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argocd-resources.ApplicationPlugin",
    jsii_struct_bases=[],
    name_mapping={"env": "env", "name": "name"},
)
class ApplicationPlugin:
    def __init__(
        self,
        *,
        env: typing.Optional[_EnvVar_490cd9ba] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param env: 
        :param name: 

        :stability: experimental
        '''
        if isinstance(env, dict):
            env = _EnvVar_490cd9ba(**env)
        self._values: typing.Dict[str, typing.Any] = {}
        if env is not None:
            self._values["env"] = env
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def env(self) -> typing.Optional[_EnvVar_490cd9ba]:
        '''
        :stability: experimental
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[_EnvVar_490cd9ba], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationPlugin(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argocd-resources.ApplicationSource",
    jsii_struct_bases=[],
    name_mapping={
        "directory": "directory",
        "path": "path",
        "plugin": "plugin",
        "repo_url": "repoURL",
        "target_revision": "targetRevision",
    },
)
class ApplicationSource:
    def __init__(
        self,
        *,
        directory: typing.Optional[ApplicationDirectory] = None,
        path: typing.Optional[builtins.str] = None,
        plugin: typing.Optional[ApplicationPlugin] = None,
        repo_url: typing.Optional[builtins.str] = None,
        target_revision: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param directory: 
        :param path: 
        :param plugin: 
        :param repo_url: 
        :param target_revision: 

        :stability: experimental
        '''
        if isinstance(directory, dict):
            directory = ApplicationDirectory(**directory)
        if isinstance(plugin, dict):
            plugin = ApplicationPlugin(**plugin)
        self._values: typing.Dict[str, typing.Any] = {}
        if directory is not None:
            self._values["directory"] = directory
        if path is not None:
            self._values["path"] = path
        if plugin is not None:
            self._values["plugin"] = plugin
        if repo_url is not None:
            self._values["repo_url"] = repo_url
        if target_revision is not None:
            self._values["target_revision"] = target_revision

    @builtins.property
    def directory(self) -> typing.Optional[ApplicationDirectory]:
        '''
        :stability: experimental
        '''
        result = self._values.get("directory")
        return typing.cast(typing.Optional[ApplicationDirectory], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def plugin(self) -> typing.Optional[ApplicationPlugin]:
        '''
        :stability: experimental
        '''
        result = self._values.get("plugin")
        return typing.cast(typing.Optional[ApplicationPlugin], result)

    @builtins.property
    def repo_url(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("repo_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_revision(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("target_revision")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argocd-resources.ApplicationSyncPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "automated": "automated",
        "retry": "retry",
        "sync_options": "syncOptions",
    },
)
class ApplicationSyncPolicy:
    def __init__(
        self,
        *,
        automated: typing.Optional["SyncPolicyAutomated"] = None,
        retry: typing.Optional["SyncRetry"] = None,
        sync_options: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param automated: 
        :param retry: 
        :param sync_options: 

        :stability: experimental
        '''
        if isinstance(automated, dict):
            automated = SyncPolicyAutomated(**automated)
        if isinstance(retry, dict):
            retry = SyncRetry(**retry)
        self._values: typing.Dict[str, typing.Any] = {}
        if automated is not None:
            self._values["automated"] = automated
        if retry is not None:
            self._values["retry"] = retry
        if sync_options is not None:
            self._values["sync_options"] = sync_options

    @builtins.property
    def automated(self) -> typing.Optional["SyncPolicyAutomated"]:
        '''
        :stability: experimental
        '''
        result = self._values.get("automated")
        return typing.cast(typing.Optional["SyncPolicyAutomated"], result)

    @builtins.property
    def retry(self) -> typing.Optional["SyncRetry"]:
        '''
        :stability: experimental
        '''
        result = self._values.get("retry")
        return typing.cast(typing.Optional["SyncRetry"], result)

    @builtins.property
    def sync_options(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("sync_options")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationSyncPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArgoCdApplication(
    cdk8s.ApiObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@opencdk8s/cdk8s-argocd-resources.ArgoCdApplication",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        metadata: typing.Optional[_ObjectMeta_29e57f6b] = None,
        spec: typing.Optional["ArgoCdApplicationSpec"] = None,
    ) -> None:
        '''(experimental) Defines an "extentions" API object for AWS Load Balancer Controller - https://github.com/kubernetes-sigs/aws-load-balancer-controller.

        :param scope: the scope in which to define this object.
        :param id: a scope-local name for the object.
        :param metadata: 
        :param spec: 

        :stability: experimental
        '''
        props = ArgoCdApplicationProps(metadata=metadata, spec=spec)

        jsii.create(ArgoCdApplication, self, [scope, id, props])

    @jsii.member(jsii_name="manifest") # type: ignore[misc]
    @builtins.classmethod
    def manifest(
        cls,
        *,
        metadata: typing.Optional[_ObjectMeta_29e57f6b] = None,
        spec: typing.Optional["ArgoCdApplicationSpec"] = None,
    ) -> typing.Any:
        '''(experimental) Renders a Kubernetes manifest for an ingress object. https://github.com/kubernetes-sigs/aws-load-balancer-controller.

        This can be used to inline resource manifests inside other objects (e.g. as templates).

        :param metadata: 
        :param spec: 

        :stability: experimental
        '''
        props = ArgoCdApplicationProps(metadata=metadata, spec=spec)

        return typing.cast(typing.Any, jsii.sinvoke(cls, "manifest", [props]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="GVK")
    def GVK(cls) -> cdk8s.GroupVersionKind:
        '''
        :stability: experimental
        '''
        return typing.cast(cdk8s.GroupVersionKind, jsii.sget(cls, "GVK"))


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argocd-resources.ArgoCdApplicationProps",
    jsii_struct_bases=[],
    name_mapping={"metadata": "metadata", "spec": "spec"},
)
class ArgoCdApplicationProps:
    def __init__(
        self,
        *,
        metadata: typing.Optional[_ObjectMeta_29e57f6b] = None,
        spec: typing.Optional["ArgoCdApplicationSpec"] = None,
    ) -> None:
        '''
        :param metadata: 
        :param spec: 

        :stability: experimental
        '''
        if isinstance(metadata, dict):
            metadata = _ObjectMeta_29e57f6b(**metadata)
        if isinstance(spec, dict):
            spec = ArgoCdApplicationSpec(**spec)
        self._values: typing.Dict[str, typing.Any] = {}
        if metadata is not None:
            self._values["metadata"] = metadata
        if spec is not None:
            self._values["spec"] = spec

    @builtins.property
    def metadata(self) -> typing.Optional[_ObjectMeta_29e57f6b]:
        '''
        :stability: experimental
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[_ObjectMeta_29e57f6b], result)

    @builtins.property
    def spec(self) -> typing.Optional["ArgoCdApplicationSpec"]:
        '''
        :stability: experimental
        '''
        result = self._values.get("spec")
        return typing.cast(typing.Optional["ArgoCdApplicationSpec"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArgoCdApplicationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argocd-resources.ArgoCdApplicationSpec",
    jsii_struct_bases=[],
    name_mapping={
        "destination": "destination",
        "project": "project",
        "source": "source",
        "sync_policy": "syncPolicy",
    },
)
class ArgoCdApplicationSpec:
    def __init__(
        self,
        *,
        destination: typing.Optional[ApplicationDestination] = None,
        project: typing.Optional[builtins.str] = None,
        source: typing.Optional[ApplicationSource] = None,
        sync_policy: typing.Optional[ApplicationSyncPolicy] = None,
    ) -> None:
        '''
        :param destination: 
        :param project: 
        :param source: 
        :param sync_policy: 

        :stability: experimental
        '''
        if isinstance(destination, dict):
            destination = ApplicationDestination(**destination)
        if isinstance(source, dict):
            source = ApplicationSource(**source)
        if isinstance(sync_policy, dict):
            sync_policy = ApplicationSyncPolicy(**sync_policy)
        self._values: typing.Dict[str, typing.Any] = {}
        if destination is not None:
            self._values["destination"] = destination
        if project is not None:
            self._values["project"] = project
        if source is not None:
            self._values["source"] = source
        if sync_policy is not None:
            self._values["sync_policy"] = sync_policy

    @builtins.property
    def destination(self) -> typing.Optional[ApplicationDestination]:
        '''
        :stability: experimental
        '''
        result = self._values.get("destination")
        return typing.cast(typing.Optional[ApplicationDestination], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source(self) -> typing.Optional[ApplicationSource]:
        '''
        :stability: experimental
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[ApplicationSource], result)

    @builtins.property
    def sync_policy(self) -> typing.Optional[ApplicationSyncPolicy]:
        '''
        :stability: experimental
        '''
        result = self._values.get("sync_policy")
        return typing.cast(typing.Optional[ApplicationSyncPolicy], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArgoCdApplicationSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArgoCdProject(
    cdk8s.ApiObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@opencdk8s/cdk8s-argocd-resources.ArgoCdProject",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        metadata: typing.Optional[_ObjectMeta_29e57f6b] = None,
        spec: typing.Optional["ArgoCdProjectSpec"] = None,
    ) -> None:
        '''(experimental) Defines an "extentions" API object for AWS Load Balancer Controller - https://github.com/kubernetes-sigs/aws-load-balancer-controller.

        :param scope: the scope in which to define this object.
        :param id: a scope-local name for the object.
        :param metadata: 
        :param spec: 

        :stability: experimental
        '''
        props = ArgoCdProjectProps(metadata=metadata, spec=spec)

        jsii.create(ArgoCdProject, self, [scope, id, props])

    @jsii.member(jsii_name="manifest") # type: ignore[misc]
    @builtins.classmethod
    def manifest(
        cls,
        *,
        metadata: typing.Optional[_ObjectMeta_29e57f6b] = None,
        spec: typing.Optional["ArgoCdProjectSpec"] = None,
    ) -> typing.Any:
        '''(experimental) Renders a Kubernetes manifest for an ingress object. https://github.com/kubernetes-sigs/aws-load-balancer-controller.

        This can be used to inline resource manifests inside other objects (e.g. as templates).

        :param metadata: 
        :param spec: 

        :stability: experimental
        '''
        props = ArgoCdProjectProps(metadata=metadata, spec=spec)

        return typing.cast(typing.Any, jsii.sinvoke(cls, "manifest", [props]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="GVK")
    def GVK(cls) -> cdk8s.GroupVersionKind:
        '''
        :stability: experimental
        '''
        return typing.cast(cdk8s.GroupVersionKind, jsii.sget(cls, "GVK"))


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argocd-resources.ArgoCdProjectProps",
    jsii_struct_bases=[],
    name_mapping={"metadata": "metadata", "spec": "spec"},
)
class ArgoCdProjectProps:
    def __init__(
        self,
        *,
        metadata: typing.Optional[_ObjectMeta_29e57f6b] = None,
        spec: typing.Optional["ArgoCdProjectSpec"] = None,
    ) -> None:
        '''
        :param metadata: 
        :param spec: 

        :stability: experimental
        '''
        if isinstance(metadata, dict):
            metadata = _ObjectMeta_29e57f6b(**metadata)
        if isinstance(spec, dict):
            spec = ArgoCdProjectSpec(**spec)
        self._values: typing.Dict[str, typing.Any] = {}
        if metadata is not None:
            self._values["metadata"] = metadata
        if spec is not None:
            self._values["spec"] = spec

    @builtins.property
    def metadata(self) -> typing.Optional[_ObjectMeta_29e57f6b]:
        '''
        :stability: experimental
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[_ObjectMeta_29e57f6b], result)

    @builtins.property
    def spec(self) -> typing.Optional["ArgoCdProjectSpec"]:
        '''
        :stability: experimental
        '''
        result = self._values.get("spec")
        return typing.cast(typing.Optional["ArgoCdProjectSpec"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArgoCdProjectProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argocd-resources.ArgoCdProjectSpec",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_resource_white_list": "clusterResourceWhiteList",
        "description": "description",
        "destination": "destination",
        "namespace_resource_blacklist": "namespaceResourceBlacklist",
        "namespace_resource_whitelist": "namespaceResourceWhitelist",
        "roles": "roles",
        "source_repos": "sourceRepos",
    },
)
class ArgoCdProjectSpec:
    def __init__(
        self,
        *,
        cluster_resource_white_list: typing.Optional[typing.Sequence["ResourceRef"]] = None,
        description: typing.Optional[builtins.str] = None,
        destination: typing.Optional[typing.Sequence[ApplicationDestination]] = None,
        namespace_resource_blacklist: typing.Optional[typing.Sequence["ResourceRef"]] = None,
        namespace_resource_whitelist: typing.Optional[typing.Sequence["ResourceRef"]] = None,
        roles: typing.Optional[typing.Sequence["ProjectRoles"]] = None,
        source_repos: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param cluster_resource_white_list: 
        :param description: 
        :param destination: 
        :param namespace_resource_blacklist: 
        :param namespace_resource_whitelist: 
        :param roles: 
        :param source_repos: 

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if cluster_resource_white_list is not None:
            self._values["cluster_resource_white_list"] = cluster_resource_white_list
        if description is not None:
            self._values["description"] = description
        if destination is not None:
            self._values["destination"] = destination
        if namespace_resource_blacklist is not None:
            self._values["namespace_resource_blacklist"] = namespace_resource_blacklist
        if namespace_resource_whitelist is not None:
            self._values["namespace_resource_whitelist"] = namespace_resource_whitelist
        if roles is not None:
            self._values["roles"] = roles
        if source_repos is not None:
            self._values["source_repos"] = source_repos

    @builtins.property
    def cluster_resource_white_list(
        self,
    ) -> typing.Optional[typing.List["ResourceRef"]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("cluster_resource_white_list")
        return typing.cast(typing.Optional[typing.List["ResourceRef"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination(self) -> typing.Optional[typing.List[ApplicationDestination]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("destination")
        return typing.cast(typing.Optional[typing.List[ApplicationDestination]], result)

    @builtins.property
    def namespace_resource_blacklist(
        self,
    ) -> typing.Optional[typing.List["ResourceRef"]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("namespace_resource_blacklist")
        return typing.cast(typing.Optional[typing.List["ResourceRef"]], result)

    @builtins.property
    def namespace_resource_whitelist(
        self,
    ) -> typing.Optional[typing.List["ResourceRef"]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("namespace_resource_whitelist")
        return typing.cast(typing.Optional[typing.List["ResourceRef"]], result)

    @builtins.property
    def roles(self) -> typing.Optional[typing.List["ProjectRoles"]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("roles")
        return typing.cast(typing.Optional[typing.List["ProjectRoles"]], result)

    @builtins.property
    def source_repos(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("source_repos")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArgoCdProjectSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argocd-resources.ProjectRoles",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "groups": "groups",
        "name": "name",
        "policies": "policies",
    },
)
class ProjectRoles:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        policies: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param description: 
        :param groups: 
        :param name: 
        :param policies: 

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if groups is not None:
            self._values["groups"] = groups
        if name is not None:
            self._values["name"] = name
        if policies is not None:
            self._values["policies"] = policies

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("policies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectRoles(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argocd-resources.ResourceRef",
    jsii_struct_bases=[],
    name_mapping={"group": "group", "kind": "kind"},
)
class ResourceRef:
    def __init__(
        self,
        *,
        group: typing.Optional[builtins.str] = None,
        kind: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param group: 
        :param kind: 

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if group is not None:
            self._values["group"] = group
        if kind is not None:
            self._values["kind"] = kind

    @builtins.property
    def group(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kind(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("kind")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResourceRef(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argocd-resources.RetryBackoff",
    jsii_struct_bases=[],
    name_mapping={
        "duration": "duration",
        "factor": "factor",
        "max_duration": "maxDuration",
    },
)
class RetryBackoff:
    def __init__(
        self,
        *,
        duration: typing.Optional[builtins.str] = None,
        factor: typing.Optional[jsii.Number] = None,
        max_duration: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param duration: 
        :param factor: 
        :param max_duration: 

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if duration is not None:
            self._values["duration"] = duration
        if factor is not None:
            self._values["factor"] = factor
        if max_duration is not None:
            self._values["max_duration"] = max_duration

    @builtins.property
    def duration(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def factor(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_duration(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("max_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RetryBackoff(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argocd-resources.SyncPolicyAutomated",
    jsii_struct_bases=[],
    name_mapping={
        "allow_empty": "allowEmpty",
        "prune": "prune",
        "self_heal": "selfHeal",
    },
)
class SyncPolicyAutomated:
    def __init__(
        self,
        *,
        allow_empty: typing.Optional[builtins.bool] = None,
        prune: typing.Optional[builtins.bool] = None,
        self_heal: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param allow_empty: 
        :param prune: 
        :param self_heal: 

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if allow_empty is not None:
            self._values["allow_empty"] = allow_empty
        if prune is not None:
            self._values["prune"] = prune
        if self_heal is not None:
            self._values["self_heal"] = self_heal

    @builtins.property
    def allow_empty(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("allow_empty")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def prune(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("prune")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def self_heal(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("self_heal")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyncPolicyAutomated(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argocd-resources.SyncRetry",
    jsii_struct_bases=[],
    name_mapping={"backoff": "backoff", "limit": "limit"},
)
class SyncRetry:
    def __init__(
        self,
        *,
        backoff: typing.Optional[RetryBackoff] = None,
        limit: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param backoff: 
        :param limit: 

        :stability: experimental
        '''
        if isinstance(backoff, dict):
            backoff = RetryBackoff(**backoff)
        self._values: typing.Dict[str, typing.Any] = {}
        if backoff is not None:
            self._values["backoff"] = backoff
        if limit is not None:
            self._values["limit"] = limit

    @builtins.property
    def backoff(self) -> typing.Optional[RetryBackoff]:
        '''
        :stability: experimental
        '''
        result = self._values.get("backoff")
        return typing.cast(typing.Optional[RetryBackoff], result)

    @builtins.property
    def limit(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyncRetry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ApplicationDestination",
    "ApplicationDirectory",
    "ApplicationPlugin",
    "ApplicationSource",
    "ApplicationSyncPolicy",
    "ArgoCdApplication",
    "ArgoCdApplicationProps",
    "ArgoCdApplicationSpec",
    "ArgoCdProject",
    "ArgoCdProjectProps",
    "ArgoCdProjectSpec",
    "ProjectRoles",
    "ResourceRef",
    "RetryBackoff",
    "SyncPolicyAutomated",
    "SyncRetry",
]

publication.publish()
