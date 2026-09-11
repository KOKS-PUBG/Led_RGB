[app]

# Название вашего приложения под иконкой на телефоне
title = RGB LED CONTROL

# Системное имя пакета (только латиница и цифры, без пробелов)
package.name = myledapp

# Домен пакета
package.domain = org.led

# Директория с исходным кодом
source.dir = .

# Расширения файлов проекта
source.include_exts = py,png,jpg,kv,atlas

# Версия приложения
version = 1.0

# Необходимые библиотеки (включая bleak для Bluetooth)
requirements = python3,kivy,bleak,android,pyjnius

# Ориентация экрана (portrait - портретная, landscape - ландшафтная)
orientation = portrait

# Поддерживаемые архитектуры процессоров
android.archs = arm64-v8a

# Разрешения для работы с Bluetooth
android.permissions = BLUETOOTH, BLUETOOTH_ADMIN, BLUETOOTH_SCAN, BLUETOOTH_CONNECT, ACCESS_FINE_LOCATION

# Версии Android SDK, NDK и API
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.accept_sdk_license = True

[buildozer]

# Уровень вывода логов (2 для подробной отладки)
log_level = 2

# Режим предупреждений
warn_on_root = 1
