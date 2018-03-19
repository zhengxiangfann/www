import logging
import sys
from flask import Flask, request, redirect
from werkzeug.routing import BaseConverter

app = Flask(__name__, static_url_path="/templates/vue")
class RegexConverter(BaseConverter):
    def __init__(self, map, *args):
        self.map = map
        self.regex = args[0]

app.url_map.converters["regexp"] = RegexConverter

@app.route('/a/b/c/<regexp(".*"):category>/<regexp(".*"):entity>/<regexp(".*"):method>', methods=['GET','POST'])
def index(category, entity, method,controller_dir="controller"):
    class_name= "%sController"%(entity.capitalize())
    module_name = "%s.%s.%s"%(controller_dir, category, class_name)
    command ="from %s import %s"%(module_name, class_name)
    print(command)
    exec(command)
    m = sys.modules[module_name]
    print(m)
    execute_class = getattr(m, class_name)
    print(execute_class)
    exc_method = getattr(execute_class(), method)
    print(exc_method)
    return exc_method()

if __name__ == '__main__':
    app.run(threaded=True, debug=False)
