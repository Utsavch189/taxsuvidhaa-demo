from rest_framework.renderers import JSONRenderer
import io
from rest_framework.parsers import JSONParser
#takes the serialized data and converts into JSON

def parse(data):
    try:
        json = JSONRenderer().render(data)
        stream = io.BytesIO(json)
        data = JSONParser().parse(stream)
        return data
    except:
        pass