django-storages
===============
1. clone from https://github.com/e-loue/django-storages.git

2. guoku django-storages use pymogile,

3. need install pymogile

## 支持七牛云存储
* 需要安装七牛提供的  [python-sdk](https://github.com/qiniu/python-sdk)

* 使用七牛存储需要在 settings.py 增加以下配置

```
QINIU_ACCESS_KEY = "<YOUR_APP_ACCESS_KEY>"
QINIU_SECRET_KEY = "<YOUR_APP_SECRET_KEY>"
QINIU_BUCKET = "<bucketName>"
```


## 支持阿里云 oss





