import requests
import logging
import sys
import argparse

FORMAT = "%(asctime)-15s - %(levelname)s - %(module)20s:%(lineno)-5d - %(message)s"
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=FORMAT)
LOG = logging.getLogger(__name__)


# Verifies whether a color string is valid for Lifx bulbs
def __validate_color(token, color):
    header = {
        "Authorization": "Bearer %s" % token,
    }
    request = {
        "string": color
    }
    LOG.info("Validating color --- {}".format(request))
    response = requests.get('https://api.lifx.com/v1/color', data=request, headers=header)
    LOG.debug("Validate color response: {}".format(response))
    if response.status_code == 200:
        return True
    return False


# Sets color for all lights associated with access token
# Optionally, specify a group to set color for only those lights
def set_color(token, color, brightness, group=None):
    if not __validate_color(token, color):
        raise ValueError("Invalid color value. Refer to Lifx API documentation for valid colors.")
    header = {
        "Authorization": "Bearer %s" % token,
    }
    request = {
        "color": color,
        "brightness": brightness
    }
    if group is None:
        LOG.info("Setting color for all lights --- {}".format(request))
        response = requests.put('https://api.lifx.com/v1/lights/all/state', data=request, headers=header)
        LOG.info("Set color response: {}".format(response))
    else:
        LOG.info("Setting color for group:{} --- {}".format(group, request))
        response = requests.put('https://api.lifx.com/v1/lights/group:{}/state'.format(group), data=request,
                                headers=header)
        LOG.info("Set color response: {}".format(response))


def parse_args():
    LOG.info("Parsing Args")
    parser = argparse.ArgumentParser(description='Lifx API for Lux')
    parser.add_argument('-t', '--token', type=str, help='Authentication token for Lifx API')
    parser.add_argument('-c', '--color', type=str, help='RGB color to set lights. Example: [#ffffff]')
    parser.add_argument('-b', '--brightness', type=str, default="1.0",
                        help='Brightness value to set lights. Range: [0.0 - 1.0]')
    parser.add_argument('-g', '--group', type=str, nargs="?", help='Group of lights to set color. [Optional]')
    return parser.parse_args()


def main():
    args = parse_args()
    LOG.info("\nRunning Lifx API script with args:\n\tColor: {}\n\tBrightness: {}\n\tGroup: {}".format(args.color,
                                                                                                     args.brightness,
                                                                                                     args.group))
    set_color(args.token, args.color, args.brightness, args.group)
    LOG.info("Done")


if __name__ == "__main__":
    main()
