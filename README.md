django-storages
===============
1. fork from https://github.com/e-loue/django-storages.git

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
* 需要安装 阿里云 oss sdk 
```
pip install oss2
```

* 再 django settings.py 加入一下配置
```
ALIYUN_ACCESS_KEY           = "<YOUR_ACCESS_KEY>"
ALIYUN_ACCESS_KYE_SECRET    = "<YOUR_ACCESS_SECRET>"
OSS_ENDPOINT                = "ALIYUN_ENDPOINT"
OSS_BUCKET                  = "YOUR_BUCKET_NAME"
```




