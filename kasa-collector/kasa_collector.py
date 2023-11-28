import datetime
import logging
import asyncio
import os
import time
from typing import Dict
from concurrent.futures.thread import ThreadPoolExecutor

from influxdb import InfluxDBClient

from kasa import SmartStrip, SmartPlug

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s {%(filename)s:%(lineno)d} %(name)s %(levelname)s:  %(message)s'
)
log = logging.getLogger('kasa_collector')
log.info("YAY I AM HERE")


influxdb_host_name = os.environ["INFLUXDB_HOST_NAME"]
influxdb_port = os.environ["INFLUXDB_PORT"]
influxdb_user_name = os.environ["INFLUXDB_USER_NAME"]
influxdb_password = os.environ["INFLUXDB_PASSWORD"]

log.info(f"influxdb_host_name={influxdb_host_name}")
log.info(f"influxdb_port={influxdb_port}")
log.info(f"influxdb_user_name={influxdb_user_name}")
log.info(f"influxdb_password={influxdb_password}")


time.sleep(2)


def submit_metric_to_db(metric_name: str, metric_value: float, metric_tags: Dict):
    time_str = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
    logging.debug(f"time_str={time_str}")
    json_body = [
        {
            "measurement": metric_name,
            "tags": metric_tags,
            "time": time_str,
            "fields": {
                "value": metric_value
            }
        }
    ]
    logging.debug(f"json_body={json_body}")
    client = InfluxDBClient(influxdb_host_name, influxdb_port, influxdb_user_name, influxdb_password, 'kasa')
    client.write_points(json_body)


async def pull_power_plug_data(plug_host_name: str):
    try:
        plug = SmartPlug(plug_host_name)
        await plug.update()
        log.info(f"current plug.alias={plug.alias},power={plug.emeter_realtime.power:.2f},is_on={plug.is_on},voltage={plug.emeter_realtime.voltage}")
        submit_metric_to_db("current_power_usage", plug.emeter_realtime.power, {"sample_level": "plug", "alias": plug.alias})
        submit_metric_to_db("current_state", 1 if plug.is_on else 0, {"sample_level": "plug", "alias": plug.alias})
        submit_metric_to_db("current_voltage", plug.emeter_realtime.voltage, {"sample_level": "plug", "alias": plug.alias})
    except Exception as e:
        log.error(f"got an error but will try again next time around plug_host_name={plug_host_name},message={str(e)}")


async def pull_power_strip_data(strip_host_name: str):
    try:
        strip = SmartStrip(strip_host_name)
        await strip.update()
        log.info(f"current strip.alias={strip.alias},power={strip.emeter_realtime.power:.2f}")
        submit_metric_to_db("current_power_usage", strip.emeter_realtime.power, {"sample_level": "strip", "alias": strip.alias})

        if strip_host_name == "192.168.69.136" and strip.alias != "Left Office Desk Strip":
            log.info("setting 192.168.69.136 alias to Left Office Desk Strip")
            await strip.set_alias("Left Office Desk Strip")
            log.info("done setting alias")

        if strip_host_name == "192.168.69.132" and strip.alias != "Right Office Desk Strip":
            log.info("setting 192.168.69.132 alias to Right Office Desk Strip")
            await strip.set_alias("Right Office Desk Strip")
            log.info("done setting alias")

        for child_plug in strip.children:
            if child_plug.alias.startswith("Z"):
                continue
            log.info(f"child_plug {child_plug.alias} power is {child_plug.emeter_realtime.power:.2f},is_on={child_plug.is_on},voltage={child_plug.emeter_realtime.voltage}")
            submit_metric_to_db("current_power_usage", child_plug.emeter_realtime.power, {"sample_level": "plug", "strip_alias": strip.alias, "alias": child_plug.alias})
            submit_metric_to_db("current_state", 1 if child_plug.is_on else 0, {"sample_level": "plug", "alias": child_plug.alias})
            submit_metric_to_db("current_voltage", child_plug.emeter_realtime.voltage, {"sample_level": "plug", "alias": child_plug.alias})
    except Exception as e:
        log.error(f"got an error but will try again next time around strip_host_name={strip_host_name},message={str(e)}")


def do_work(type: str, ip_address: str):
    if type == "strip":
        asyncio.run(pull_power_strip_data(ip_address))
    else:
        asyncio.run(pull_power_plug_data(ip_address))


if __name__ == "__main__":
    executor: ThreadPoolExecutor = ThreadPoolExecutor(20)

    while True:
        futures = []

        futures.append(executor.submit(do_work, "strip", "192.168.69.178"))
        futures.append(executor.submit(do_work, "strip", "192.168.69.195"))
        futures.append(executor.submit(do_work, "plug", "192.168.69.154"))
        futures.append(executor.submit(do_work, "plug", "192.168.69.111"))
        futures.append(executor.submit(do_work, "plug", "192.168.69.152"))
        futures.append(executor.submit(do_work, "plug", "192.168.69.68"))
        futures.append(executor.submit(do_work, "plug", "192.168.69.85"))
        futures.append(executor.submit(do_work, "plug", "192.168.69.167"))

        for future in futures:
            try:
                future.result(5)
            except:
                log.exception("hit timeout")

        log.info("")
        log.info("")
        time.sleep(0.1)
