# Tornado Web Template

Tornado 是 Python 的一个异步 Web 开发框架，可以提供很高的并发，另外框架本身简单，可以当作一个库来使用，
非常适合用来开发 Restful 风格的 API。

# Feature

- [x] Python 3.5+ Async / Await 支持
- [x] uvloop 支持
- [x] json schema 参数校验
- [x] middleware error handle
- [x] request_id support
- [x] celery 后台任务
- [x] health check 健康检查
- [x] log 定制
- [x] docker 支持
- [x] redis 支持
- [x] mysql 支持
- [x] unittest 支持
- [x] pylint 代码检查
- [x] 常见 python 漏洞扫描
- [x] benchmark 测试

# headers

add customer header at `base_handler.py`。

```shell
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: POST, GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Access-Control-Allow-Origin: 
Cache-Control: no-cache, no-store, must-revalidate
Content-Length: 112
Content-Type: text/javascript;charset=UTF-8
Date: Sun, 23 Sep 2018 09:59:56 GMT
Etag: "4ba583c5d680eecc835af558d0f0225c73e2f60e"
Expires: 0
Pragma: no-cache
Server: TornadoServer/5.1.1
X-Request-Id: ed297d6f511f4951a3dbe9ecb368d3bf
```

# Requirements

参见 `requirements.txt`。

```shell
virtualenv project
source project/bin/activate

pip install -r requirements.txt
```

# Run

```shell
source project/bin/activate
python run.py
```

# Unittest

```shell
source project/bin/activate
python run_test.py
```

# Benchmark

```shell
source project/bin/activate
python run_benchmark.py
```

# Docker
