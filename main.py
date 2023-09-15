from mkdocs_table_reader_plugin.readers import READERS
import yaml
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def define_env(env):
    with open("mkdocs.yml", "r") as mkdocs_file:
        mkdocs = yaml.load(mkdocs_file, Loader=Loader)

    file_list = []
    notices = None

    if mkdocs:
        tmp_list = [
            item
            for item in mkdocs["plugins"]
            if isinstance(item, dict) and item.get("macros")
        ]

        for macros_dict in tmp_list:
            for option, value_list in macros_dict["macros"].items():
                if option == "include_yaml":
                    for value in value_list:
                        if isinstance(value, dict):
                            for name, path in value.items():
                                if name == "notices":
                                    with open(path, "r") as notices_file:
                                        notices = yaml.safe_load(notices_file)
                                elif name == "vendors":
                                    with open(path, "r") as vendors_file:
                                        vendors = yaml.safe_load(vendors_file)
                                else:
                                    file_list.append(path)
                        elif isinstance(value, str):
                            file_list.append(value)
        
#        for filename in [
#            name for name in file_list if "_onu" in name or "_olt" in name
#        ]:
            
    @env.macro
    def read_csv(*args, **kwargs):
        return READERS["read_csv"](*args, **kwargs)
    
    @env.macro
    def read_table(*args, **kwargs):
        return READERS["read_table"](*args, **kwargs)
    
    @env.macro
    def read_fwf(*args, **kwargs):
        return READERS["read_fwf"](*args, **kwargs)
    
    @env.macro
    def read_excel(*args, **kwargs):
        return READERS["read_excel"](*args, **kwargs)
    
    @env.macro
    def read_yaml(*args, **kwargs):
        return READERS["read_yaml"](*args, **kwargs)
    
    @env.macro
    def read_json(*args, **kwargs):
        return READERS["read_json"](*args, **kwargs)
    
    @env.macro
    def read_raw(*args, **kwargs):
        return READERS["read_raw"](*args, **kwargs)

    @env.macro
    def credentials_table(type, credentials):
        if not credentials:
            return None

        buffer_templ = ""
        table_templ = "\n    | {0} | {1} | {2}"
        tab_templ = (
            '=== "{0}"\n    | Username | Password | {1}\n    | ---- | ---- | {2}'
        )
        priv = False
        for credential in credentials:
            username = credential.get("username")
            password = credential.get("password")
            privilege = credential.get("privilege")
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
    def specifications_tables(onu):
        specifications = onu.get("specifications", None)
        if not specifications:
            return
        
        buffer = ""
        div_templ = '<div class="headerless" markdown="1">\n{0}\n</div>'
        for spec in specifications:
            if isinstance(spec, str):
                buffer += read_table(spec, sep = ':', escapechar='\\') + "\n\n"
            elif isinstance(spec, dict):
                for key, value in spec.items():
                    buffer += "### " + key + "\n"
                    buffer += read_table(value, sep = ':', escapechar='\\') + "\n\n"
        return div_templ.format(buffer)
        
    @env.macro
    def resellers_table(odm):
        resellers = odm.get("resellers", None)
        if not resellers:
            return
        
        url_templ = "[{0}]({1})"
        row_templ = "\n| {0} | {1}{2} |"
        table_templ = "| Company | Product Number |\n| ---- | ---- |{0}\n"

        table_buffer = ""
        notes_buffer = ""

        for reseller in resellers:
            if not vendors.get(reseller["vendor"]):
                continue
            url = ''
            title = ''
            pn = reseller["pn"].replace("_", "-").upper()
            for key, value in vendors[reseller["vendor"]].items():
                if key == "web":
                    url = value
                elif key == "title":
                    title = value
            if not title:
                title =  reseller["vendor"]

            if reseller.get("note_id") != None:
                note_id = "[^" + str(reseller["note_id"]) + "]"
                note = reseller["note"]
                notes_buffer += note_id + ": " + note + "\n"
            else:
                note_id = ""
                    
            if url or url != "N/A":
                table_buffer += row_templ.format(url_templ.format(title, url), pn, note_id)
            else:
                table_buffer += row_templ.format(title, pn, note_id)
                        
        return table_templ.format(table_buffer) + "\n" + notes_buffer + "\n"

    @env.macro
    def connections_table(onu):
        connections = onu.get("connections")
        if not connections:
            return
        
        buffer = ""        
        for connection in connections:
            type = connection.get("type")
            credentials = connection.get("credentials")
            notices_list = connection.get("notices")
            buffer += credentials_table(type, credentials)
            if notices_list:
                for name in notices_list:
                    notice = notices.get(name)
                    if notice:
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
                or alias.get("connections") == None
                or not alias["connections"]
            ):
                return
            buffer += templ.format(alias["title"], connections_table(alias))

        if buffer:
            buffer = "## Vendor Credentials\n\n" + buffer

        return buffer
    
    @env.macro
    def calculate_onu(device, odm):
        if not device:
            return
        
        onu = {
            "specifications": None,
            "images": None,
            "connections": None,
            "notices": None,
            "content": None
        }
        if device.get("specifications") is not None:
            onu['specifications'] = device["specifications"]
        elif odm is not None and odm.get("specifications") is not None:
            onu['specifications'] = odm["specifications"]
        if device.get("images") is not None:
            onu['images'] = device["images"]
        elif odm is not None and odm.get("images") is not None:
            onu['images'] = odm["images"]
        if device.get("connections") is not None:
            onu['connections'] = device["connections"]
        elif odm is not None and odm.get("connections") is not None:
            onu['connections'] = odm["connections"]
        if device.get("notices") is not None:
            onu['notices'] = device["notices"]
        elif odm is not None and odm.get("notices") is not None:
            onu['notices'] = odm["notices"]
        if device.get("content") is not None:
            onu['content'] = device["content"]
        elif odm is not None and odm.get("content") is not None:
            onu['content'] = odm["content"]
        return onu
