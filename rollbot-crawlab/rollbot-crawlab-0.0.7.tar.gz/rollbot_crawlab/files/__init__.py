import functools
from collections import defaultdict
from contextlib import suppress

from scrapy.exceptions import IgnoreRequest, NotConfigured
from scrapy.utils.datatypes import SequenceExclude
from scrapy.utils.defer import defer_result, mustbe_deferred
from itemadapter import ItemAdapter
from scrapy import Request
from scrapy.settings import Settings
from scrapy.utils.log import logger, failure_to_exc_info
from scrapy.utils.misc import arg_to_iter
from scrapy.utils.request import referer_str, request_fingerprint
from twisted.internet import defer
from io import BytesIO
from twisted.internet.defer import DeferredList, Deferred
from twisted.python.failure import Failure
from rollbot_crawlab.utils.oss_file_upload import OssFileUpload


class FileException(Exception):
    """General media error exception"""



class MediaPipeline:

    LOG_FAILED_RESULTS = True

    class SpiderInfo:
        def __init__(self, spider):
            self.spider = spider
            self.downloading = set()
            self.downloaded = {}
            self.waiting = defaultdict(list)

    def __init__(self, download_func=None, settings=None):
        self.download_func = download_func

        if isinstance(settings, dict) or settings is None:
            settings = Settings(settings)
        resolve = functools.partial(self._key_for_pipe,
                                    base_class_name="MediaPipeline",
                                    settings=settings)
        self.allow_redirects = settings.getbool(
            resolve('MEDIA_ALLOW_REDIRECTS'), False
        )
        self._handle_statuses(self.allow_redirects)

    def _handle_statuses(self, allow_redirects):
        self.handle_httpstatus_list = None
        if allow_redirects:
            self.handle_httpstatus_list = SequenceExclude(range(300, 400))

    def _key_for_pipe(self, key, base_class_name=None, settings=None):
        """
        >>> MediaPipeline()._key_for_pipe("IMAGES")
        'IMAGES'
        >>> class MyPipe(MediaPipeline):
        ...     pass
        >>> MyPipe()._key_for_pipe("IMAGES", base_class_name="MediaPipeline")
        'MYPIPE_IMAGES'
        """
        class_name = self.__class__.__name__
        formatted_key = "{}_{}".format(class_name.upper(), key)
        if (
            not base_class_name
            or class_name == base_class_name
            or settings and not settings.get(formatted_key)
        ):
            return key
        return formatted_key

    @classmethod
    def from_crawler(cls, crawler):
        try:
            pipe = cls.from_settings(crawler.settings)
        except AttributeError:
            pipe = cls()
        pipe.crawler = crawler
        return pipe

    def open_spider(self, spider):
        self.spiderinfo = self.SpiderInfo(spider)

    def process_item(self, item, spider):
        upload_oss = item.get('upload_oss', False)
        if upload_oss:
            info = self.spiderinfo
            requests = arg_to_iter(self.get_media_requests(item, info))
            dlist = [self._process_request(r, info, item) for r in requests]
            dfd = DeferredList(dlist, consumeErrors=1)
            return dfd.addCallback(self.item_completed, item, info)
        else:
            return item

    def _process_request(self, request, info, item):
        fp = request_fingerprint(request)
        cb = request.callback or (lambda _: _)
        eb = request.errback
        request.callback = None
        request.errback = None

        # Return cached result if request was already seen
        if fp in info.downloaded:
            return defer_result(info.downloaded[fp]).addCallbacks(cb, eb)

        # Otherwise, wait for result
        wad = Deferred().addCallbacks(cb, eb)
        info.waiting[fp].append(wad)

        # Check if request is downloading right now to avoid doing it twice
        if fp in info.downloading:
            return wad

        # Download request checking media_to_download hook output first
        info.downloading.add(fp)
        dfd = mustbe_deferred(self.media_to_download, request, info, item)
        dfd.addCallback(self._check_media_to_download, request, info, item)
        dfd.addBoth(self._cache_result_and_execute_waiters, fp, info)
        dfd.addErrback(lambda f: logger.error(
            f.value, exc_info=failure_to_exc_info(f), extra={'spider': info.spider})
        )
        return dfd.addBoth(lambda _: wad)  # it must return wad at last

    def _modify_media_request(self, request):
        if self.handle_httpstatus_list:
            request.meta['handle_httpstatus_list'] = self.handle_httpstatus_list
        else:
            request.meta['handle_httpstatus_all'] = True

    def _check_media_to_download(self, result, request, info, item):
        if result is not None:
            return result
        if self.download_func:
            # this ugly code was left only to support tests. TODO: remove
            dfd = mustbe_deferred(self.download_func, request, info.spider)
            dfd.addCallbacks(
                callback=self.media_downloaded, callbackArgs=(request, info, item),
                errback=self.media_failed, errbackArgs=(request, info))
        else:
            self._modify_media_request(request)
            dfd = self.crawler.engine.download(request, info.spider)
            dfd.addCallbacks(
                callback=self.media_downloaded, callbackArgs=(request, info, item),
                errback=self.media_failed, errbackArgs=(request, info))
        return dfd

    def _cache_result_and_execute_waiters(self, result, fp, info):
        if isinstance(result, Failure):
            # minimize cached information for failure
            result.cleanFailure()
            result.frames = []
            result.stack = None

            # This code fixes a memory leak by avoiding to keep references to
            # the Request and Response objects on the Media Pipeline cache.
            #
            # What happens when the media_downloaded callback raises an
            # exception, for example a FileException('download-error') when
            # the Response status code is not 200 OK, is that the original
            # StopIteration exception (which in turn contains the failed
            # Response and by extension, the original Request) gets encapsulated
            # within the FileException context.
            #
            # Originally, Scrapy was using twisted.internet.defer.returnValue
            # inside functions decorated with twisted.internet.defer.inlineCallbacks,
            # encapsulating the returned Response in a _DefGen_Return exception
            # instead of a StopIteration.
            #
            # To avoid keeping references to the Response and therefore Request
            # objects on the Media Pipeline cache, we should wipe the context of
            # the encapsulated exception when it is a StopIteration instance
            #
            # This problem does not occur in Python 2.7 since we don't have
            # Exception Chaining (https://www.python.org/dev/peps/pep-3134/).
            context = getattr(result.value, '__context__', None)
            if isinstance(context, StopIteration):
                setattr(result.value, '__context__', None)

        info.downloading.remove(fp)
        info.downloaded[fp] = result  # cache result
        for wad in info.waiting.pop(fp):
            defer_result(result).chainDeferred(wad)

    # Overridable Interface
    def media_to_download(self, request, info, item):
        """Check request before starting download"""
        pass

    def get_media_requests(self, item, info):
        """Returns the media requests to download"""
        pass

    def media_downloaded(self, response, request, info, item):
        """Handler for success downloads"""
        return response

    def media_failed(self, failure, request, info):
        """Handler for failed downloads"""
        return failure

    def item_completed(self, results, item, info):
        """Called per item when all media requests has been processed"""
        if self.LOG_FAILED_RESULTS:
            for ok, value in results:
                if not ok:
                    logger.error(
                        '%(class)s found errors processing %(item)s',
                        {'class': self.__class__.__name__, 'item': item},
                        exc_info=failure_to_exc_info(value),
                        extra={'spider': info.spider}
                    )
        return item


