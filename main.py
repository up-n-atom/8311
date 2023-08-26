

def define_env(env):

    @env.macro
    def credentials(type, cred_list):
        buffer = ""
        table_templ = "\n    | {0} | {1} | {2}"
        tab_templ = "=== \"{0}\"\n    | Username | Password | {1}\n    | ---- | ---- | {2}"
        priv = False
        for cred in cred_list:
            username = cred.get('username')
            password = cred.get('password')
            privilege = cred.get('privilege')
            if privilege is not None:
                priv = True
                buffer += table_templ.format(username, password, privilege) + " |"
            else:
                buffer += table_templ.format(username, password, "")
        if priv:
            buffer = tab_templ.format(type, "Privilege |", "---- |") + buffer
        else:
            buffer = tab_templ.format(type, "", "") + buffer
        return buffer

    @env.macro
    def iterate_specifications(onu):
        specifications = onu.get('specifications', None)
        if specifications != None:
            text = ""
            first = True
            for spec in specifications:
                if first:
                    text += "| " + spec[0] + " | " + spec[1] + " |\n| ---- | ---- |"
                    first = False
                else:
                    text += "\n| " + spec[0] + " | " + spec[1] + " |"
            return text
