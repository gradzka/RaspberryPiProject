from camera import Camera
from flask import Flask, jsonify, request, make_response, Response
from flask_cors import CORS, cross_origin
from netifaces import interfaces, ifaddresses, AF_INET
import os
import sys
import wiringpi


app = Flask(__name__, static_url_path="")
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
pathname = os.path.dirname(sys.argv[0])


@app.errorhandler(400)
def bad_request(error):
    if error == "":
        return make_response(jsonify({'Error': 'Bad request'}), 400)
    else:
        return make_response(jsonify({'Error': error}), 400)


@app.route('/get_gyroscope_xyz', methods=['GET'])
@cross_origin()
def get_gyroscope_xyz():
    fd = wiringpi.wiringPiI2CSetup(0x6B)
    wiringpi.wiringPiI2CWriteReg8(fd, 0x20, 15)
    x = twos_complement_combine(wiringpi.wiringPiI2CReadReg8(fd, 0x29), wiringpi.wiringPiI2CReadReg8(fd, 0x29)) / 32768  # left, right
    y = twos_complement_combine(wiringpi.wiringPiI2CReadReg8(fd, 0x2B), wiringpi.wiringPiI2CReadReg8(fd, 0x2A)) / 32768  # up, down
    z = twos_complement_combine(wiringpi.wiringPiI2CReadReg8(fd, 0x2D), wiringpi.wiringPiI2CReadReg8(fd, 0x2C)) / 32768  # rotation
    return jsonify({"gyroscope": [str(x), str(y), str(z)]})


@app.route('/get_processor_percentage_usage', methods=['GET'])
@cross_origin()
def get_processor_percentage_usage():
    processor_usage = str(round(float(os.popen('''grep 'cpu ' /proc/stat |awk '{print ($2+$4)*100/($2+$4+$5)}' ''').
                                      readline()), 2))
    return jsonify({"ProcessorUsage": str(processor_usage)})


@app.route('/get_ram_percentage_usage', methods=['GET'])
@cross_origin()
def get_ram_percentage_usage():
    ram_usage = str(round(float(os.popen('''free | grep Mem | awk '{print $4/$2 * 100.0}' ''').readline()), 2))
    return jsonify({"RAMUsage": str(ram_usage)})


def get_stream(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/get_temperature', methods=['GET'])
@cross_origin()
def get_temperature():
    get_processor_percentage_usage()
    with open("/sys/class/thermal/thermal_zone0/temp") as file:
        temperature = round(float(file.readline()[:-1])/1000, 2)
        return jsonify({"Temperature": str(temperature)})


def ip4_addresses():
    ip_list = []
    for interface in interfaces():
        if ifaddresses(interface).get(AF_INET) is not None:
            for link in ifaddresses(interface).get(AF_INET):
                if link.get('addr') is not None:
                    ip_list.append(link.get('addr'))
    return ip_list


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'Error': 'Not found'}), 404)


@app.route('/toggle_diode/<state>', methods=['GET'])
@cross_origin()
def toggle_diode(state):
    wiringpi.wiringPiSetupGpio()  # For GPIO pin numbering
    if state == '0' or state == '1':
        wiringpi.pinMode(26, int(state))
        wiringpi.digitalWrite(26, int(state))
        return make_response(jsonify({'Success': 'OK'}), 200)
    else:
        return bad_request("Bad diode state")


def twos_complement_combine(msb: int, lsb: int) -> int:
    twos_comp = 256 * msb + lsb
    if twos_comp >= 32768:
        return twos_comp - 65536
    else:
        return twos_comp


# from https://blog.miguelgrinberg.com/post/video-streaming-with-flask
@app.route('/get_video', methods=['GET'])
@cross_origin()
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(get_stream(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1247, threaded=True, debug=True)
