{% set sshuser = get_sshuser(device) %}

To flash these firmwares on your G-010S-P stick, you must first upload them via *SCP* to the stick's `/tmp` folder like so:

```shell
scp firmware.img {{ sshuser ~ "@" if sshuser is defined }}192.168.1.10:/tmp/firmware.img
```

Then verify the `md5sum` of the file on the stick matches what you uploaded with

```shell
md5sum /tmp/firmware.img`
```

After that, determine if you are currently booted into `image0`, or `image1` on the stick, either with:

```shell
fw_printenv committed_image
```

if that's `0` then you are on `image0`, and if that's `1` then you are on `image1`
Or, if you do:

```shell
cat /proc/mtd | grep image
```

if that says `image0`, you are on `image1`, and if that says `image1`, then you are on `image0`
Depending on which firmware image you are on, only one of the following steps will work:

**Image 0 (Flashing Image 1)**

```shell
mtd -e image1 write /tmp/firmware.img image1
fw_setenv image1_version PUTVERSIONFROMNAMEOFIMGHERE
fw_setenv image1_is_valid 1
fw_setenv target oem-generic
fw_setenv committed_image 1
```

**Image 1 (Flashing Image 0)**

```shell
mtd -e image0 write /tmp/firmware.img image0
fw_setenv image0_version PUTVERSIONFROMNAMEOFIMGHERE
fw_setenv image0_is_valid 1
fw_setenv target oem-generic
fw_setenv committed_image 0
```

Replace `PUTVERSIONFROMNAMEOFIMGHERE` in those commands with the name of the file you uploaded in the first step (without the `.img`suffix)

***If you pick the wrong set of commands to run, the first one will fail, do not proceed further if that is the case !***

After this, reboot the stick to boot the new firmware, and optionally do the same set of steps but for the other image