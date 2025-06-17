---
date: 2024-03-21
categories:
  - WAS-110
  - BFW Solutions
  - XGS-PON
description: Install the 8311 community firmware on the WAS-110
pin: true
---

# Install the 8311 community firmware on the WAS-110

![WAS-110 community](install-8311-community-firmware-on-the-bfw-solutions-was-110/was_110_firmware.webp){ class="nolightbox" }
<!-- more -->
<!-- nocont -->

??? tip "Group buy participants..."
    Just a reminder that your [WAS-110] should have come pre-flashed with the 8311 community firmware unless otherwise
    indicated.

    Please ignore the Azores [shell upgrade] and [web UI upgrade](#web-ui-upgrade) sections mentioned below. To update
    your [WAS-110] to a *newer* 8311 community firmware release, refer to the instructions in the
    [supplementary upgrade] section.

Out of the box, the [WAS-110] is not fully compatible with varying ISP OLT configurations, with issues ranging from
vendor-specific managed entities to VEIP to IEEE standards such as [802.1X] and [802.1ad]. Due to these
incompatibilities and discovered bugs, a community firmware[^1] has been curated to fix any impeding issues[^2].

  [802.1X]: https://en.wikipedia.org/wiki/IEEE_802.1X
  [802.1ad]: https://en.wikipedia.org/wiki/IEEE_802.1ad

## Firmware Preparation

### Download firmware

The community firmware comes in two (2) variants: *basic* and *bfw*; for the purposes of this guide, we'll focus on
the recommended <ins>basic</ins> firmware, which can be downloaded at:

<https://github.com/djGrrr/8311-was-110-firmware-builder/releases/latest>

As an example, the following command downloads the *basic* firmware into the current users download directory.

=== ":material-microsoft: Windows"

    ``` sh
    curl.exe -L --output-dir %UserProfile%\Downloads -O https://github.com/djGrrr/8311-was-110-firmware-builder/releases/download/v2.8.0/WAS-110_8311_firmware_mod_v2.8.0_basic.exe
    ```

=== ":simple-apple: macOS / :simple-linux: Linux"

    ``` sh
    curl -L --output-dir ~/Downloads -O https://github.com/djGrrr/8311-was-110-firmware-builder/releases/download/v2.8.0/WAS-110_8311_firmware_mod_v2.8.0_basic.7z
    ```

The *basic* firmware is based on a vanilla MaxLinear [OpenWrt] 19.07 build from [Potrontec]. Additionally, it
includes customized luci web interfaces for hassle-free masquerading and the aforementioned fixes. And unlike the *bfw*
variant, it does not include the abysmal BFW patches and cruft.

  [OpenWrt]: https://openwrt.org/
  [Potrontec]: https://www.potrontec.com/

### Extract download

The community firmware upgrade comes bundled as a self-extracting executable (:material-microsoft: Windows only) or a
[7-Zip] archive and includes:

`local-upgrade.img`

:   Used with the Azores [web upgrade] utility.

`local-upgrade.tar`

:   Used with the universal [shell upgrade] command sequence.

  [web upgrade]: #web-ui-upgrade
  [shell upgrade]: #shell-upgrade
  [7-Zip]: https://www.7-zip.org/

To extract the archive to a temporary directory, execute the following command(s):

!!! info "Replace `<version>` with the downloaded version."

=== ":material-microsoft: Windows"

    #### Self-extracting Executable

    Double-click on the exe file in [Windows File Explorer].

    #### 7-zip

    ``` sh
    7z e "-i!local-upgrade.*" %UserProfile%\Downloads\WAS-110_8311_firmware_mod_<version>_basic.7z -o%Temp%\8311
    ```

      [Windows File Explorer]: https://en.wikipedia.org/wiki/File_Explorer

=== ":simple-apple: macOS"

    !!! bug "macOS Archive Utility mangles the extracted `local-upgrade.tar`"

    !!! note "The following commands assume [Homebrew](https://brew.sh) is installed"

    ``` sh
    brew install sevenzip
    7zz e '-i!local-upgrade.*' ~/Downloads/WAS-110_8311_firmware_mod_<version>_basic.7z -o/tmp
    ```

=== ":simple-linux: Linux"

    !!! note "The following commands assume [Debian] or derivatives[^3]"

    ``` sh
    sudo apt-get install p7zip-full
    7z e '-i!local-upgrade.*' ~/Downloads/WAS-110_8311_firmware_mod_<version>_basic.7z -o/tmp
    ```

## Network setup

Plug the [WAS-110] into a 10-gigabit compatible SFP+ host interface, such as a NIC, media converter, and/or network
switch.

!!! note "Rx loss"
    The [WAS-110] running the default Azores firmware will trigger RX_LOS if the SC/APC fiber cable is unplugged or
    inactive. Some host interfaces will enter a power-saving state, making the [WAS-110] inaccessible.

The default IP address of the [WAS-110] is `192.168.11.1/24`. To connect successfully, choose one (1) of the following
configurations based on your network setup:

* [Static IP](#static-ip)
* [Static Route](#static-route)
* [Source NAT](#source-nat)

=== "Static IP"

    === ":material-microsoft: Windows"

        !!! info "For the shameless mouse clickers..."
            If you are more comfortable with the Windows GUI, follow the <ins>manual</ins> steps outlined by Microsoft at:

            <https://support.microsoft.com/en-us/windows/change-tcp-ip-settings-bd0a07af-15f5-cd6a-363f-ca2b6f391ace>

        !!! tip "Run Command Prompt as Administrator"

            1. Press ++win+r++
            2. In the Run dialog box, type `cmd` into the input field and then press
               ++ctrl+shift+enter++.


        1. Retrieve the host __Interface Name__ the WAS-110 is connected to.

            ``` sh
            netsh interface ip show config
            ```

        2. Assign a `192.168.11.2` static IP address to the host interface, replacing `<interface name>` in the
           following commands with the value retrieved from step 1.

            ``` sh
            netsh interface ipv4 set address name="<interface name>" static 192.168.11.2 255.255.255.0 192.168.11.1
            netsh interface ipv4 set interface "<interface name>" mtu=1500
            ```

            !!! tip "Execute the following command to restore DHCP, *only* if the static IP was temporary for setup."

                ``` sh
                netsh interface ipv4 set address name="<interface name>" dhcp
                ```

    === ":simple-apple: macOS"

        !!! info "For the shameless mouse clickers..."
            If you are more comfortable with the macOS GUI, follow the <ins>manual</ins> steps outlined by Apple at:

            * <https://support.apple.com/en-ca/guide/mac-help/mchlp2718/mac>
            * <https://support.apple.com/en-ca/guide/mac-help/mh14129/mac>

        1. Launch __Terminal App__.

        2. Retrieve the __Network Service__ the WAS-110 is connected to.

            ``` sh
            sudo networksetup -listallnetworkservices
            ```

        3. Assign a `192.168.11.2` static IP address to the host network, replacing `<service>` in the
           following commands with the value retrieved from step 2.

            ``` sh
            sudo networksetup -setmanual <service> 192.168.11.2 255.255.255.0 192.168.11.1
            ```

            !!! tip "Execute the following command to restore DHCP, *only* if the static IP was temporary for setup."

                ``` sh
                sudo networksetup -setdhcp <service>
                ```

    === ":simple-linux: Linux"

        !!! note "The following commands set the IP address but will not persist after a power cycle"
            For persistence check your OS documentation, such as
            [Debian Network Configuration](https://wiki.debian.org/NetworkConfiguration)

        !!! note "The following commands must be run as root `su -` or prepended with `sudo`"

        ``` sh hl_lines="6"
        ip link show
        ethtool <interface>
        ip address show
        ip address flush dev <interface>
        ip route flush dev <interface>
        ip address add 192.168.11.2/24 dev <interface>
        ip address show dev <interface>
        ```

=== "Static Route"

    !!! note "Requires 8311 community firmware v2.7.2+"

    === ":simple-ubiquiti: UniFi Dream Machine"

        <div class="swiper" markdown>

        <div class="swiper-slide" markdown>

        ![Ubiquity WAN](install-8311-community-firmware-on-the-bfw-solutions-was-110/ubiquity_wan_full.webp){ loading=lazy }

        </div>

        <div class="swiper-slide" markdown>

        ![Ubiquity Static Route](install-8311-community-firmware-on-the-bfw-solutions-was-110/ubiquity_routes_full.webp){ loading=lazy }

        </div>

        </div>

        1. Set the SFP+ port as the WAN interface by navigating to **Network > Settings > Internet**.

        2. Create a static route entry by navigating to **Network > Settings > Routing > Static Routes** and applying
           the settings below.

            |                         |                  |
            | ----------------------- | ---------------- |
            | **Name**                | ONT              |
            | **Destination Network** | 192.168.11.0/24  |
            | **Type**                | Interface        |
            | **Value**               | WAN              |

=== "Source NAT"

    === ":simple-opnsense: OPNsense"

        ![OPNsense Virtual IP](install-8311-community-firmware-on-the-bfw-solutions-was-110/opnsense_virtual_ip.webp){ loading=lazy }

        1. Add a virtual IP to the WAN interface by navigating to **Interfaces > Virtual IPs > Settings**, clicking
           :material-plus-thick:, applying the settings below, clicking **Save**, and clicking **Apply**.

            |                                  |                                   |
            | -------------------------------- | --------------------------------- |
            | **Mode**                         | IP Alias                          |
            | **Interface**                    | WAN                               |
            | **Network / Address**            | 192.168.11.2/24                   |
            | **Deny service binding**         | :material-checkbox-blank-outline: |
            | **VHID Group**                   |                                   |
            | **Description**                  | WAS-110 Management                |

        ![OPNsense Firewall Alias](install-8311-community-firmware-on-the-bfw-solutions-was-110/opnsense_firewall_alias.webp){ loading=lazy }

        2. Add a firewall alias by navigating to **Firewall > Aliases**, clicking :material-plus-thick:, applying the
           settings below, clicking **Save**, and clicking **Apply**.

            |                                  |                                    |
            | -------------------------------- | ---------------------------------- |
            | **Enabled**                      | :material-checkbox-marked-outline: |
            | **Name**                         | was_110                            |
            | **Type**                         | Host(s)                            |
            | **Categories**                   |                                    |
            | **Content**                      | 192.168.11.1                       |
            | **Statistics**                   | :material-checkbox-blank-outline:  |
            | **Description**                  | WAS-110                            |

        ![OPNsense Outbound NAT](install-8311-community-firmware-on-the-bfw-solutions-was-110/opnsense_outbound_nat.webp){ loading=lazy }

        3. Switch to Hybrid outbound NAT by navigating to **Firewall > Outbound > NAT**, selecting
           **Hybrid outbound NAT rule generation**, clicking **Save**, and clicking **Apply changes**.

        ![OPNsense Outbound NAT Rule](install-8311-community-firmware-on-the-bfw-solutions-was-110/opnsense_outbound_nat_rule.webp){ loading=lazy }

        4. Add a manual outbound NAT rule, click :material-plus-thick: in the **Manual rules** table, apply the
           settings below, click **Save**, and click **Apply changes**.

            |                                   |                                              |
            | --------------------------------- | -------------------------------------------- |
            | **Interface**                     | WAN                                          |
            | **Source address**                | LAN net                                      |
            | **Destination address**           | was_110                                      |
            | **Translation / target**          | 192.168.11.2 (WAS-110 Management)            |

    === ":simple-pfsense: pfSense"

        === "DHCP WAN"

             ![pfSense Virtual IP](install-8311-community-firmware-on-the-bfw-solutions-was-110/pfsense_firewall_virtual_ip.webp){ loading=lazy }

             1. Add a virtual IP to the WAN interface by navigating to **Firewall > Virtual IPs**, clicking
                :material-plus-thick: **Add**, applying the settings below, clicking **Save**, and clicking **Apply Changes**.

                |                                  |                                   |
                | -------------------------------- | --------------------------------- |
                | **Type**                         | IP Alias                          |
                | **Interface**                    | WAN                               |
                | **Address(es)**                  | 192.168.11.2/24                   |
                | **Description**                  | WAS-110 Management                |

            ![pfSense Firewall Alias](install-8311-community-firmware-on-the-bfw-solutions-was-110/pfsense_firewall_alias.webp){ loading=lazy }

            2. Add a firewall alias by navigating to **Firewall > Aliases > IP**, clicking :material-plus-thick: **Add**,
               applying the settings below, clicking **Save**, and clicking **Apply Changes**.

                | Properties                       | &nbsp;                             |
                | -------------------------------- | ---------------------------------- |
                | **Name**                         | was_110                            |
                | **Description**                  | WAS-110                            |
                | **Type**                         | Host(s)                            |

                | Host(s)                          | &nbsp;                             |
                | -------------------------------- | ---------------------------------- |
                | **IP or FQDN**                   | 192.168.11.1                       |

            ![pfSense Outbound NAT](install-8311-community-firmware-on-the-bfw-solutions-was-110/pfsense_firewall_nat_outbound.webp){ loading=lazy }

            3. Switch to Hybrid outbound NAT by navigating to **Firewall > NAT > Outbound**, selecting
               **Hybrid Outbound NAT rule generation**, clicking **Save**, and clicking **Apply Changes**.

            ![pfSense Outbound NAT Rule](install-8311-community-firmware-on-the-bfw-solutions-was-110/pfsense_firewall_nat_outbound_rule.webp){ loading=lazy }

            4. Add a manual outbound NAT rule, click :material-arrow-up: **Add** in the **Mappings** table, apply the
               settings below, click **Save**, and click **Apply Changes**.

                | Edit Advanced Outbound NAT Entry  | &nbsp;                                       |
                | --------------------------------- | -------------------------------------------- |
                | **Interface**                     | WAN                                          |
                | **Source**                        | LAN subnets                                  |
                | **Destination**                   | Network or Alias - was_110 / 32              |


                | Translation                       | &nbsp;                                       |
                | --------------------------------- | -------------------------------------------- |
                | **Address**                       | 192.168.11.2 (WAS-110 Management)            |

        === "PPPoE WAN"

             Follow the __Accessing a CPE/Modem from Inside the Firewall__ guide from the pfSense documentation:

             <https://docs.netgate.com/pfsense/en/latest/recipes/modem-access.html>

    === ":simple-ubiquiti: UniFi Dream Machine"

        1. Enable SSH by navigating to **OS Settings > Console Settings > Advanced**.

            <https://help.ui.com/hc/en-us/articles/204909374-UniFi-Connect-with-Debug-Tools-SSH>

        2. Connect and execute the following commands from a SSH session:

            !!! tip "Interface numbers are zero (0) indexed, e.g. `eth9` for Port 10"

            ``` sh
            ip addr add dev eth9 local 192.168.11.2/24
            iptables -t nat -A POSTROUTING -o eth9 -d 192.168.11.0/24 -j SNAT --to 192.168.11.2
            ```

            !!! warning "These commands will not persist with the next power cycle or web UI change"
                For boot persistence, please consider installing [on-boot-script-2.x](https://github.com/unifi-utilities/unifios-utilities/tree/main/on-boot-script-2.x).

    === ":simple-mikrotik: MikroTik RouterOS"

        === "WinBox/WebFig"

            1. Assign a static IP on the Ethernet interface within the same subnet as the ONT by navigating to **IP > Addresses**.
            Be sure to set the interface to the correct SFP+ interface of your ONT.

                |                   |                   |
                | ----------------- | ----------------- |
                | **Address**       | 192.168.11.2/24   |
                | **Interface**     | sfp-sfpplus1      |

                ![RouterOS Add IP Address](install-8311-community-firmware-on-the-bfw-solutions-was-110/routeros_ip_address.webp){ loading=lazy }

            2. From Apply a source NAT rule for the Ethernet interface and assigned IP(s) by navigating to **IP > Firewall > NAT**.
            Be sure to set the out interface to the correct SFP+ interface of your ONT.

                |                       |                   |
                | --------------------- | ----------------- |
                | **Chain**             | srcnat            |
                | **Dst. Address**      | 192.168.11.1      |
                | **Out. Interface**    | sfp-sfpplus1      |
                | **Action**            | src-nat           |
                | **To Addresses**      | 192.168.11.2      |

                ![RouterOS srcnat Match](install-8311-community-firmware-on-the-bfw-solutions-was-110/routeros_srcnat_match.webp){ loading=lazy }
                ![RouterOS srcnat Action](install-8311-community-firmware-on-the-bfw-solutions-was-110/routeros_srcnat_action.webp){ loading=lazy }

        === "Terminal"

            !!! tip "Be sure to change `sfp-sfpplus1` for the correct SFP+ interface of your ONT. These terminal commands will persist."

            ``` sh
            /ip/address add address=192.168.11.2/24 interface=sfp-sfpplus1 network=192.168.11.0
            /ip firewall nat add action=src-nat chain=srcnat dst-address=192.168.11.1 out-interface=sfp-sfpplus1 to-addresses=192.168.11.2
            ```

You should now be able to access the [WAS-110] at `192.168.11.1`.

## Test optics

Before any installation, it's highly recommended to do a simple optics [fault test] on the [WAS-110]. If the signal(s)
are abnormal, contact the seller immediately to start the RMA process. If you're uncertain, please double-check on the
[8311 Discord].

[fault test]: troubleshoot-connectivity-issues-with-the-was-110.md#optical-status
[8311 Discord]: https://discord.pon.wiki/

## Dump & backup firmware <small>optional</small> { #dump-and-backup-firmware data-toc-label="Dump & backup firmware" }

1. [Enable SSH] from the web UI by following the steps outlined below in the shell upgrade section.

2. Login to the [WAS-110] remote shell over SSH using the *root* [shell credentials]{ data-preview target="_blank" }.

    ``` sh
    ssh -oHostKeyAlgorithms=+ssh-rsa -oPubkeyAcceptedKeyTypes=+ssh-rsa root@192.168.11.1
    ```

3. Execute the following command sequence from the [WAS-110] remote shell to dump the [WAS-110]'s volumes into its
   temporary directory and exit from the remote shell.

    ``` sh
    mkdir -p /tmp/fw; for part in kernelA bootcoreA rootfsA kernelB bootcoreB rootfsB; do VOL=$(ubinfo /dev/ubi0 -N "$part" | grep "Volume ID" | awk '{print $3}'); [ -n "$VOL" ] && { DEV="/dev/ubi0_$VOL"; OUT="/tmp/fw/ubi0_$VOL-$part.img"; echo "Dumping $part ($DEV) to: $OUT"; dd if="$DEV" of="$OUT"; }; done; exit
    ```

4. Execute the following command from the host PC terminal (not the [WAS-110] remote shell) to back-up the dumped
   volumes to your local user directory.

    === ":material-microsoft: Windows"

        ??? note "Prior to Windows 11 Build 22631.4391 (KB5044380) and Windows 10 Build 19045.5073 (KB5045594)..."
            The `scp` command used the legacy SCP protocol without the need for specifying the `-O` optional parameter.
            If you're using an older Windows build or an [OpenSSH](https://github.com/PowerShell/Win32-OpenSSH) version
            before 8.9.0.0, please remove `-O` from the `scp` command parameters.

            ``` sh
            systeminfo
            ssh -V # (1)!
            ```

            1. OpenSSH version info

            If you continue to have issues, consider installing and running [WinSCP](https://winscp.net/), a GUI client.

        **Command Prompt**

        ``` sh
        cd /D %UserProfile% & scp -O -oHostKeyAlgorithms=+ssh-rsa -oPubkeyAcceptedKeyTypes=+ssh-rsa root@192.168.11.1:/tmp/fw/ubi* .
        ```

        **Powershell / Windows Terminal**

        ``` sh
        cd /D %UserProfile%; scp -O -oHostKeyAlgorithms=+ssh-rsa -oPubkeyAcceptedKeyTypes=+ssh-rsa root@192.168.11.1:/tmp/fw/ubi* .
        ```

    === ":simple-apple: macOS / :simple-linux: Linux"

        ``` sh
        cd ~/; scp -O -oHostKeyAlgorithms=+ssh-rsa -oPubkeyAcceptedKeyTypes=+ssh-rsa 'root@192.168.11.1:/tmp/fw/ubi*' ./
        ```

## Shell upgrade <small>recommended</small> { #shell-upgrade data-toc-label="Shell upgrade" }

The extracted `local-upgrade.tar` includes a <ins>safer</ins> upgrade script in comparison to the built-in web UI.

### Enable SSH

SSH must be enabled from the web UI prior to running the shell commands.

<div class="swiper" markdown>

<div class="swiper-slide" markdown>

![WAS-110 login](install-8311-community-firmware-on-the-bfw-solutions-was-110/was_110_azores_login.webp){ loading=lazy }

</div>

<div class="swiper-slide" markdown>

![WAS-110 services](install-8311-community-firmware-on-the-bfw-solutions-was-110/was_110_azores_services.webp){ loading=lazy }

</div>

</div>

1. Within a web browser, navigate to
   <https://192.168.11.1/html/main.html#service/servicecontrol>
   and, if asked, input the *admin* [web credentials]{ data-preview target="_blank" }.

2. From the __Service Control__ page, check the __SSH__ checkbox and click __Save__.

### Upgrade firmware

Run the following commands from the host terminal to upgrade to the 8311 community firmware.

Input the *root* [shell credentials]{ data-preview target="_blank" } when asked.

=== ":material-microsoft: Windows"

    ??? note "Prior to Windows 11 Build 22631.4391 (KB5044380) and Windows 10 Build 19045.5073 (KB5045594)..."
        The `scp` command used the legacy SCP protocol without the need for specifying the `-O` optional parameter.
        If you're using an older Windows build or an [OpenSSH](https://github.com/PowerShell/Win32-OpenSSH) version
        before 8.9.0.0, please remove `-O` from the `scp` command parameters.

        ``` sh
        ssh -V # (1)!
        ```

        1. OpenSSH version info

        If you continue to have issues, consider installing and running [WinSCP](https://winscp.net/), a GUI client.

        Also, a popular GUI alternative to the `ssh` command is [Putty](https://putty.org/).

    ``` sh
    scp -O -oHostKeyAlgorithms=+ssh-rsa -oPubkeyAcceptedKeyTypes=+ssh-rsa %Temp%\8311\local-upgrade.tar root@192.168.11.1:/tmp/
    ssh -oHostKeyAlgorithms=+ssh-rsa -oPubkeyAcceptedKeyTypes=+ssh-rsa root@192.168.11.1 "tar xvf /tmp/local-upgrade.tar -C /tmp/ -- upgrade.sh && /tmp/upgrade.sh -y -r /tmp/local-upgrade.tar"
    ```

=== ":simple-apple: macOS / :simple-linux: Linux"

    ``` sh
    scp -O -oHostKeyAlgorithms=+ssh-rsa -oPubkeyAcceptedKeyTypes=+ssh-rsa /tmp/local-upgrade.tar root@192.168.11.1:/tmp/
    ssh -oHostKeyAlgorithms=+ssh-rsa -oPubkeyAcceptedKeyTypes=+ssh-rsa root@192.168.11.1 'tar xvf /tmp/local-upgrade.tar -C /tmp/ -- upgrade.sh && /tmp/upgrade.sh -y -r /tmp/local-upgrade.tar'
    ```

Once rebooted, enjoy the labor of love of the 8311 community. As a first step, it is recommended to perform a
[supplementary upgrade].

!!! note "New SSH host keys will be generated"
    Don't be alarmed when attempting to connect over SSH into the newly installed firmware and the following warning is
    presented:

    ```
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    @    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
    Someone could be eavesdropping on you right now (man-in-the-middle attack)!
    It is also possible that a host key has just been changed.
    The fingerprint for the ECDSA key sent by the remote host is
    SHA256:Y3WzWezEYQi5374JfEa4KMm2nqfkj7raMyZIi6TS+X4.
    Please contact your system administrator.
    Add correct host key in /home/8311/.ssh/known_hosts to get rid of this message.
    Offending ECDSA key in /home/8311/.ssh/known_hosts:1
    Host key for 192.168.11.1 has changed and you have requested strict checking.
    Host key verification failed.
    ```

    Simply delete the old host ID by running the following command and retry:

    ```
    ssh-keygen -R 192.168.11.1
    ```

## Web UI upgrade <small>not recommended</small> { #web-ui-upgrade data-toc-label="Web UI upgrade" }

!!! danger "Proceed with caution!"
    The Azores firmware upgrade utility on occasion is known to soft-brick itself. To recover, a host device with
    serial breakout on SFP pins 2 (rx) and 7 (tx) will be required.

    Alternatively, jump to the <ins>safer</ins> [shell upgrade](#shell-upgrade) within this guide.

<div class="swiper" markdown>

<div class="swiper-slide" markdown>

![WAS-110 login](install-8311-community-firmware-on-the-bfw-solutions-was-110/was_110_azores_login.webp){ loading=lazy }

</div>

<div class="swiper-slide" markdown>

![WAS-110 firmware upgrade](install-8311-community-firmware-on-the-bfw-solutions-was-110/was_110_azores_upgrade.webp){ loading=lazy }

</div>

</div>

!!! danger "50/50 chance of soft-bricking the [WAS-110] if proceeded!"

1. Within a web browser, navigate to
   <https://192.168.11.1/html/main.html#admin/upgrade>
   and, if asked, input the *admin* [web credentials]{ data-preview target="_blank" }.

2. From the __Firmware Upgrade__ page, browse for `local-upgrade.img` from the extracted download, and click
   __Upgrade__.

Patiently wait out the process, 4 to 5 minutes, or until the web session becomes unresponsive.

??? tip "Run a continuous ping"
    To recieve an early indication that the [WAS-110] has completed its upgrade reboot cycle, run a continuous ping:

    === ":material-microsoft: Windows"

        ``` sh
        ping -t 192.168.11.1
        ```

    === ":simple-apple: macOS / :simple-linux: Linux"

        ``` sh
        ping 192.168.11.1
        ```

Once rebooted, enjoy the labor of love of the 8311 community. As a first step, it is recommended to perform a
[supplementary upgrade].

## Supplementary upgrades

### A/B architecture

--8<-- "docs/xgs-pon/ont/bfw-solutions/was-110.md:mtd"

The [WAS-110] uses an A/B architecture, which means there are two adjacent firmware images: an active image
(the currently running and firmware) and an inactive image. Either image can be selected as active, and upon upgrade,
the inactive image will be overwritten and become the newly active image after reboot, i.e. committed image.

Furthermore, the OLT has the capability to select the active firmware image, upgrade the inactive image, and reboot
the ONT. It is therefore recommended to install the community firmware on both A and B slots.

### Web UI upgrade <small>safe</small> { #8311-web-ui-upgrade data-toc-label="Web UI upgrade" }

!!! info "Integrity first and foremost"
    The 8311 community firmware re-uses the <ins>safe</ins> shell upgrade logic throughout. Those who prefer the CLI
    may continue to use the [shell upgrade] method going forward.

    Furthermore, the 8311 community firmware includes an up-to-date `dropbear`[^4] build, which does not require the use
    of weak algorithms when using an SSH client, i.e.

    `-oHostKeyAlgorithms=+ssh-rsa -oPubkeyAcceptedKeyTypes=+ssh-rsa`

    can be removed from future command usage.

![WAS-110 firmware](install-8311-community-firmware-on-the-bfw-solutions-was-110/was_110_luci_firmware.webp){ loading=lazy }

1. Within a web browser, navigate to
   <https://192.168.11.1/cgi-bin/luci/admin/8311/firmware>
   and, if asked, input your *root* password.

2. From the __Firmware__ page, browse for `local-upgrade.tar` from the extracted download, and click __Upload__.

  [Debian]: https://www.debian.org/
  [WAS-110]: ../xgs-pon/ont/bfw-solutions/was-110.md
  [web credentials]: ../xgs-pon/ont/bfw-solutions/was-110.md#web-credentials
  [shell credentials]: ../xgs-pon/ont/bfw-solutions/was-110.md#shell-credentials
  [supplementary upgrade]: #supplementary-upgrades
  [shell upgrade]: #upgrade-firmware
  [Enable SSH]: #enable-ssh

[^1]: <https://github.com/djGrrr/8311-was-110-firmware-builder>
[^2]: <https://github.com/djGrrr/8311-xgspon-bypass>

      <https://github.com/djGrrr/8311-was-110-firmware-builder/blob/master/mods/>
[^3]: <https://www.debian.org/derivatives/>
[^4]: <https://en.wikipedia.org/wiki/Dropbear_(software)>
