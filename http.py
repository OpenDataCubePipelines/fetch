"""
HTTP-based download of files.
"""

from . import DataSource
import os
import tempfile
import requests
import logging
from contextlib import closing

_log = logging.getLogger(__name__)


def filename_from_url(url):
    """
    Get the filename component of the URL

    >>> filename_from_url('http://example.com/somefile.zip')
    'somefile.zip'
    >>> filename_from_url('http://oceandata.sci.gsfc.nasa.gov/Ancillary/LUTs/modis/utcpole.dat')
    'urcpole.dat'
    """
    return url.split('/')[-1]


def fetch_file(target_dir, name, reporter, url):
    """
    Fetch the given URL to the target folder.

    :type target_dir: str
    :type name: str
    :type reporter: FetchReporter
    :type url: str
    """
    with closing(requests.get(url, stream=True)) as res:
        if res.status_code != 200:
            _log.debug('Received text %r', res.text)
            reporter.file_error(url, "Status code %r" % res.status_code)
            return

        t = tempfile.mktemp(
            dir=target_dir
        )

        with open(t, 'wb') as f:
            for chunk in res.iter_content(4096):
                if chunk:
                    f.write(chunk)
                    f.flush()
    size_bytes = os.path.getsize(t)
    if size_bytes == 0:
        _log.debug('Empty file returned for url %r', url)
        reporter.file_error(url, "Empty return")
        return

    # Move to destination
    target_path = os.path.join(target_dir, name)
    os.rename(t, target_path)
    # Report as complete.
    reporter.file_complete(url, name, target_path)


class HttpSource(DataSource):
    def __init__(self, source_urls, target_dir):
        """
        Get static HTTP urls.

        This is useful for unchanging URLs that need to be
        repeatedly updated.

        :type source_urls: list of str
        :type target_dir: str
        :return:
        """
        super(HttpSource, self).__init__()

        self.source_urls = source_urls
        self.target_dir = target_dir

    def trigger(self, reporter):
        """
        Download all URLs, overriding existing.
        :type reporter: FetchReporter
        :return:
        """
        for url in self.source_urls:
            name = filename_from_url(url)
            fetch_file(self.target_dir, name, reporter, url)


class RssSource(DataSource):
    def __init__(self, rss_url, target_dir):
        """
        Fetch any files from the given RSS URL.

        The title of feed entries is assumed to be the filename.

        :type rss_url: str
        :type target_dir: str
        :return:
        """
        super(RssSource, self).__init__()

        self.rss_url = rss_url
        self.target_dir = target_dir

    def trigger(self, reporter):
        """
        Download RSS feed and fetch missing files.
        """
        super(RssSource, self).trigger(reporter)

        # Fetch feed.
        requests.get(self.rss_url)

        # For each entry,
        #     - does it match pattern?
        #     - do we already have it?

        # Download entry.
        # Move into place.


