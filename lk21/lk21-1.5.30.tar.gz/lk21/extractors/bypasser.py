from ..thirdparty import exrex
from . import BaseExtractor
from urllib.parse import urlparse
from collections import defaultdict
import re
import inspect
import math


class Bypass(BaseExtractor):
    bypassPattern = defaultdict(lambda: defaultdict(set))
    allBypassPattern = None

    def bypass_ouo(self, url):
        """
        regex: https?://ouo\.(?:press|io)/[^>]+
        """

        def getData(form):
            if not form:
                return None, None
            data = {}
            for input in form.findAll("input", {"name": re.compile(r"token$")}):
                k = input.get("id") or input.get("name")
                data[k] = input["value"]
            return form["action"], data

        raw = self.session.get(url)
        soup = self.soup(raw)
        action, data = getData(soup.form)

        for _ in range(2):
            self.report_bypass(action)
            raw = self.session.post(action, data=data)
            soup = self.soup(raw)
            action, data = getData(soup.form)

        return raw.url

    def bypass_anonfiles(self, url):
        """
        regex: https?://anonfiles\.com/[^>]+
        """

        raw = self.session.get(url)
        soup = self.soup(raw)

        if (dlurl := soup.find(id="download-url")):
            return dlurl["href"]

    def bypass_letsupload(self, url):
        """
        regex: https?://letsupload\.[ic]o/[0-9A-Za-z]+(?:/|\?pt=)[^>]+
        """

        raw = self.session.get(url)
        if (fileId := re.search(r"(?i)showFileInformation\((\d+)\)", raw.text)):
            return self.bypass_redirect('https://letsupload.io/account/direct_download/' + fileId.group(1))
        if (nextUrl := re.search(r"window.location += ['\"]([^\"']+)", raw.text)):
            return nextUrl.group(1)

    def bypass_filesIm(self, url):
        """
        regex: https?://(?:files\.im|racaty\.net|hxfile\.co)/[^>]+
        """

        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Safari/537.36',
        }

        data = {
            'op': 'download2',
            'id': self.getPath(url),
            'rand': '',
            'referer': '',
            'method_free': '',
            'method_premium': '',
        }

        response = self.session.post(url, headers=headers, data=data)
        soup = self.soup(response)

        if (btn := soup.find(class_="btn btn-dow")):
            return btn["href"]
        if (unique := soup.find(id="uniqueExpirylink")):
            return unique["href"]

    def bypass_redirect(self, url):
        """
        regex: https?://bit\.ly/[^>]+
        regex: https?://(?:link\.zonawibu\.cc/redirect\.php\?go|player\.zafkiel\.net/blogger\.php\?yuzu)\=[^>]+
        """
        head = self.session.head(url)
        return head.headers.get("Location", url)

    def bypass_linkpoi(self, url):
        """
        regex: https?://(?:www\.)?uservideo\.xyz/file/[^>]+
        regex: https?://linkpoi\.me/[^>]+
        """

        raw = self.session.get(url)
        soup = self.soup(raw)

        if (a := soup.find("a", class_="btn-primary")):
            return a["href"]

    def bypass_mediafire(self, url):
        """
        regex: https?://(?:www\.)?mediafire\.com/file/[^>]+(?:/file)?
        """

        raw = self.session.get(url)
        soup = self.soup(raw)

        if (dl := soup.find(id="downloadButton")):
            return dl["href"]

    def bypass_zippyshare(self, url):
        """
        regex: https?://www\d+\.zippyshare\.com/v/[^/]+/file\.html
        """

        raw = self.session.get(url)
        soup = self.soup(raw)

        if (script := soup.find("script", text=re.compile("(?si)\s*var a = \d+;"))):
            sc = str(script)
            var = re.findall(r"var [ab] = (\d+)", sc)
            omg = re.findall(r"\.omg (!?=) [\"']([^\"']+)", sc)
            file = re.findall(r'"(/[^"]+)', sc)
            if var and omg:
                a, b = var
                if eval(f"{omg[0][1]!r} {omg[1][0]} {omg[1][1]!r}") or 1:
                    a = math.ceil(int(a) // 3)
                else:
                    a = math.floor(int(a) // 3)
                divider = int(re.findall(f"(\d+)%b", sc)[0])
                return re.search(r"(^https://www\d+.zippyshare.com)", raw.url).group(1) + \
                    "".join([
                        file[0],
                        str(a + (divider % int(b))),
                        file[1]
                    ])

    def bypass_fembed(self, url):
        """
        regex: https?://(?:www\.naniplay|naniplay)(?:\.nanime\.(?:in|biz)|\.com)/file/[^>]+
        regex: https?://layarkacaxxi\.icu/f/[^>]+
        """

        raw = self.session.get(url)
        api = re.search(r"(/api/source/[^\"']+)", raw.text)
        if api is not None:
            result = {}
            raw = self.session.post(
                "https://layarkacaxxi.icu" + api.group(1)).json()
            for d in raw["data"]:
                f = d["file"]
                direct = self.bypass_redirect(f)
                result[f"{d['label']}/{d['type']}"] = direct
            return result

    def report_bypass(self, url):
        if self.logger:
            self.logger.info(f"Bypass link {urlparse(url).netloc}: {url}")

    def bypass_url(self, url):
        """
        Bypass url

        Args:
              url: type 'str'
        """

        patterns = {k: v['pattern'] for k, v in self.bypassPattern.items()}

        previous = url
        stop = False
        while not stop:
            _break = False
            for fname, pattern in patterns.items():
                if isinstance(url, dict) or _break:
                    break

                if any(_re.search(url) for _re in pattern):
                    self.report_bypass(url)

                    func = getattr(self, fname)
                    try:
                        result = func(url)
                    except Exception:
                        result = None

                    if not result:
                        stop = True
                        break

                    if self.run_as_module or not isinstance(result, dict):
                        url = result
                    else:
                        key = self.choice(result.keys())
                        url = result[key]
                    if url == previous:
                        stop = not stop
                    else:
                        previous = url
                    _break = True
            if not _break:
                break

        return re.sub(r" ", "%20", url)


# lazy method
allBypassPattern = []
pattern = re.compile(r"regex *: *(.+)(?:\n|$)")
for key, value in inspect.getmembers(Bypass):
    if key.startswith("bypass_") and key != "bypass_url":
        for urlPattern in pattern.findall(value.__doc__ or ""):
            Bypass.bypassPattern[key]["pattern"].add(
                re.compile(urlPattern)
            )
            allBypassPattern.append(urlPattern)
        if (allPattern := Bypass.bypassPattern.get(key)):
            for rule in allPattern["pattern"]:
                valid_regex = re.sub(
                    r"\[.+?\][+*]\??|\\[a-zA-Z][+*]\??", "\[id\]", rule.pattern)
                valid_regex = re.sub(r"\.[*+]\??", "\[any\]", valid_regex)
                for url in exrex.generate(valid_regex):
                    Bypass.bypassPattern[key]["support"].add(
                        urlparse(url).netloc.removeprefix("www."))

Bypass.allBypassPattern = re.compile(r"|".join(allBypassPattern))
