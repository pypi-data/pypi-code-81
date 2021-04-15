"""Template for customize the content of the Desktop entry.

Such file should be placed under:

- /usr/share/applications
- ~/.local/share/applications
"""

TEMPLATE = """[Desktop Entry]
Name={name}
Comment=Web Browser
Exec={exec}
Terminal=false
Type=Application
Icon={icon}
Categories=Network;WebBrowser;
MimeType=text/html;text/xml;application/xhtml+xml;application/xml;application/vnd.mozilla.xul+xml;application/rss+xml;application/rdf+xml;image/gif;image/jpeg;image/png;x-scheme-handler/http;x-scheme-handler/https;
StartupNotify=true"""
