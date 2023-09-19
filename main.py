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

    print = env.start_chatting("pon.wiki")

    file_list = []
    notices = None

    if not mkdocs:
        return

    macros_index = next(
        (
            index
            for (index, d) in enumerate(mkdocs["plugins"])
            if isinstance(d, dict) and d.get("macros") != None
        ),
        None,
    )

    for option, value_list in mkdocs["plugins"][macros_index]["macros"].items():
        if option != "include_yaml":
            continue

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
        break

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

        table_templ = "\n    | {0} | {1} | {2}"
        tab_templ = (
            '=== "{0}"\n    | Username | Password | {1}\n    | ---- | ---- | {2}'
        )

        buffer_templ = ""
        priv = False

        for credential in credentials:
            username = credential.get("username")
            password = credential.get("password")
            privilege = credential.get("privilege")

            if privilege:
                priv = True

            buffer_templ += table_templ.format(username, password, privilege) + "{0}"

        if priv:
            return tab_templ.format(
                type, "Privilege |", "---- |"
            ) + buffer_templ.format(" |")
        else:
            return tab_templ.format(type, "", "") + buffer_templ.format("")

    @env.macro
    def specifications_tables(onu, div_class="headerless", no_heading=False):
        specifications = onu.get("specifications")

        if not specifications:
            return

        div_templ = '<div class="{1}" markdown="1">\n{0}\n</div>'
        templ = '=== "{0}"\n    {1}'
        buffer = ""

        if not no_heading:
            div_templ = "## Specifications\n" + div_templ

        for spec in specifications:
            if isinstance(spec, str):
                buffer += templ.format(" ", specifications_table(spec, nesting=1))

            elif isinstance(spec, dict):
                for key, _ in spec.items():
                    buffer += templ.format(key, specifications_table(spec, nesting=1))
                    break

        return div_templ.format(buffer, div_class)

    @env.macro
    def specifications_table(spec, nesting=0):
        if isinstance(spec, str):
            filename = "include/" + spec
            text = read_table(filename, sep=":", escapechar="\\")
            buffer = nest(text, level=nesting) + "\n\n"

        elif isinstance(spec, dict):
            for _, value in spec.items():
                filename = "include/" + value
                text = read_table(filename, sep=":", escapechar="\\")
                buffer = nest(text, level=nesting) + "\n\n"
                break

        return buffer

    @env.macro
    def resellers_table(odm):
        resellers = odm.get("resellers")

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

            url = ""
            title = ""
            pn = reseller["pn"].replace("_", "-").upper()

            for key, value in vendors[reseller["vendor"]].items():
                if key == "web":
                    url = value
                elif key == "title":
                    title = value

            if not title:
                title = reseller["vendor"]

            if reseller.get("note_id") != None:
                note_id = "[^" + str(reseller["note_id"]) + "]"
                note = reseller["note"]
                notes_buffer += note_id + ": " + note + "\n"
            else:
                note_id = ""

            if url or url != "N/A":
                table_buffer += row_templ.format(
                    url_templ.format(title, url), pn, note_id
                )
            else:
                table_buffer += row_templ.format(title, pn, note_id)

        return table_templ.format(table_buffer) + "\n" + notes_buffer + "\n"

    @env.macro
    def connections_table(onu, no_heading=False):
        connections = onu.get("connections")

        if not connections:
            return

        buffer = ""

        if not no_heading:
            buffer += "## Login Credentials\n"

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
        text = nest(text, level=nesting)

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

            buffer += templ.format(
                alias["title"], connections_table(alias, no_heading=True)
            )

        if buffer:
            buffer = "## Vendor Credentials\n\n" + buffer

        return buffer

    @env.macro
    def process_content_group(content_group):
        if isinstance(content_group, str):
            content = {"title": None, "uri": content_group, "tab": False}
            return {"heading": None, "sections": [content]}

        if not isinstance(content_group, dict):
            return None

        key = next(
            (key for (key, _) in content_group.items() if key),
            None,
        )

        if not key:
            return None

        if isinstance(content_group[key], str):
            content = {"title": None, "uri": content_group[key], "tab": False}
            return {"heading": key, "sections": [content]}

        if not isinstance(content_group[key], list):
            return None

        content_list = handle_content_list(content_group[key])

        print({"heading": key, "sections": content_list})
        return {"heading": key, "sections": content_list}

    def handle_content_list(content_group):
        content_list = []
        content = {}

        for group in content_group:
            if isinstance(group, str):
                content["uri"] = group
                content_list.append(content)
                content = {}

            elif isinstance(group, dict):
                key = next(
                    (key for (key, _) in group.items() if key),
                    None,
                )

                if not key:
                    return None

                if isinstance(group[key], list):
                    if key != "tabbed":
                        content_list.append(
                            {
                                "heading": key,
                                "sections": handle_content_list(group[key]),
                            }
                        )
                        continue

                    for obj in group[key]:
                        if not isinstance(obj, dict):
                            continue

                        content_sublist = []
                        content = {}

                        for title, uri in obj.items():
                            content["title"] = title
                            content["uri"] = uri
                            content["tab"] = True
                            content_sublist.append(content)
                            content = {}

                        content_list += content_sublist
                else:
                    content["title"] = key
                    content["uri"] = group[key]
                    content_list.append(content)
                    content = {}

            elif isinstance(group, list):
                continue

        return content_list

    @env.macro
    def nest(text, level=0):
        return text.replace("\n", "\n    " + level * "    ")

    @env.macro
    def heading(level):
        return level * "#" + " "
