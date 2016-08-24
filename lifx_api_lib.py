import requests
import logging
import sys

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
        LOG.debug("Set color response: {}".format(response))
    else:
        LOG.info("Setting color for group:{} --- {}".format(group, request))
        response = requests.put('https://api.lifx.com/v1/lights/group:{}/state'.format(group), data=request,
                                headers=header)
        LOG.debug("Set color response: {}".format(response))
