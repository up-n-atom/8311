??? info "Management Connection"
    Some firmware versions use outdated algorithms for SSH and SCP, in this case it may be necessary to use the
    following parameters:

        -oKexAlgorithms=+diffie-hellman-group1-sha1 -oHostKeyAlgorithms=+ssh-dss

??? info "Management Connection"
    The module defaults to a gateway of `192.168.2.2` or `192.168.2.0`, so connecting can be tricky initially if it is not physically connected to the device you are connecting from.

!!! warning "RX_LOS"
    The module outputs an RX_LOS signal when no fibre/light is detected. Some equipment may disable the interface when detecting the RX_LOS signal.