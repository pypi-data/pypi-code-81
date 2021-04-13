"""
Main interface for route53resolver service client paginators.

Usage::

    ```python
    import boto3

    from mypy_boto3_route53resolver import Route53ResolverClient
    from mypy_boto3_route53resolver.paginator import (
        ListFirewallConfigsPaginator,
        ListFirewallDomainListsPaginator,
        ListFirewallDomainsPaginator,
        ListFirewallRuleGroupAssociationsPaginator,
        ListFirewallRuleGroupsPaginator,
        ListFirewallRulesPaginator,
        ListResolverDnssecConfigsPaginator,
        ListResolverEndpointIpAddressesPaginator,
        ListResolverEndpointsPaginator,
        ListResolverQueryLogConfigAssociationsPaginator,
        ListResolverQueryLogConfigsPaginator,
        ListResolverRuleAssociationsPaginator,
        ListResolverRulesPaginator,
        ListTagsForResourcePaginator,
    )

    client: Route53ResolverClient = boto3.client("route53resolver")

    list_firewall_configs_paginator: ListFirewallConfigsPaginator = client.get_paginator("list_firewall_configs")
    list_firewall_domain_lists_paginator: ListFirewallDomainListsPaginator = client.get_paginator("list_firewall_domain_lists")
    list_firewall_domains_paginator: ListFirewallDomainsPaginator = client.get_paginator("list_firewall_domains")
    list_firewall_rule_group_associations_paginator: ListFirewallRuleGroupAssociationsPaginator = client.get_paginator("list_firewall_rule_group_associations")
    list_firewall_rule_groups_paginator: ListFirewallRuleGroupsPaginator = client.get_paginator("list_firewall_rule_groups")
    list_firewall_rules_paginator: ListFirewallRulesPaginator = client.get_paginator("list_firewall_rules")
    list_resolver_dnssec_configs_paginator: ListResolverDnssecConfigsPaginator = client.get_paginator("list_resolver_dnssec_configs")
    list_resolver_endpoint_ip_addresses_paginator: ListResolverEndpointIpAddressesPaginator = client.get_paginator("list_resolver_endpoint_ip_addresses")
    list_resolver_endpoints_paginator: ListResolverEndpointsPaginator = client.get_paginator("list_resolver_endpoints")
    list_resolver_query_log_config_associations_paginator: ListResolverQueryLogConfigAssociationsPaginator = client.get_paginator("list_resolver_query_log_config_associations")
    list_resolver_query_log_configs_paginator: ListResolverQueryLogConfigsPaginator = client.get_paginator("list_resolver_query_log_configs")
    list_resolver_rule_associations_paginator: ListResolverRuleAssociationsPaginator = client.get_paginator("list_resolver_rule_associations")
    list_resolver_rules_paginator: ListResolverRulesPaginator = client.get_paginator("list_resolver_rules")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    ```
"""
import sys
from typing import Iterator, List

from botocore.paginate import Paginator as Boto3Paginator

from mypy_boto3_route53resolver.type_defs import (
    FilterTypeDef,
    ListFirewallConfigsResponseTypeDef,
    ListFirewallDomainListsResponseTypeDef,
    ListFirewallDomainsResponseTypeDef,
    ListFirewallRuleGroupAssociationsResponseTypeDef,
    ListFirewallRuleGroupsResponseTypeDef,
    ListFirewallRulesResponseTypeDef,
    ListResolverDnssecConfigsResponseTypeDef,
    ListResolverEndpointIpAddressesResponseTypeDef,
    ListResolverEndpointsResponseTypeDef,
    ListResolverQueryLogConfigAssociationsResponseTypeDef,
    ListResolverQueryLogConfigsResponseTypeDef,
    ListResolverRuleAssociationsResponseTypeDef,
    ListResolverRulesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    PaginatorConfigTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "ListFirewallConfigsPaginator",
    "ListFirewallDomainListsPaginator",
    "ListFirewallDomainsPaginator",
    "ListFirewallRuleGroupAssociationsPaginator",
    "ListFirewallRuleGroupsPaginator",
    "ListFirewallRulesPaginator",
    "ListResolverDnssecConfigsPaginator",
    "ListResolverEndpointIpAddressesPaginator",
    "ListResolverEndpointsPaginator",
    "ListResolverQueryLogConfigAssociationsPaginator",
    "ListResolverQueryLogConfigsPaginator",
    "ListResolverRuleAssociationsPaginator",
    "ListResolverRulesPaginator",
    "ListTagsForResourcePaginator",
)


