import inspect
from collections import deque

from pygments.formatters import HtmlFormatter
from pygments.formatters.html import _escape_html_table
from pygments.token import Token


class CodeHtmlFormatter(HtmlFormatter):
    def __init__(self, instance_class, *args, **kwargs):
        self.instance_class = instance_class
        super(CodeHtmlFormatter, self).__init__(*args, **kwargs)

    def _format_lines(self, tokensource):
        """
        Just format the tokens, without any wrapping tags.
        Yield individual lines.

        most of this code is extracted from HtmlFormatter. Sadly there was no easy
        way to reuse with the changes we needed without copy pasting.
        """
        nocls = self.noclasses
        lsep = self.lineseparator
        # for <span style=""> lookup only
        getcls = self.ttype2class.get
        c2s = self.class2style
        escape_table = _escape_html_table
        lookback = deque()
        instance_class = self.instance_class

        lspan = ''
        line = ''
        for ttype, value in tokensource:
            lookback.append((ttype, value))
            if nocls:
                cclass = getcls(ttype)
                while cclass is None:
                    ttype = ttype.parent
                    cclass = getcls(ttype)
                cspan = cclass and '<span style="%s">' % c2s[cclass][0] or ''
            else:
                cls = self._get_css_class(ttype)
                cspan = cls and '<span class="%s">' % cls or ''

            parts = value.translate(escape_table).split('\n')

            # check if we are dealing with a method
            if ttype in Token.Name and lookback[-2][1] == '.' and lookback[-3][1] == 'self':
                try:
                    is_method = inspect.ismethod(getattr(instance_class, value))
                except AttributeError:
                    # This means it's an attribute that is not in the instance_class
                    pass
                else:
                    if is_method:
                        parts[0] = "<a href=\"#%s\">%s" % \
                            (value, parts[0])
                        parts[-1] = parts[-1] + "</a>"

            # for all but the last line
            for part in parts[:-1]:
                if line:
                    if lspan != cspan:
                        line += (lspan and '</span>') + cspan + part + \
                                (cspan and '</span>') + lsep
                    else: # both are the same
                        line += part + (lspan and '</span>') + lsep
                    yield 1, line
                    line = ''
                elif part:
                    yield 1, cspan + part + (cspan and '</span>') + lsep
                else:
                    yield 1, lsep
            # for the last line
            if line and parts[-1]:
                if lspan != cspan:
                    line += (lspan and '</span>') + cspan + parts[-1]
                    lspan = cspan
                else:
                    line += parts[-1]
            elif parts[-1]:
                line = cspan + parts[-1]
                lspan = cspan
            # else we neither have to open a new span nor set lspan

        if line:
            yield 1, line + (lspan and '</span>') + lsep
