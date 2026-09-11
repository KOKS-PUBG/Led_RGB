import asyncio
import threading
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from bleak import BleakScanner, BleakClient

LED_CHARACTERISTIC_UUID = "0000fff3-0000-1000-8000-00805f9b34fb"
TARGET_MAC_ADDRESS = "BE:30:8B:00:1B:2F"

CMD_ON = bytearray([0x7e, 0x00, 0x04, 0xf0, 0x00, 0x01, 0xff, 0x00, 0xef])
CMD_OFF = bytearray([0x7e, 0x00, 0x04, 0x00, 0x00, 0x00, 0xff, 0x00, 0xef])

def get_color_command(r, g, b):
    return bytearray([0x7e, 0x07, 0x05, 0x03, r, g, b, 0x10, 0xef])

def get_brightness_command(brightness):
    return bytearray([0x7e, 0x04, 0x01, brightness, 0x00, 0x00, 0xff, 0x00, 0xef])

class LEDControllerApp(App):
    def build(self):
        self.client = None
        self.is_on = False
        self.loop = asyncio.new_event_loop()
        threading.Thread(target=self.start_async_loop, daemon=True).start()

        # Главный экран (верстаем сеткой)
        root = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Статус соединения
        self.lbl_status = Label(text="Статус: Поиск ленты...", size_hint_y=None, height=50, color=(1, 0.7, 0, 1))
        root.add_widget(self.lbl_status)

        # Кнопка питания (Большая)
        self.btn_power = Button(text="⏻ ВЫКЛ", font_size=24, background_color=(0.3, 0.3, 0.3, 1), size_hint_y=None, height=80)
        self.btn_power.bind(on_press=self.toggle_power)
        root.add_widget(self.btn_power)

        # Яркость
        root.add_widget(Label(text="Яркость", size_hint_y=None, height=30))
        self.slider_bright = Slider(min=0, max=100, value=100, size_hint_y=None, height=40)
        self.slider_bright.bind(on_touch_up=self.change_brightness)
        root.add_widget(self.slider_bright)

        # Быстрые цвета (Квадратики)
        root.add_widget(Label(text="Быстрые цвета", size_hint_y=None, height=30))
        colors_layout = GridLayout(cols=5, spacing=10, size_hint_y=None, height=60)
        
        colors = [
            (255, 0, 0),    # Красный
            (0, 255, 0),    # Зеленый
            (0, 0, 255),    # Синий
            (255, 255, 0),  # Желтый
            (255, 255, 255) # Белый
        ]
        
        for r, g, b in colors:
            btn = Button(text="", background_color=(r/255, g/255, b/255, 1))
            btn.bind(on_press=lambda instance, cr=r, cg=g, cb=b: self.send_command(get_color_command(cr, cg, cb)))
            colors_layout.add_widget(btn)
            
        root.add_widget(colors_layout)

        # Кнопка повторного автоподключения
        btn_reconnect = Button(text="🔄 Переподключиться", size_hint_y=None, height=50, background_color=(0.2, 0.5, 0.8, 1))
        btn_reconnect.bind(on_press=lambda x: self.auto_connect())
        root.add_widget(btn_reconnect)

        # Запуск автоподключения через 1 секунду после старта
        Clock.schedule_once(lambda dt: self.auto_connect(), 1)

        return root

    def start_async_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def auto_connect(self):
        self.lbl_status.text = "Статус: Сканирование эфира..."
        self.lbl_status.color = (1, 0.7, 0, 1)

        async def task():
            try:
                devices = await BleakScanner.discover(timeout=4.0)
                target = None
                for d in devices:
                    if d.address.upper() == TARGET_MAC_ADDRESS.upper():
                        target = d
                        break
                
                if target:
                    Clock.schedule_once(lambda dt: setattr(self.lbl_status, 'text', "Статус: Подключение..."))
                    if self.client and self.client.is_connected:
                        await self.client.disconnect()
                    
                    self.client = BleakClient(target.address)
                    await self.client.connect()
                    Clock.schedule_once(lambda dt: self.set_connected_status(True))
                else:
                    Clock.schedule_once(lambda dt: self.set_connected_status(False))
            except Exception as e:
                Clock.schedule_once(lambda dt: self.set_connected_status(False))

        asyncio.run_coroutine_threadsafe(task(), self.loop)

    def set_connected_status(self, success):
        if success:
            self.lbl_status.text = "Статус: Подключено ✅"
            self.lbl_status.color = (0.2, 0.8, 0.2, 1)
        else:
            self.lbl_status.text = "Статус: Лента не найдена ❌"
            self.lbl_status.color = (0.9, 0.2, 0.2, 1)

    def toggle_power(self, instance):
        self.is_on = not self.is_on
        if self.is_on:
            self.btn_power.text = "⏻ ВКЛ"
            self.btn_power.background_color = (0.2, 0.8, 0.2, 1)
            self.send_command(CMD_ON)
        else:
            self.btn_power.text = "⏻ ВЫКЛ"
            self.btn_power.background_color = (0.3, 0.3, 0.3, 1)
            self.send_command(CMD_OFF)

    def change_brightness(self, instance, value):
        val = int(self.slider_bright.value)
        self.send_command(get_brightness_command(int(val * 2.55)))

    def send_command(self, cmd):
        if not self.client or not self.client.is_connected:
            return

        async def task():
            try:
                await self.client.write_gatt_char(LED_CHARACTERISTIC_UUID, cmd)
            except Exception as e:
                print(f"Ошибка отправки: {e}")

        asyncio.run_coroutine_threadsafe(task(), self.loop)

if __name__ == "__main__":
    LEDControllerApp().run()