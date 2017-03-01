

class Validator:

    def __init__(self, cfg, log=None):
        self.log = log
        self.cfg = cfg

    def check_sections(self):
        if not "hubic" in self.cfg:
            self.log.error("No 'hubic' section in settings.cfg!")
            return False
        if not len(self.cfg) > 1:
            self.log.error("No backup sections defined in settings.cfg!")
            return False
        return True

    def check_hubic(self):
        cfg = self.cfg["hubic"]
        if not "email" in cfg:
            self.log.error("Hubic login not set in settings.cfg!")
            return False
        elif cfg["email"] == "no":
            self.log.error("Hubic login not set in settings.cfg!")
            return False
        if not "password" in cfg:
            self.log.error("Hubic password not set in settings.cfg!")
            return False
        elif cfg["password"] == "no":
            self.log.error("Hubic password not set in settings.cfg!")
            return False
        if not "crypt_password" in cfg:
            self.log.info("Hubic encryption key not set in settings.cfg, disabling encryption.")
        if not "backup_dir" in cfg:
            self.log.info("Hubic backup dir not set in settings.cfg, using /.")
        elif not cfg["backup_dir"] == "root" and not cfg["backup_dir"].endswith("/"):
            self.log.error("'backup_dir' needs to be 'root' or end with '/'")
            return False
        return True

    def validate(self):
        if not self.check_sections():
            return False
        if not self.check_hubic():
            return False
        return True
