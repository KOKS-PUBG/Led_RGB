name: Build APK

on:
  push:
    branches: [ main, master ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Java
      uses: actions/setup-java@v4
      with:
        distribution: 'zulu'
        java-version: '17'

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'

    - name: Install Buildozer dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y \
          git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config \
          zlib1g-dev libffi-dev libssl-dev cmake ccache libstdc++6 \
          libglu1-mesa libpulse0 libncursesw6

    - name: Install Buildozer and Cython
      run: |
        pip install --upgrade pip
        pip install --upgrade buildozer cython==0.29.36

    - name: Build with Buildozer
      run: |
        buildozer -v android debug
      env:
        # Отключаем автозагрузку чужих NDK, используем ту версию, что укажем или скачаем
        BUILDER_NDK_VERSION: "25b"

    - name: Upload APK artifact
      uses: actions/upload-artifact@v4
      with:
        name: android-apk
        path: bin/*.apk
