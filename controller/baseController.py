#coding:utf-8

# import sys
import json
import datetime
from json import JSONDecoder, JSONEncoder
from flask import request,Response
# from flask.ext.login import current_user
from flask_login import current_user

class BaseController(object):

    def __init__(self):

        self._params = None
        self._data = None
        self._cookie = None
        self._logger = None
        self._conf = None
        self._url_prefix = "a/b/c"
        self.__init_params()

    def set_logger(self, logger):
        params_str = ''
        if self._params:
            params_str = json.dumps(self._params.to_dict())
        cookie_str = ''
        if self._cookie:
            cookie_str = "%s"%(self._cookie)
        self._logger = logger
        self._logger.info('[URL:%s] [params:%s][cookie:%s][user:%s]'%(request.full_path, params_str, cookie_str, self.__format_current_user_info() ))

    def __format_current_user_info(self):
        if not current_user:
            return
        if current_user.is_anonymous:
            return
        ui = current_user.info
        return "{id:%s,name:%s}"%(ui.id, ui.name)

    def __init_params(self):
        if request.method == 'POST':
            self._params = request.form
        if request.method == 'GET':
            self._params = request.args
        if request.cookies:
            self._cookie = request.cookies
        if request.data:
            self._data = request.data
        print("data", self._data)
        print("json", request.json)
        print("values",request.values)
        print("stream", request.stream.read())
        print("environment", request.environ)

    def set_conf(self, conf):
        self._conf = conf

    def _write_response(self, code, data='', msg=''):
        class DateTimeEncoder(JSONEncoder):
            def default(self, obj):
                if isinstance(obj,datetime.datetime) or isinstance(obj, datetime.date):
                    encoded_object = str(obj)
                else:
                    encoded_object = json.JSONEncoder.default(self, obj)
                return encoded_object
        response_msg_map = {
            'SUCCESS': {'code': 0, 'message': 'success'},
            'UNKNOWN': {'code': -1, 'message': 'unknown'},
            'SERVER_FAILED': {'code': 1, 'message': 'server failed'},
            'NO_DATA': {'code': 2, 'message': 'no data'},
            'NO_USER_LEVEL': {'cdoe': 3, 'message': 'no user level'},
            'WRONG_PARAMS': {'code': 4, 'message': 'wrong params'}
        }
        if code not in response_msg_map:
            response = {'code': 5, 'message': msg}
        else:
            response = response_msg_map[code]
        response['data'] = data
        return Response(json.dumps(response, cls=DateTimeEncoder), mimetype="application/json")

    def _format_response_digits2(self, data, except_fields=[], thousands=True, rounds=2):
        if not data:
            return False
        for item in data:
            for k, v in item.items():
                if self.__is_number(v) and k not in except_fields:
                    if int(float(v)) != float(v):
                        item[k] = round(float(v), rounds)
                    else:
                        item[k] = int(float(v))
                    if thousands:
                        item[k] = format(item[k], ',')
        return True

    def _format_response_digits(self, data, fields, thousands=True, rounds=2):
        if not data or not fields:
            return False
        for item in data:
            for field in fields:
                if field in item:
                    # only float round
                    if not item[field]:
                        item[field] = 0.0
                    if int(float(item[field])) != float(item[field]):
                        item[field] = round(float(item[field]), rounds)
                    else:
                        item[field] = int(float(item[field]))
                    if thousands:
                        item[field] = format(item[field], ',')
        return True

    def _gen_in_url(self, category, entity, method, version, params=None):
        url = "%s/%s/%s/%s/%s" % (self.__url_prefix, version, category, entity, method)
        if params:
            params_str = params
            if type(params) == type({}):
                params_set = map(lambda v: "%s=%s" % (v[0], urllib.quote(("%s" % v[1]).encode('utf-8'))),
                                 params.items())
                params_str = '&'.join("%s" % v for v in params_set)
            url = "%s?%s" % (url, params_str)
        return url


    def _get_param(self, key, default=''):
        val = self._params.get(key)
        if not val:
            val = default
        if type(default) == type(''):
            val = str(val)
        elif type(default) == type(1):
            val = int(val)
        elif type(default) == type(3.1):
            val = float(val)
        return val

