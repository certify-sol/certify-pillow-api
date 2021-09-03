import base64
from io import BytesIO
from flask import Flask, Response, request

from make_certi import make_certi


def text_plain(s): return Response(s, mimetype='text/plain')


app = Flask(__name__)


@app.route('/')
def home():
    json_body = request.get_json(silent=True)
    print(json_body)

    # {"firstName":"ok","secondName":"ok","location":"ok","date":"ok","officiant":"ok","registrant":"ok"}
    certi_lines = [
        "This certifies that",
        "{} & {}".format(json_body["firstName"], json_body["secondName"]),
        "were united in marriage",
        "at {}".format(json_body["location"]),
        "on {}".format(json_body["date"]),
        "by {}".format(json_body["officiant"])
    ]

    certiB64img = make_certi(certi_lines, qr_link=json_body['sig'])
    # print(certiB64img)

    return text_plain(certiB64img)


app.run(host='0.0.0.0')
