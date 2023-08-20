# WAS-110I
![Image of WAS-110I](/img/was-110i.png){ align=center }

## Login Credentials

=== "Web UI"
    | Username | Password       |
    | -------- | -------------- |
    | admin    | QsCg@7249#5281 |
    | user     | user1234       |

    !!! warning "Changing Passwords"
        The password length isn't restricted from within the web UI; Passwords longer than 16 characters are sliced.

    ??? info "Password Storage"
        The default web UI password is stored in `/ptconf/param_ct.xml`. Modifications from the web UI are stored in
        `/ptconf/usrconfig_conf` and take precedence.

=== "Telnet / SSH / UART"
    | Username | Password       |
    | -------- | -------------- |
    | root     | QpZm@4246#5753 |

## Value-Added Resellers

| Company                                        | Product Number                                |
| ---------------------------------------------- | --------------------------------------------- |
| [Azores Networks](https://azoresnetworks.com/) | XSS[^1]                                       |
| [E.C.I. Networks](https://ecin.ca/)            | EN-XGSFPP-OMAC-V2                             |

[^1]: Azores Networks XSS formally WAS-110
