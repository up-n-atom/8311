import yaml
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def define_env(env):
    with open("mkdocs.yml", "r") as mkdocs_file:
        mkdocs = yaml.load(mkdocs_file, Loader=Loader)

    filename = None
    notices = None

    if mkdocs != None:
        file_list = []

        tmp_list = [
            item
            for item in mkdocs["plugins"]
            if isinstance(item, dict) and item.get("macros") != None
        ]

        for macros_dict in tmp_list:
            for option, value_list in macros_dict["macros"].items():
                if option == "include_yaml":
                    for value in value_list:
                        if isinstance(value, dict):
                            for name, path in value.items():
                                if name == "notices":
                                    filename = path

    if filename:
        with open(filename, "r") as notices_file:
            notices = yaml.safe_load(notices_file)

    @env.macro
    def credentials(type, cred_list):
        buffer_templ = ""
        table_templ = "\n    | {0} | {1} | {2}"
        tab_templ = (
            '=== "{0}"\n    | Username | Password | {1}\n    | ---- | ---- | {2}'
        )
        priv = False
        for cred in cred_list:
            username = cred.get("username")
            password = cred.get("password")
            privilege = cred.get("privilege")
            if privilege != None:
                priv = True
            buffer_templ += table_templ.format(username, password, privilege) + "{0}"

        if priv:
            return tab_templ.format(
                type, "Privilege |", "---- |"
            ) + buffer_templ.format(" |")
        else:
            return tab_templ.format(type, "", "") + buffer_templ.format("")

    @env.macro
    def iterate_specifications(onu):
        specifications = onu.get("specifications", None)
        if specifications != None:
            div_templ = '<div class="headerless" markdown="1">\n{0}\n</div>'
            text = "| | |\n| ---- | ---- |"
            first = True
            for spec in specifications:
                text += "\n| **" + spec[0] + "** | " + spec[1] + " |"
            return div_templ.format(text)

    @env.macro
    def iterate_credentials(onu):
        buffer = ""
        creds = onu.get("credentials")
        for cred in creds:
            type = cred.get("type")
            cred_list = cred.get("credentials")
            notices_list = cred.get("notices")
            buffer += credentials(type, cred_list)
            if notices_list != None:
                for name in notices_list:
                    notice = notices.get(name)
                    if notice != None:
                        buffer += "\n" + admonition(notice, nesting=1)
            buffer += "\n"
        return buffer

    @env.macro
    def admonition(notice, nesting=0):
        admon_templ = ' {0} "{1}"\n    ' + nesting * "    " + "{2}"
        type = notice.get("type", "info")
        title = notice.get("title", "")
        text = notice.get("text", "")
        expanding = notice.get("expanding", False)
        expand = notice.get("expand", False)
        text = text.replace("\n", "\n    " + nesting * "    ")
        if expanding:
            buffer = "???"
            if expand:
                buffer += "?"
            return nesting * "    " + buffer + admon_templ.format(type, title, text)
        else:
            return nesting * "    " + "!!!" + admon_templ.format(type, title, text)

    @env.macro
    def iterate_notices(onu):
        names = onu.get("notices")
        buffer = ""
        for name in names:
            notice = notices.get(name)
            if notice != None:
                buffer += "\n" + admonition(notice)
        return buffer

    @env.macro
    def generate_vendor_credentials(odm, onu_type):
        templ = '=== "{0}"\n    {1}'
        buffer = ""

        for name in odm.get("aliases"):
            if name == None:
                break
            alias = onu_type.get(name)
            if (
                alias == None
                or alias.get("credentials") == None
                or not alias["credentials"]
            ):
                return
            buffer += templ.format(alias["title"], iterate_credentials(alias))

        if buffer:
            buffer = "## Vendor Credentials\n\n" + buffer

        return buffer
    
    @env.macro
    def calculate_onu(device, odm):
        onu = {
            "specifications": None,
            "images": None,
            "credentials": None
        }
        if device is not None:
            if device.get("specifications") is not None:
                onu['specifications'] = device["specifications"]
            elif odm is not None and odm.get("specifications") is not None:
                onu['specifications'] = odm["specifications"]
            if device.get("images") is not None:
                onu['images'] = device["images"]
            elif odm is not None and odm.get("images") is not None:
                onu['images'] = odm["images"]
            if device.get("credentials") is not None:
                onu['credentials'] = device["credentials"]
            elif odm is not None and odm.get("credentials") is not None:
                onu['credentials'] = odm["credentials"]
        return onu
