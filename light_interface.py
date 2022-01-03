import logging

import requests


class RingLight:
    def __init__(self, address: str, port: int):
        self.ip_address = address
        self.port = port

        # On init, go talk to the light and get the full product info
        res = requests.get(f"http://{address}:{port}/elgato/accessory-info", timeout=1)
        details = res.json()
        self.product_name: str = details["productName"]
        self.hardware_board_type: str = details["hardwareBoardType"]
        self.firmware_build_number: str = details["firmwareBuildNumber"]
        self.firmware_version: str = details["firmwareVersion"]
        self.serial_number: str = details["serialNumber"]
        self.display_name: str = details["displayName"]

        self.is_on = 0
        self.brightness = 0
        self.temperature = 0
        self.info()

    def __repr__(self) -> str:
        return f"Elgato Light {self.serial_number} @ {self.ip_address}:{self.port}"

    def on(self) -> None:
        """ Turns the light on """
        logging.debug(f"turning on {self.display_name}")
        data = {"numberOfLights": 1, "lights": [{"on": 1}]}
        res = requests.put(f"http://{self.ip_address}:{self.port}/elgato/lights", json=data)
        self.is_on = res.json()["lights"][0]["on"]

    def off(self) -> None:
        """ Turns the light off """
        logging.debug(f"turning off {self.display_name}")
        data = {"numberOfLights": 1, "lights": [{"on": 0}]}
        res = requests.put(f"http://{self.ip_address}:{self.port}/elgato/lights", json=data)
        self.is_on = res.json()["lights"][0]["on"]

    def set_brightness(self, level: int) -> None:
        """ Sets the light to a specific brightness (0-100) level """
        level = int(level)
        logging.debug(f"setting brightness {level} on {self.display_name}")
        if 0 <= level <= 100:
            data = {"numberOfLights": 1, "lights": [{"brightness": level}]}

            res = requests.put(f"http://{self.ip_address}:{self.port}/elgato/lights", json=data)
            self.brightness = res.json()["lights"][0]["brightness"]
        else:
            logging.warning("INVALID BRIGHTNESS LEVEL - Must be 0-100")

    def inc_brightness(self, amount: int) -> None:
        """ Increases the light brightness by a set amount """
        self.info()
        self.set_brightness(self.brightness + amount)

    def dec_brightness(self, amount: int) -> None:
        """ Decreases the light brightness by a set amount """
        self.info()
        self.set_brightness(self.brightness - amount)

    def set_color(self, temp: int) -> None:
        """ Sets the light to a specific color temperature (2900-7000k) """
        temp = int(temp)
        logging.debug(f"setting color {temp}K on {self.display_name}")
        if 2900 <= temp <= 7000:
            data = {"numberOfLights": 1, "lights": [{"temperature": self._color_fit(temp)}]}

            res = requests.put(f"http://{self.ip_address}:{self.port}/elgato/lights", json=data)
            self.temperature = self._post_fit(res.json()["lights"][0]["temperature"])
        else:
            logging.warning("INVALID COLOR TEMP - Must be 2900-7000")

    def inc_color(self, amount: int) -> None:
        """ Increases the lights color temperature by a set amount """
        self.info()
        self.set_color(self.temperature + amount)

    def dec_color(self, amount: int) -> None:
        """ Decreases the lights color temperature by a set amount """
        self.info()
        self.set_color(self.temperature - amount)

    def info(self) -> dict:
        """ Gets the current light status. """
        logging.debug(f"getting info for {self.display_name}")
        res = requests.get(f"http://{self.ip_address}:{self.port}/elgato/lights")
        status = res.json()["lights"][0]
        self.is_on = status["on"]
        self.brightness = status["brightness"]
        self.temperature = self._post_fit(status["temperature"])
        return {
            "on": self.is_on,
            "brightness": self.brightness,
            "temperature": self.temperature,
        }

    @staticmethod
    def _color_fit(val: int) -> int:
        """Take a color temp (in K) and convert it to the format the Elgato Light wants"""
        return round(987007 * val ** -0.999)

    @staticmethod
    def _post_fit(val: int) -> int:
        """Take the int that the Elgato Light returns and convert it roughly back to color temp (in K)"""
        return int(round(1000000 * val ** -1, -2))


class FakeRingLight:
    def __init__(self) -> None:
        self.ip_address = "-"
        self.port = "0"

        self.product_name: str = "Fake Light"
        self.hardware_board_type: str = "-"
        self.firmware_build_number: str = "-"
        self.firmware_version: str = "-"
        self.serial_number: str = "-"
        self.display_name: str = "-"

        self.is_on = 0
        self.brightness = 50
        self.temperature = 3600

    def __repr__(self) -> str:
        return f"Elgato Light {self.serial_number} @ {self.ip_address}:{self.port}"

    def on(self) -> None:
        self.is_on = True

    def off(self) -> None:
        self.is_on = False

    def set_brightness(self, level: int) -> None:
        level = int(level)
        if 0 <= level <= 100:
            self.brightness = level

    def inc_brightness(self, amount: int) -> None:
        self.set_brightness(self.brightness + amount)

    def dec_brightness(self, amount: int) -> None:
        self.set_brightness(self.brightness - amount)

    def set_color(self, temp: int) -> None:
        temp = int(temp)
        if 2900 <= temp <= 7000:
            self.temperature = temp

    def inc_color(self, amount: int) -> None:
        self.set_color(self.temperature + amount)

    def dec_color(self, amount: int) -> None:
        self.set_color(self.temperature - amount)

    def info(self) -> None:
        pass
