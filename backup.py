#!/usr/bin/python3
import os
import sys
import configparser
import logging
from validate_cfg import Validator

SCHED = True
try:
    from crontab import CronTab
except ImportError:
    print("Crontab support is not installed, will not schedule backups.")
    print(
        """
To schedule backups, install python3 package 'python-crontab' or \
do 'apt-get install python3-crontab'.
        """
    )
    SCHED = False

HUBIC_BIN = "/usr/local/bin/hubic-backup"

# Logging
logging.basicConfig(
    filename='debug.log',
    filemode='w',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)
logger.setLevel(logging.DEBUG)

# Get the full path of this script
BASEDIR = os.path.dirname(os.path.realpath(__file__))

# Load configuration from file
config = configparser.ConfigParser()
cfg_path = os.path.join(BASEDIR, "settings.cfg")


def check_requirements():
    if not os.path.isfile(HUBIC_BIN):
        logger.error(
            "hubic-backup is not installed, run setup.sh!"
        )
        sys.exit()


def load_cfg():
    if not os.path.isfile(cfg_path):
        logger.error("Could not locate {0}, exiting...".format(cfg_path))
        sys.exit()
    logger.info("Loading configuration from {0}".format(cfg_path))
    config.read(cfg_path)
    logger.debug("Loading validator...")
    validator = Validator(config, logger)
    if not validator.validate():
        logger.error("Failed to validate config file, exiting...")
        sys.exit()
    logger.debug("Config validated successfully, carrying on...")


def create_backup_command(backup_cfg, hubic_cfg):
    if hubic_cfg["backup_dir"] == "root":
        hubic_cfg["backup_dir"] = ""
    cmd = "{bin} -l {email} -p {pw} -i {src_dir} -o {dst_dir} -d".format(
        bin=HUBIC_BIN,
        email=hubic_cfg["email"],
        pw=hubic_cfg["password"],
        src_dir=backup_cfg["source_dir"],
        dst_dir=hubic_cfg["backup_dir"] + backup_cfg["hubic_dir"]
    )
    exclude_path = os.path.join(BASEDIR, backup_cfg.name + "_exclude.txt")
    if os.path.isfile(exclude_path):
        cmd += " --excludes " + exclude_path
    if backup_cfg["encrypt"] == "yes":
        cmd += " --crypt-password " + hubic_cfg["crypt_password"]
    return cmd


def execute_backup(cmd):
    os.system(cmd)


def run():
    hubic_cfg_section = config["hubic"]
    backup_sections = [
        config[s] for s in config.sections() if not s == "hubic"
    ]
    for bs in backup_sections:
        cmd = create_backup_command(bs, hubic_cfg_section)
        execute_backup(cmd)
        if bs.get("schedule") and SCHED:
            enable_schedule(bs, cmd)


def enable_schedule(cfg, cmd):
    cron  = CronTab(user=True)
    jobs = cron.find_comment("hubic-backup-{0}".format(cfg.name))
    for j in jobs:
        cron.remove(j)
    job = cron.new(command=cmd, comment="hubic-backup-{0}".format(cfg.name))
    schedule = cfg["schedule"]
    if schedule in [
        "reboot", "annually", "monthly", "weekly", "daily", "hourly"
    ]:
        job.setall("@" + schedule)
    else:
        logger.error(
            "Incorrect schedule value in {0}: {1}".format(
                cfg.name, schedule
            )
        )
        logger.error(
            "Valid settings: {0}".format(
                "reboot, annually, monthly, weekly, daily, hourly"
            )
        )

        return
    cron.write()
    logger.info("Scheduled '{0}' to run {1}.".format(cfg.name, schedule))


if __name__ == "__main__":
    check_requirements()
    load_cfg()
    run()
