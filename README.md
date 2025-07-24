on remote
sudp apt update
sudo apt install vim vlc 

не обязательно
sudo apt install mpg123 mpv


## Setting audio

https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/raspberry-pi-usage

### Create asound.conf file

```bash
sudo vim /etc/asound.conf
```

add

```conf
pcm.speakerbonnet {
   type hw card 0
}

pcm.dmixer {
   type dmix
   ipc_key 1024
   ipc_perm 0666
   slave {
     pcm "speakerbonnet"
     period_time 0
     period_size 1024
     buffer_size 8192
     rate 44100
     channels 2
   }
}

ctl.dmixer {
    type hw card 0
}

pcm.softvol {
    type softvol
    slave.pcm "dmixer"
    control.name "PCM"
    control.card 0
}

ctl.softvol {
    type hw card 0
}

pcm.!default {
    type             plug
    slave.pcm       "softvol"
}
```

### Add Device Tree Overlay

```bash
sudo vim /boot/firmware/config.txt
```

- disable `dtparam=audio=on`
- add `dtoverlay=max98357a`

Reboot

Test audio

```bash
mpg123 file.mp3
```

Volume control - `alsamixer`



sudo apt install -y libgpiod-dev

# autostart

```bash
sudo vim /etc/systemd/system/wekker_main.service
```

```ini
[Unit]
Description=Wekker main service
After=network.target

[Service]
Type=simple
User=wekker
WorkingDirectory=/home/wekker/deploy
ExecStart=/home/wekker/deploy/venv/bin/python /home/wekker/deploy/main.py
Restart=on-failure
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable wekker_main.service
sudo systemctl start wekker_main.service
```

check status

```bash
systemctl status wekker_main.service
```

Stop

```bash
sudo systemctl stop wekker_main.service
```

view logs

```bash
journalctl -u wekker_main.service -f
```


- ✅Сохранять текущую радиостанцию, переключать только поворотом tune
- После будильника песни включать радио
- Переписать radio на отдельный поток и связать через очередь комманд
- Причесать readme
- Добавить отправку homeassistant события при срабатывании
- добавить логгер
- Добавить style, lint
- ✅Поддержка разных типов радиостанций
- mpg123 плейер для mp3 потоков радио