class AliOssStore(object):
    OSS_ACCESS_KEY_ID = None
    OSS_SECRET_ACCESS_KEY = None
    OSS_ENDPOINT_URL = None
    OSS_BUCKET_NAME = None
    file_upload = None
    def __init__(self):
        """
        auto define the store object
        for more detail please refer
        https://github.com/scrapy/scrapy/blob/0ede017d2ac057b1c3f9fb77a875e4d083e65401/scrapy/pipelines/files.py
        :param host_base:
        :param access_key_id:
        :param access_key_secret:
        :param bucket_name:
        """
        self.file_upload = OssFileUpload(self.OSS_ACCESS_KEY_ID, self.OSS_SECRET_ACCESS_KEY, self.OSS_ENDPOINT_URL, self.OSS_BUCKET_NAME)

    def stat_file(self, path, info):
        # always return the empty result ,force the media request to download the file
        return self.file_upload.exist(path)

    def persist_file(self, path, buf, info, meta=None, headers=None):
        """Upload file to Ali oss storage"""
        self._upload_file(path, buf)

    def _upload_file(self, path, buf):
        self.file_upload.upload_object(path, buf)


class FilesPipeline(MediaPipeline):
    STORE_SCHEME = AliOssStore
    oss_url = None

    def __init__(self, oss_url, download_func=None, settings=None):
        if not oss_url:
            raise NotConfigured
        if isinstance(settings, dict) or settings is None:
            settings = Settings(settings)
        if oss_url[len(oss_url) - 1] != '/':
            oss_url += "/"
        self.oss_url = oss_url
        self.store = self._get_store()
        super(FilesPipeline, self).__init__(download_func=download_func, settings=settings)

    def _get_store(self):
        store_cls = self.STORE_SCHEME
        return store_cls()

    @classmethod
    def from_settings(cls, settings):
        ossStore = cls.STORE_SCHEME
        ossStore.OSS_ACCESS_KEY_ID = settings['OSS_ACCESS_KEY_ID']
        ossStore.OSS_SECRET_ACCESS_KEY = settings['OSS_SECRET_ACCESS_KEY']
        ossStore.OSS_ENDPOINT_URL = settings['OSS_ENDPOINT_URL']
        ossStore.OSS_BUCKET_NAME = settings['OSS_BUCKET_NAME']
        store_uri = settings['OSS_BUCKET_URL']

        return cls(oss_url=store_uri, settings=settings)

    def media_failed(self, failure, request, info):
        if not isinstance(failure.value, IgnoreRequest):
            referer = referer_str(request)
            logger.warning(
                'File (unknown-error): Error downloading %(medianame)s from '
                '%(request)s referred in <%(referer)s>: %(exception)s',
                {'request': request, 'referer': referer, 'exception': failure.value},
                extra={'spider': info.spider}
            )
        raise FileException

    def media_to_download(self, request, info, item):
        def _onsuccess(result):
            if not result:
                return  # returning None force download
            url = self.oss_url + path
            return {'url': request.url, 'oss_url': url, 'path': path}
        path = self.file_path(request, info=info, item=item)
        dfd = defer.maybeDeferred(self.store.stat_file, path, info)
        dfd.addCallbacks(_onsuccess, lambda _: None)
        dfd.addErrback(
            lambda f:
            logger.error(self.__class__.__name__ + '.store.stat_file',
                         exc_info=failure_to_exc_info(f),
                         extra={'spider': info.spider})
        )
        return dfd

    def media_downloaded(self, response, request, info, item):
        referer = referer_str(request)
        if response.status != 200:
            logger.warning(
                'File (code: %(status)s): Error downloading file from '
                '%(request)s referred in <%(referer)s>',
                {'status': response.status,
                 'request': request, 'referer': referer},
                extra={'spider': info.spider}
            )
            raise FileException('download-error')

        if not response.body:
            logger.warning(
                'File (empty-content): Empty file from %(request)s referred '
                'in <%(referer)s>: no-content',
                {'request': request, 'referer': referer},
                extra={'spider': info.spider}
            )
            raise FileException('empty-content')

        status = 'cached' if 'cached' in response.flags else 'downloaded'
        logger.debug(
            'File (%(status)s): Downloaded file from %(request)s referred in '
            '<%(referer)s>',
            {'status': status, 'request': request, 'referer': referer},
            extra={'spider': info.spider}
        )

        try:
            path = self.file_path(request, response=response, info=info, item=item)
            self.file_downloaded(response, request, info, path=path)
        except FileException as exc:
            logger.warning(
                'File (error): Error processing file from %(request)s '
                'referred in <%(referer)s>: %(errormsg)s',
                {'request': request, 'referer': referer, 'errormsg': str(exc)},
                extra={'spider': info.spider}, exc_info=True
            )
            raise
        except Exception as exc:
            logger.error(
                'File (unknown-error): Error processing file from %(request)s '
                'referred in <%(referer)s>',
                {'request': request, 'referer': referer},
                exc_info=True, extra={'spider': info.spider}
            )
            raise FileException(str(exc))
        url = self.oss_url + path
        return {'url': request.url, 'oss_url': url, 'path': path}

    def file_downloaded(self, response, request, info, path):
        buf = BytesIO(response.body)
        buf.seek(0)
        self.store.persist_file(path, buf, info)

    def file_path(self, request, response=None, info=None, item=None):
        pass


