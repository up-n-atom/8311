

def define_env(env):

    @env.macro
    def credentials(type, cred_list):
        buffer_templ = ""
        table_templ = "\n    | {0} | {1} | {2}"
        tab_templ = "=== \"{0}\"\n    | Username | Password | {1}\n    | ---- | ---- | {2}"
        priv = False
        for cred in cred_list:
            username = cred.get('username')
            password = cred.get('password')
            privilege = cred.get('privilege')
            if privilege != None: priv = True
            buffer_templ += table_templ.format(username, password, privilege) + "{0}"
        if priv:
            return tab_templ.format(type, "Privilege |", "---- |") + buffer_templ.format(" |")
        else:
            return tab_templ.format(type, "", "") + buffer_templ.format("")

    @env.macro
    def iterate_specifications(onu):
        specifications = onu.get('specifications', None)
        if specifications != None:
            div_templ = "<div class=\"headerless\" markdown=\"1\">\n{0}\n</div>"
            text = "| | |\n| ---- | ---- |"
            first = True
            for spec in specifications:
                text += "\n| **" + spec[0] + "** | " + spec[1] + " |"
            return div_templ.format(text)

    @env.macro
    def iterate_credentials(onu):
        buffer = ""
        creds = onu.get('credentials')
        for cred in creds:
            type = cred.get('type')
            cred_list = cred.get('credentials')
            buffer += credentials(type, cred_list) + "\n"
        return buffer

    @env.macro
    def admonition(notice):
        admon_templ = " {0} \"{1}\"\n    {2}"
        type = notice.get('type', 'info')
        title = notice.get('title', '')
        text = notice.get('text', '')
        expanding = notice.get('expanding', False)
        expand = notice.get('expand', False)
        if expanding:
            buffer = "???"
            if expand: buffer += "?"
            return buffer + admon_templ.format(type, title, text)
        else:
            return "!!!" + admon_templ.format(type, title, text)

    @env.macro
    def iterate_notices(onu, notices):
        names = onu.get('notices')
        buffer = ""
        for name in names:
            notice = notices.get(name)
            if notice != None:
                buffer += "\n" + admonition(notice)
        return buffer

    @env.macro
    def generate_vendor_credentials(onu, odm, onu_type):
        templ = "=== \"{0}\"\n    {1}"
        buffer = ''
        if onu != odm:
            return

        for name in odm.get('aliases'):
            if name == None:
                break
            alias = onu_type.get(name)
            if alias == None or alias.get('credentials') == None or not alias['credentials']:
                return
            buffer += templ.format(alias['title'], iterate_credentials(alias))

        if len(buffer) > 0:
            buffer = '## Vendor Credentials\n\n' + buffer
            
        return buffer
