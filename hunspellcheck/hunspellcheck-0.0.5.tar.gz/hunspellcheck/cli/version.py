"""Version CLI option utilities for hunspellcheck."""

from jinja2 import Template

from hunspellcheck.hunspell.version import get_hunspell_version


DEFAULT_VERSION_TEMPLATE = (
    "{% if version_number %}{{version_prog}} {{version_number}}{% endif %}"
    "{% if version_number and (hunspell_version or ispell_version) %} - {% endif %}"
    "{% if hunspell_version %}Hunspell {{hunspell_version}}{% endif %}"
    "{% if hunspell_version and ispell_version %} - {% endif %}"
    "{% if ispell_version %}Ispell {{ispell_version}}{% endif %}"
)


def render_version_template(
    version_template,
    version_template_context,
    version_prog=None,
    version_number=None,
    hunspell_version=True,
    ispell_version=True,
):
    versions = (
        {}
        if not hunspell_version and not ispell_version
        else get_hunspell_version(hunspell=hunspell_version, ispell=ispell_version)
    )

    _version_template_context = {
        "hunspell_version": None if not hunspell_version else versions["hunspell"],
        "ispell_version": None if not ispell_version else versions["ispell"],
    }
    if version_number is not None:
        _version_template_context["version_prog"] = version_prog
        _version_template_context["version_number"] = version_number
    _version_template_context.update(version_template_context)

    return Template(version_template).render(**_version_template_context)
