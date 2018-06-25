* [简介](#introduction)
* [安装](#installation)
* [快速开始](#quickstart)
* [高级用法](#advancedusage)

# Introduction

Flask-Validate致力于为Flask的请求信息提供可靠的、配置声明式的校验，目的是让参数非法的请求“快速失败”，从而避免造成“坏的影响”。同时，我们也提供校验失败后的错误信息，在提高web应用健壮性的同时，还可以优雅地告知客户端它到底“错在哪儿了”。

校验是全面的，囊括`headers`，`args`，`form`以及`json`。
校验是纯粹的，不向web应用注入任何数据，用户应该从原生的Flask API中获取请求数据。

Flask-Validate依赖[WTForms](http://wtforms.readthedocs.io/en/stable/)和[jsonschema](https://python-jsonschema.readthedocs.io/en/latest/)作为核心校验组件，具体使用方式请参见其文档。

# Installation

使用`pip`安装.

```bash
pip install flask-validate
```

# Quickstart

## 一个完整的例子

创建一个app.py文件，内容如下：

```python
from flask import Flask, jsonify, request
from flask_validate import Input, Validator, validate
from wtforms.validators import DataRequired, AnyOf

app = Flask(__name__)
validator = Validator(app, handle_errors=lambda e: (jsonify(e.errors), 400))


class MyInput(Input):
    headers = {
        'token': [AnyOf(
            ['messi', 'cr7'], message='authentication failure')]
    }
    args = {'name': [DataRequired(message='name is required.')]}


@app.route('/who')
@validate(MyInput)
def who():
    return request.args.get('name')


app.run(host='127.0.0.1', port=6579)
```

打开终端，输入命令`python app.py`运行这个web应用，用`curl`测试结果如下：

当请求数据非法时，会根据用户定义的`handle_errors`这个callable对象处理响应，这里我们直接通过JSON返回校验的错误信息。

```bash
$ curl -s http://127.0.0.1:6579/who | json_pp
{
   "headers" : {
      "token" : [
         "authentication failure"
      ]
   },
   "query_string" : {
      "name" : [
         "name is required."
      ]
   }
}
```

只有请求数据完全合法时才会进入相应的`view_func`处理业务逻辑。

```bash
$ curl -s -H "token: messi" http://127.0.0.1:6579/who\?name\=mec
mec
```

## 使用JSON Schema

当我们需要校验JSON格式的请求体时，可以使用JSON Schema。

```python
from flask import Flask, jsonify, request
from flask_validate import Input, Validator, validate
from flask_validate.validators import JsonSchema, ValidationError

schema = {'type': 'object', 'properties': {'name': {'type': 'string'}}}


def deny_users(form, field):
    name = field.data.get('name')
    if isinstance(name, str) and name != 'mec':
        raise ValidationError('user %s is denied.' % name)


class JsonInput(Input):
    json = [JsonSchema(schema), deny_users]


app = Flask(__name__)
validator = Validator(app, handle_errors=lambda e: (jsonify(e.errors), 400))


@app.route('/who', methods=['POST'])
@validate(JsonInput)
def who():
    print request.get_json(force=True)
    return request.get_json(force=True).get('name')


app.run(host='127.0.0.1', port=6579)
```

当JSON数据格式不合法时，会返回具体的信息。

```bash
$ curl -X POST -s -d '{"name":1}' -H 'Content-type: application/json' http://127.0.0.1:6579/who | json_pp
{
   "json" : {
      "_jsonschema" : [
         "1 is not of type 'string'"
      ]
   }
}
```

在上面的例子中，我们还用到了自定义校验`deny_users`，这使得我们可以根据具体业务逻辑定义校验规则。

```bash
$ curl -X POST -s -d '{"name":"mec1"}' -H 'Content-type: application/json' http://127.0.0.1:6579/who | json_pp
{
   "json" : {
      "_jsonschema" : [
         "user mec1 is denied."
      ]
   }
}
```

# AdvancedUsage

在上面的例子中，我们统一在初始化`flask_validate.Validator`时定义了`handle_errors`参数，这样会使所有的路由在遇到校验失败时都使用这个callable对象处理。为了给特定的路由绑定特定的处理行为，我们可以这样做：

```python
class MyInput(Input):
    def handle_errors(self, e):
        return '1024'
```

注意，`Input`里面定义的`handle_errors`会覆盖`flask_validate.Validator`初始化时传入的行为。

当然，也可以不定义错误处理机制，使用`Input`对象暴露的`Input.validate()`和`Input.errors`在`view_func`里面自行处理。
