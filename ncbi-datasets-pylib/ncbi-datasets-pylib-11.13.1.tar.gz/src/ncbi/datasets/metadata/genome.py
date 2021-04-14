"""Utility functions for working and reporting on assembly data descriptors."""
from typing import List
from ncbi.datasets.openapi.models import V1alpha1AssemblyMatch
from ncbi.datasets.openapi.models import V1alpha1AssemblyDatasetDescriptor


def print_assembly_warning_or_error(assembly_match: V1alpha1AssemblyMatch):
    """Reports assembly warnings and/or errors per query term

    Args:
        assembly_match: A single assembly metadata record returned by the API

    Returns:
        None

    Side Effects:
        Prints report to stdout.
    """
    print(assembly_match.messages)


def assembly_values_by_fields(assembly: V1alpha1AssemblyDatasetDescriptor, fields=List[str]):
    """Filters assembly descriptor for provided `fields`

    Args:
        assembly_descriptor: A single assembly descriptor record returned by the API
        fields: List of top-level fields to allow into returned dict

    Returns:
        dict of supplied fields to their values

    Side Effects:
        Prints report to stdout.
    """
    asm_descriptor_dict = assembly.to_dict()

    if not fields:
        return asm_descriptor_dict

    return {fld: asm_descriptor_dict[fld] for fld in fields if fld in asm_descriptor_dict}


def print_assembly_metadata_by_fields(assembly_match: V1alpha1AssemblyMatch, fields=List[str]):
    """Reports selected fields for a V1alpha1AssemblyMatch object to stdout

    Warning/Error code will be printed if the supplied assembly object does not contain a assembly field.

    Args:
        assembly_match: A single assembly metadata record returned by the API
        fields: A list of top-level field names to display.  If set to None, print the entire object.

    Returns:
        None

    Side Effects:
        Prints report to stdout.
    """
    if not assembly_match.assembly:
        print_assembly_warning_or_error(assembly_match)
        return

    assembly_descriptor = assembly_match.assembly
    assembly_metadata = assembly_values_by_fields(assembly_descriptor, fields=fields)
    print(assembly_metadata)
