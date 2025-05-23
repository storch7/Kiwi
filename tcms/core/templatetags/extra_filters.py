"""
Custom template tag filters.
"""

from importlib import import_module

import bleach
import markdown
import pkg_resources
from bleach_allowlist import markdown_attrs, markdown_tags, print_attrs, print_tags
from django import template
from django.contrib.messages import constants as messages
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="is_list")
def is_list(variable):
    return isinstance(variable, list)


def bleach_input(input_html):
    return bleach.clean(
        input_html,
        markdown_tags + print_tags + ["del", "s"],
        {**markdown_attrs, **print_attrs},
    )


@register.filter(name="markdown2html")
def markdown2html(md_str):
    """
    Returns markdown string as HTML.
    """
    if md_str is None:
        md_str = ""

    extensions = [
        "markdown.extensions.codehilite",
        "markdown.extensions.fenced_code",
        "markdown.extensions.nl2br",
        "markdown.extensions.sane_lists",
        "markdown.extensions.tables",
        "tcms.utils.markdown",
    ]
    for plugin in pkg_resources.iter_entry_points("kiwitcms.plugins"):
        try:
            module_name = f"{plugin.module_name}.markdown"
            import_module(module_name)
            extensions.append(module_name)
        except ModuleNotFoundError:
            # maybe the add-on doesn't ship markdown extensions
            pass

    rendered_md = markdown.markdown(
        md_str,
        extensions=extensions,
    )

    html = bleach_input(rendered_md)
    return mark_safe(html)  # nosec:B703:B308:blacklist


@register.filter(name="message_icon")
def message_icon(msg):
    """
    Returns the string class name of a message icon
    which feeds directly into Patternfly.
    """
    icons = {
        messages.ERROR: "error-circle-o",
        messages.WARNING: "warning-triangle-o",
        messages.SUCCESS: "ok",
        messages.INFO: "info",
    }
    return "pficon-" + icons[msg.level]
