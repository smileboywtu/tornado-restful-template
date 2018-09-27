# Tornado Web Template

Tornado 是 Python 的一个异步 Web 开发框架，可以提供很高的并发，另外框架本身简单，可以当作一个库来使用，
非常适合用来开发 Restful 风格的 API。

[![asciicast](https://asciinema.org/a/YTtcBNnOItY8IRXjBx7E70VIc.png)](https://asciinema.org/a/YTtcBNnOItY8IRXjBx7E70VIc)


任务监控：

![text](./3rds/screens/flower01.png)
![text](./3rds/screens/flower02.png)
![text](./3rds/screens/flower02.png)


# 特性

- [x] Python 3.5+ Async / Await 支持
- [x] uvloop 支持
- [x] json schema 参数校验
- [x] middleware error handle
- [x] request_id support
- [x] celery 后台任务
- [x] flower 任务监控
- [x] health check 健康检查
- [x] log 定制
- [x] docker 支持
- [x] redis 支持
- [x] mysql 支持
- [x] unittest 支持
- [x] pylint 代码检查
- [x] 常见 python 漏洞扫描
- [x] benchmark 测试

# Run

```shell
make up
```

# Unittest

```shell
make test
```

# Pylint

使用 `pylint` 来检查代码，pylint 的配置文件在 `3rd/pylint/pylint.rc`。

```shell
make lint
```

# Benchmark

使用 [wrk](https://github.com/wg/wrk) 进行测试：

```shell
./wrk -c 100 -t 5 -d 20s http://localhost:8000/api/v1/counter\?name\=zhangsan
```

# Docker

你需要先配置 `.env/.local/` 下面的文件，配置完成后用 `docker-compose` 来启动应用：

```shell
sudo docker-compose -f local.yaml build
sudo docker-compose -f local.yaml up
```

目前可以直接使用 `make` 来操作 `docker-compose` , 具体参见 `make help`。

# Celery 任务

celery 的配置在 `celery_app.py` 中，celery 的任务可以写在 `celery_tasks.tasks` 中。

# 日志模板

tornado log file content example:

```shell
## access log
127.0.0.1 - - [09/23/18:18:18:34 +0800] "GET /api/v1/counter HTTP/1.1" 200 0 1.50 dd50668528cd417a86f9e2f331a9cbf6 app-up [{}] -
127.0.0.1 - - [09/23/18:18:18:34 +0800] "GET /api/v1/counter HTTP/1.1" 200 0 1.50 69aa272728cb45fdbcfbe8334ff1a117 app-up [{}] -
127.0.0.1 - - [09/23/18:18:18:34 +0800] "GET /api/v1/counter HTTP/1.1" 200 0 1.50 5aa968a778374df2b327e24a27cd9ff4 app-up [{}] -
127.0.0.1 - - [09/23/18:18:18:34 +0800] "GET /api/v1/counter HTTP/1.1" 200 0 0.98 0930f80545ed4d7eb8521742a9f65189 app-up [{}] -
127.0.0.1 - - [09/23/18:18:18:34 +0800] "GET /api/v1/counter HTTP/1.1" 200 0 0.98 4641fd35c6934c7eb0a359ffd7e18ab1 app-up [{}] -


## app log
2018-09-23 17:47:36,984 ERROR 9df1c32f753f41e4aa3d8047523902ba-3908 response.py:63 -- Expecting value: line 1 column 1 (char 0)
Traceback (most recent call last):
  File "E:\workspace\tornado-restfull-cookiecutter\application\response.py", line 83, in __wrapper__
    return await method(*args, **kwargs)
  File "E:\workspace\tornado-restfull-cookiecutter\application\handlers\counter\handler.py", line 35, in get
    print(self.request.body)
  File "C:\python36\lib\json\__init__.py", line 354, in loads
    return _default_decoder.decode(s)
  File "C:\python36\lib\json\decoder.py", line 339, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
  File "C:\python36\lib\json\decoder.py", line 357, in raw_decode
    raise JSONDecodeError("Expecting value", s, err.value) from None
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)


## gen log

```
