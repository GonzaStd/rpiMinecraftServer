The following minimum hardware requirements are recommended (or needed):
* Raspberry Pi model: 2b or newer
* OS: Raspberry Pi OS Lite (recommended) 
* Available RAM: 2gb for the Minecraft server (keep free memory for the system)
* Secondary Storage: M.2 > SSD > HDD (avoid hosting into microSD card. If you are goint to use it anyway, use a good one)
    - Edit /etc/fstab and add this line: `UUID=xxxx /mnt/hdd1 ext4 defaults,noatime 0 2` to see your device UUID use `sudo blkid`
It is also recommended to:
* Use active cooling
* Use ETHERNET instead of WiFi for permanent hosting

