import requests.exceptions
import rumps
from rumps import SliderMenuItem

from light_interface import FakeRingLight, RingLight

from config import IP_ADDRESS, PORT, DEBUG

class ElgatoRingLight(rumps.App):
    def __init__(self, **kwargs) -> None:
        super().__init__("Light Controller", icon="icons/taskbar_icon.png", *kwargs)
        try:
            self.light = RingLight(IP_ADDRESS, PORT)
        except requests.exceptions.ConnectTimeout:
            rumps.alert(f"Cannot Connect", f"Unable to connect to Elgato Ring Light @ {IP_ADDRESS}:{PORT}")
            if DEBUG:
                self.light = FakeRingLight()
            else:
                rumps.quit_application()

        self.light_info_1 = rumps.MenuItem(None, callback=self.onoff_controller)
        self.light_info_2 = rumps.MenuItem(None)

        self.brightness_label = rumps.MenuItem("Brightness")
        self.brightness = rumps.SliderMenuItem(value=self.light.brightness, callback=self.brightness_control, dimensions=(230, 25))

        self.warmth_label = rumps.MenuItem("Warmth")
        self.warmth_label = rumps.MenuItem("🟠--------🟡--------⚪--------️🔵")
        self.warmth = rumps.SliderMenuItem(value=self.light.temperature, min_value=2900, max_value=7000, callback=self.warmth_control, dimensions=(230, 25))

        self.hw_details = rumps.MenuItem("Details")
        self.hw_details.add(f"Name: {self.light.display_name}")
        self.hw_details.add(f"Product: {self.light.product_name}")
        self.hw_details.add(f"IP Address: {self.light.ip_address}:{self.light.port}")
        self.hw_details.add(f"Serial #: {self.light.serial_number}")
        self.hw_details.add(f"Hardware Rev #: {self.light.hardware_board_type}")
        self.hw_details.add(f"Firmware Version: {self.light.firmware_version}")
        self.hw_details.add(f"Firmware Build: {self.light.firmware_build_number}")

        self.menu = [self.light_info_1, None, self.brightness_label, self.brightness, self.warmth_label, self.warmth, self.light_info_2, None, self.hw_details]

        self.get_light_info()

    def onoff_controller(self, _) -> None:
        if self.light.is_on:
            self.light.off()
        else:
            self.light.on()
        self.get_light_info()

    def brightness_control(self, sender: SliderMenuItem):
        self.light.set_brightness(sender.value)
        self.get_light_info()

    def warmth_control(self, sender: SliderMenuItem):
        self.light.set_color(sender.value)
        self.get_light_info()

    def get_light_info(self) -> None:
        self.light.info()
        self.light_info_1.title = f"{self.light.product_name} - {'On' if self.light.is_on else 'Off'}"
        self.light_info_2.title = f"Brightness: {self.light.brightness} Warmth: {self.light.temperature}K"


if __name__ == "__main__":
    ElgatoRingLight().run()
