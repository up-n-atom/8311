Run the commands:

```sh
fw_printenv committed_image 
fw_printenv image0_version
fw_printenv image1_version 
fw_printenv image0_is_valid 
fw_printenv image1_is_valid
```

If `image0_is_valid` or `image1_is_valid` are set to `0`, assume there is no firmware installed for that image or that it may not be in a consistent state.

**Image 0**

If the commited image is set to `0` run the following commands to create a backup of the firmware:

```sh
cd /tmp
cat /proc/mtd > mtd.txt
cat /dev/mtd0 > 0_uboot.bin
cat /dev/mtd1 > 1_uboot_env.bin
cat /dev/mtd2 > 2_linux.bin
cat /dev/mtd3 > 3_rootfs.bin
cat /dev/mtd4 > 4_roofts_data.bin
cat /dev/mtd5 > 5_image1.bin
```

Once the backups are created, they can be copied from the ONU with the following commands:

```sh
scp {{ ontuser ~ "@" if ontuser is defined }}192.168.1.10:/tmp/mtd.txt .
scp {{ ontuser ~ "@" if ontuser is defined }}192.168.1.10:/tmp/0_uboot.bin .
scp {{ ontuser ~ "@" if ontuser is defined }}192.168.1.10:/tmp/1_uboot_env.bin .
scp {{ ontuser ~ "@" if ontuser is defined }}192.168.1.10:/tmp/2_linux.bin .
scp {{ ontuser ~ "@" if ontuser is defined }}192.168.1.10:/tmp/3_rootfs.bin .
scp {{ ontuser ~ "@" if ontuser is defined }}192.168.1.10:/tmp/4_roofts_data.bin .
scp {{ ontuser ~ "@" if ontuser is defined }}192.168.1.10:/tmp/5_image1.bin .
```

If `image 1` is also valid and you would like to back it up, run the following commands:

```sh
fw_setenv committed_image 1
reboot
```

then follow the directions for `image 1` below.

**Image 1**

If the commited image is set to `1` run the following commands to create a backup of the firmware:

```sh
cat /proc/mtd > mtd.txt
cat /dev/mtd0 > 0_uboot.bin
cat /dev/mtd1 > 1_uboot_env.bin
cat /dev/mtd2 > 2_image0.bin
cat /dev/mtd3 > 3_linux.bin
cat /dev/mtd4 > 4_rootfs.bin
cat /dev/mtd5 > 5_rootfs_data.bin
```

Once the backups are created, they can be copied from the ONU with the following commands:

```sh
scp {{ ontuser ~ "@" if ontuser is defined }}192.168.1.10:/tmp/mtd.txt .
scp {{ ontuser ~ "@" if ontuser is defined }}192.168.1.10:/tmp/0_uboot.bin .
scp {{ ontuser ~ "@" if ontuser is defined }}192.168.1.10:/tmp/1_uboot_env.bin .
scp {{ ontuser ~ "@" if ontuser is defined }}192.168.1.10:/tmp/2_image0.bin .
scp {{ ontuser ~ "@" if ontuser is defined }}192.168.1.10:/tmp/3_linux.bin .
scp {{ ontuser ~ "@" if ontuser is defined }}192.168.1.10:/tmp/4_rootfs.bin .
scp {{ ontuser ~ "@" if ontuser is defined }}192.168.1.10:/tmp/5_rootfs_data.bin .
```

If `image 0` is also valid and you would like to back it up, run the following commands:

```sh
fw_setenv committed_image 0
reboot
```

then follow the directions for `image 0` above.
