import urlparse
from django.conf import settings
from django.core.files.storage import Storage
from django.utils.text import force_unicode
from django.core.exceptions import ImproperlyConfigured
from django.core.files import File
# from django.utils.text import force_unicode


try:
    import oss2
except ImportError:
    raise ImproperlyConfigured, "Could not load aliyun oss2 sdk dependency.\
        \nSee https://help.aliyun.com/document_detail/32026.html"


class OSS2Storage(Storage):

    def __init__(self, base_url=settings.MEDIA_URL):
        # if hasattr(settings, 'OSS_MEDIA_URL'):
        #     self.base_url       = settings.OSS_MEDIA_URL
        # else:
        self.base_url       = base_url

        if hasattr(settings, 'ALIYUN_ACCESS_KEY'):
            self.access_key     = settings.ALIYUN_ACCESS_KEY
        else:
            raise

        if hasattr(settings, 'ALIYUN_ACCESS_KYE_SECRET'):
            self.access_secret  = settings.ALIYUN_ACCESS_KYE_SECRET
        else:
            raise

        if hasattr(settings, 'OSS_ENDPOINT') and hasattr(settings, 'OSS_BUCKET'):
            self.endpoint       = settings.OSS_ENDPOINT
            self.bucket_name    = settings.OSS_BUCKET
        else:
            raise

        auth                    = oss2.Auth(self.access_key, self.access_secret)
        self.bucket             = oss2.Bucket(auth, self.endpoint, self.bucket_name)

    def _open(self, filename, mode='rb'):
        f   = self.bucket.get_object(filename)
        return File(file=f, name=filename)

    def filesize(self, filename):
        raise NotImplemented

    def exists(self, filename):
        f = oss2.ObjectIterator(self.bucket, prefix=filename)
        for row in f:
            if filename == row.key:
                return True
        return False

    def save(self, filename, raw_contents):
        filename = self.get_available_name(filename)
        success = self.bucket.put_object(filename, raw_contents)
        if (success.status == 200):
            return force_unicode(filename.replace('\\', '/'))
        else:
            print "FAILURE writing file %s" % (filename)

    def delete(self, filename):
        success     = self.bucket.delete_object(filename)
        if (success.status == 200):
            return True
        return False

    def url(self, filename):
        return urlparse.urljoin(self.base_url, filename).replace('\\', '/')


