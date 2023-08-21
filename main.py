

def define_env(env):

    @env.macro
    def credentials(type, cred_list):
        text = "=== \"{0}\"\n    | Username            | Password            | Privilege                                                        |\n    | ------------------- | ------------------- | ---------------------------------------------------------------- |\n"
        for cred in cred_list:
            username = cred['username']
            password = cred['password']
            privilege = cred.get('privilege')
            text += "    | " + username + " | " + password + " | "
            if privilege is not None:
                text += privilege + " |\n    "
            else:
                text += "Unknown |\n"
        return text.format(type)
