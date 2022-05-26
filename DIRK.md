# Installing RTL-SDR software on Ubuntu

* Install dump1090
```
git clone https://github.com/antirez/dump1090.git
cd dump1090
sudo apt-get install rtl-sdr librtlsdr-dev pkgconf
#
# Change permissions for RTL-SDR usb device
#
sed -i 's/0660/0666/' /lib/udev/rules.d/60-librtlsdr0.rules
sudo udevadm control --reload
make
# Test
./dump1090
#
```

Access to the RTL-SDR device itself is controlled by the udev rules
file. The `sed` command changes the permissions from RWX for `root` to
being avilable for all users. The `udevadm` command is supposed to
reload the udev rules after the `sed` command has changed the file. If
you get a permission denied, just reboot your system or figure out how
to restart udev manually.
