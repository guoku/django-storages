from django.conf import settings
from django.core.files.storage import Storage
from django.core.exceptions import ImproperlyConfigured
from django.utils.text import force_unicode

try:
    import qiniu.conf
    import qiniu.io
    import qiniu.rs
    import qiniu.rsf
except ImportError:
    raise ImproperlyConfigured, "Could not load qiniu sdk dependency.\
    \nSee https://github.com/qiniu"



class QiNiuStorage(Storage):

    def __init__(self, base_url=settings.MEDIA_URL):
        if hasattr(settings, 'QINIU_MEDIA_URL'):
            self.base_url = settings.MOGILEFS_MEDIA_URL
        else:
            self.base_url = base_url

        if hasattr(settings, 'QINIU_ACCESS_KEY'):
            qiniu.conf.ACCESS_KEY = settings.QINIU_ACCESS_KEY
        else:
            raise

        if hasattr(settings, "QINIU_SECRET_KEY"):
            qiniu.conf.SECRET_KEY = settings.QINIU_SECRET_KEY
        else:
            raise

        if hasattr(settings, "QINIU_BUCKET"):
            self.bucket = settings.QINIU_BUCKET
            self.policy = qiniu.rs.PutPolicy(self.bucket)
        else:
            raise

        self.uptoken = self.policy.token()
        self.extra = qiniu.io.PutExtra()
        self.extra.mime_type = "image/jpeg"
        self.client = qiniu.rsf.Client()


    def _open(self, filename, mode='rb'):
        pass
        # f = self.client.read_file(filename)
        # # f.closed = False
        # # print f
        # return File(file=f, name=filename)

    def exists(self, filename):
        items, err =  self.client.list_prefix(self.bucket, prefix=filename, limit=1)
        return bool(items['items'])

    def save(self, filename, raw_contents):
        filename = self.get_available_name(filename)
        ret, err = qiniu.io.put(self.uptoken, filename, raw_contents, self.extra)
        if err is not None:
            print "Error: %s" % err
            print "FAILURE writing file %s" % (filename)
        else:
            return force_unicode(filename.replace('\\', '/'))

    def delete(self, filename):
        ret, err =self.client.delete(self.bucket, filename)
        if err is not None:
            print "Error: Delete Error %s" % err
            return False
        else:
            return True

__author__ = 'edison'
