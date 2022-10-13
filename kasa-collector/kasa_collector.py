import logging

from tplink_smartplug import run_tplink_cmd

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s {%(filename)s:%(lineno)d} %(name)s %(levelname)s:  %(message)s'
)
log = logging.getLogger('kasa_collector')
log.info("YAY I AM HERE")

quiet = False

run_tplink_cmd("192.168.69.132", 9999, 'info', 5, quiet)
