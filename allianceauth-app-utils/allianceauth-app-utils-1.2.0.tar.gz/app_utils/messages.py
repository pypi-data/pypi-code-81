from django.contrib.messages.constants import DEBUG, ERROR, SUCCESS, WARNING, INFO
from django.contrib import messages
from django.http import HttpRequest
from django.utils.html import format_html


class messages_plus:
    """Improvement of default Django messages with added level icons and HTML support

    Careful: Use with safe strings only
    """

    _glyph_map = {
        DEBUG: "eye-open",
        INFO: "info-sign",
        SUCCESS: "ok-sign",
        WARNING: "exclamation-sign",
        ERROR: "alert",
    }

    @classmethod
    def _add_messages_icon(cls, level: int, message: str) -> str:
        """Adds an level based icon to standard Django messages"""
        if level not in cls._glyph_map:
            raise ValueError("glyph for level not defined")
        else:
            glyph = cls._glyph_map[level]

        return format_html(
            '<span class="glyphicon glyphicon-{}" '
            'aria-hidden="true"></span>&nbsp;&nbsp;{}',
            glyph,
            message,
        )

    @classmethod
    def debug(
        cls,
        request: HttpRequest,
        message: str,
        extra_tags: str = "",
        fail_silently: bool = False,
    ) -> None:
        """send a debug message"""
        messages.debug(
            request, cls._add_messages_icon(DEBUG, message), extra_tags, fail_silently
        )

    @classmethod
    def info(
        cls,
        request: HttpRequest,
        message: str,
        extra_tags: str = "",
        fail_silently: bool = False,
    ) -> None:
        """send an info message"""
        messages.info(
            request, cls._add_messages_icon(INFO, message), extra_tags, fail_silently
        )

    @classmethod
    def success(
        cls,
        request: HttpRequest,
        message: str,
        extra_tags: str = "",
        fail_silently: bool = False,
    ) -> None:
        """send a success message"""
        messages.success(
            request, cls._add_messages_icon(SUCCESS, message), extra_tags, fail_silently
        )

    @classmethod
    def warning(
        cls,
        request: HttpRequest,
        message: str,
        extra_tags: str = "",
        fail_silently: bool = False,
    ) -> None:
        """send a warning message"""
        messages.warning(
            request, cls._add_messages_icon(WARNING, message), extra_tags, fail_silently
        )

    @classmethod
    def error(
        cls,
        request: HttpRequest,
        message: str,
        extra_tags: str = "",
        fail_silently: bool = False,
    ) -> None:
        """send an error message"""
        messages.error(
            request, cls._add_messages_icon(ERROR, message), extra_tags, fail_silently
        )