class ListFirewallConfigsPaginator(Boto3Paginator):
    """
    [Paginator.ListFirewallConfigs documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/route53resolver.html#Route53Resolver.Paginator.ListFirewallConfigs)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListFirewallConfigsResponseTypeDef]:
        """
        [ListFirewallConfigs.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/route53resolver.html#Route53Resolver.Paginator.ListFirewallConfigs.paginate)
        """


class ListFirewallDomainListsPaginator(Boto3Paginator):
    """
    [Paginator.ListFirewallDomainLists documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/route53resolver.html#Route53Resolver.Paginator.ListFirewallDomainLists)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListFirewallDomainListsResponseTypeDef]:
        """
        [ListFirewallDomainLists.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/route53resolver.html#Route53Resolver.Paginator.ListFirewallDomainLists.paginate)
        """


class ListFirewallDomainsPaginator(Boto3Paginator):
    """
    [Paginator.ListFirewallDomains documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/route53resolver.html#Route53Resolver.Paginator.ListFirewallDomains)
    """

    def paginate(
        self, FirewallDomainListId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListFirewallDomainsResponseTypeDef]:
        """
        [ListFirewallDomains.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/route53resolver.html#Route53Resolver.Paginator.ListFirewallDomains.paginate)
        """


class ListFirewallRuleGroupAssociationsPaginator(Boto3Paginator):
    """
    [Paginator.ListFirewallRuleGroupAssociations documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/route53resolver.html#Route53Resolver.Paginator.ListFirewallRuleGroupAssociations)
    """

    def paginate(
        self,
        FirewallRuleGroupId: str = None,
        VpcId: str = None,
        Priority: int = None,
        Status: Literal["COMPLETE", "DELETING", "UPDATING"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListFirewallRuleGroupAssociationsResponseTypeDef]:
        """
        [ListFirewallRuleGroupAssociations.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/route53resolver.html#Route53Resolver.Paginator.ListFirewallRuleGroupAssociations.paginate)
        """


class ListFirewallRuleGroupsPaginator(Boto3Paginator):
    """
    [Paginator.ListFirewallRuleGroups documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/route53resolver.html#Route53Resolver.Paginator.ListFirewallRuleGroups)
    """

    def paginate(
        self, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListFirewallRuleGroupsResponseTypeDef]:
        """
        [ListFirewallRuleGroups.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/route53resolver.html#Route53Resolver.Paginator.ListFirewallRuleGroups.paginate)
        """


class ListFirewallRulesPaginator(Boto3Paginator):
    """
    [Paginator.ListFirewallRules documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/route53resolver.html#Route53Resolver.Paginator.ListFirewallRules)
    """

    def paginate(
        self,
        FirewallRuleGroupId: str,
        Priority: int = None,
        Action: Literal["ALLOW", "BLOCK", "ALERT"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListFirewallRulesResponseTypeDef]:
        """
        [ListFirewallRules.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/route53resolver.html#Route53Resolver.Paginator.ListFirewallRules.paginate)
        """


class ListResolverDnssecConfigsPaginator(Boto3Paginator):
    """
    [Paginator.ListResolverDnssecConfigs documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/route53resolver.html#Route53Resolver.Paginator.ListResolverDnssecConfigs)
    """

    def paginate(
        self, Filters: List[FilterTypeDef] = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListResolverDnssecConfigsResponseTypeDef]:
        """
        [ListResolverDnssecConfigs.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/route53resolver.html#Route53Resolver.Paginator.ListResolverDnssecConfigs.paginate)
        """


class ListResolverEndpointIpAddressesPaginator(Boto3Paginator):
    """
    [Paginator.ListResolverEndpointIpAddresses documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/route53resolver.html#Route53Resolver.Paginator.ListResolverEndpointIpAddresses)
    """

    def paginate(
        self, ResolverEndpointId: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListResolverEndpointIpAddressesResponseTypeDef]:
        """
        [ListResolverEndpointIpAddresses.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/route53resolver.html#Route53Resolver.Paginator.ListResolverEndpointIpAddresses.paginate)
        """


class ListResolverEndpointsPaginator(Boto3Paginator):
    """
    [Paginator.ListResolverEndpoints documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/route53resolver.html#Route53Resolver.Paginator.ListResolverEndpoints)
    """

    def paginate(
        self, Filters: List[FilterTypeDef] = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListResolverEndpointsResponseTypeDef]:
        """
        [ListResolverEndpoints.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/route53resolver.html#Route53Resolver.Paginator.ListResolverEndpoints.paginate)
        """


class ListResolverQueryLogConfigAssociationsPaginator(Boto3Paginator):
    """
    [Paginator.ListResolverQueryLogConfigAssociations documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/route53resolver.html#Route53Resolver.Paginator.ListResolverQueryLogConfigAssociations)
    """

    def paginate(
        self,
        Filters: List[FilterTypeDef] = None,
        SortBy: str = None,
        SortOrder: Literal["ASCENDING", "DESCENDING"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListResolverQueryLogConfigAssociationsResponseTypeDef]:
        """
        [ListResolverQueryLogConfigAssociations.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/route53resolver.html#Route53Resolver.Paginator.ListResolverQueryLogConfigAssociations.paginate)
        """


class ListResolverQueryLogConfigsPaginator(Boto3Paginator):
    """
    [Paginator.ListResolverQueryLogConfigs documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/route53resolver.html#Route53Resolver.Paginator.ListResolverQueryLogConfigs)
    """

    def paginate(
        self,
        Filters: List[FilterTypeDef] = None,
        SortBy: str = None,
        SortOrder: Literal["ASCENDING", "DESCENDING"] = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListResolverQueryLogConfigsResponseTypeDef]:
        """
        [ListResolverQueryLogConfigs.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/route53resolver.html#Route53Resolver.Paginator.ListResolverQueryLogConfigs.paginate)
        """


class ListResolverRuleAssociationsPaginator(Boto3Paginator):
    """
    [Paginator.ListResolverRuleAssociations documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/route53resolver.html#Route53Resolver.Paginator.ListResolverRuleAssociations)
    """

    def paginate(
        self, Filters: List[FilterTypeDef] = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListResolverRuleAssociationsResponseTypeDef]:
        """
        [ListResolverRuleAssociations.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/route53resolver.html#Route53Resolver.Paginator.ListResolverRuleAssociations.paginate)
        """


class ListResolverRulesPaginator(Boto3Paginator):
    """
    [Paginator.ListResolverRules documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/route53resolver.html#Route53Resolver.Paginator.ListResolverRules)
    """

    def paginate(
        self, Filters: List[FilterTypeDef] = None, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListResolverRulesResponseTypeDef]:
        """
        [ListResolverRules.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/route53resolver.html#Route53Resolver.Paginator.ListResolverRules.paginate)
        """


class ListTagsForResourcePaginator(Boto3Paginator):
    """
    [Paginator.ListTagsForResource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/route53resolver.html#Route53Resolver.Paginator.ListTagsForResource)
    """

    def paginate(
        self, ResourceArn: str, PaginationConfig: PaginatorConfigTypeDef = None
    ) -> Iterator[ListTagsForResourceResponseTypeDef]:
        """
        [ListTagsForResource.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.51/reference/services/route53resolver.html#Route53Resolver.Paginator.ListTagsForResource.paginate)
        """