class ImageFilesPipeline(FilesPipeline):
    files_urls_field = "images"
    files_result_field = "oss_images"

    def get_media_requests(self, item, info):
        urls = ItemAdapter(item).get(self.files_urls_field, [])
        meta = {'has_base': True}
        return [Request(u, meta=meta) for u in urls]

    def item_completed(self, results, item, info):
        with suppress(KeyError):
            res_list = [x for ok, x in results if ok]
            if len(res_list) > 0:
                article_html = ItemAdapter(item).get("article_html")
                if article_html and '' != article_html:
                    for res_item in res_list:
                        request_url = res_item.get('url')
                        oss_url = res_item.get('oss_url')
                        article_html = article_html.replace(request_url, oss_url)
                    ItemAdapter(item)["article_html"] = article_html
                ItemAdapter(item)[self.files_result_field] = res_list
        return item

    def file_path(self, request, response=None, info=None, item=None):
        return self.store.file_upload.get_file_path(
            url=request.url, item=item, default_ext=".jpg", folder="image"
        )


class AuthorAvatarFilesPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        author = ItemAdapter(item).get('author', {})
        author_avatar = author.get('avatar', None)
        urls = []
        if author_avatar:
            urls.append(author_avatar)
        meta = {'has_base': True}
        return [Request(u, meta=meta) for u in urls]

    def item_completed(self, results, item, info):
        with suppress(KeyError):
            if 'author' in item:
                res_list = [x for ok, x in results if ok]
                if len(res_list) > 0:
                    article_html = ItemAdapter(item).get("article_html")
                    if article_html and '' != article_html:
                        for res_item in res_list:
                            request_url = res_item.get('url')
                            oss_url = res_item.get('oss_url')
                            article_html = article_html.replace(request_url, oss_url)
                        ItemAdapter(item)["article_html"] = article_html
                    if res_list and len(res_list) > 0:
                        ItemAdapter(item)['author']['avatar'] = res_list[0].get("oss_url")
        return item

    def file_path(self, request, response=None, info=None, item=None):
        return self.store.file_upload.get_file_path(
            url=request.url, item=item, default_ext=".jpg", folder="avatar"
        )


class VideoFilesPipeline(FilesPipeline):
    STORE_SCHEME = AliOssStore
    files_urls_field = "movies"
    files_result_field = "oss_movies"

    def get_media_requests(self, item, info):
        urls = ItemAdapter(item).get(self.files_urls_field, [])
        meta = {'has_base': True}
        return [Request(u, meta=meta) for u in urls]

    def item_completed(self, results, item, info):
        with suppress(KeyError):
            res_list = [x for ok, x in results if ok]
            if len(res_list) > 0:
                article_html = ItemAdapter(item).get("article_html")
                if article_html and '' != article_html:
                    for res_item in res_list:
                        request_url = res_item.get('url')
                        oss_url = res_item.get('oss_url')
                        article_html = article_html.replace(request_url, oss_url)
                    ItemAdapter(item)["article_html"] = article_html
                ItemAdapter(item)[self.files_result_field] = res_list
        return item

    def file_path(self, request, response=None, info=None, item=None):
        return self.store.file_upload.get_file_path(
            url=request.url, item=item, default_ext=".mp4", folder="video"
        )
