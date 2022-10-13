import datetime
import logging
import asyncio
import time
from typing import Dict

from influxdb import InfluxDBClient

from kasa import SmartStrip


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s {%(filename)s:%(lineno)d} %(name)s %(levelname)s:  %(message)s'
)
log = logging.getLogger('kasa_collector')
log.info("YAY I AM HERE")


def submit_metric_to_db(metric_name: str, metric_value: float, metric_tags: Dict):
    time_str = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
    logging.info(f"time_str={time_str}")
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
    logging.info(f"json_body={json_body}")
    client = InfluxDBClient('ec2-52-207-133-65.compute-1.amazonaws.com', 38086, 'if_user', 'if_password', 'kasa')
    client.write_points(json_body)


async def pull_power_strip_data(strip_host_name: str):
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
        log.info(f"child_plug {child_plug.alias} power is {child_plug.emeter_realtime.power:.2f}")
        submit_metric_to_db("current_power_usage", child_plug.emeter_realtime.power, {"sample_level": "plug", "strip_alias": strip.alias, "alias": child_plug.alias})


if __name__ == "__main__":
    while True:
        try:
            asyncio.run(pull_power_strip_data("192.168.69.136"))
            asyncio.run(pull_power_strip_data("192.168.69.132"))
        except Exception as e:
            log.exception("got an error but will try again next time around")

        log.info("")
        log.info("")
        time.sleep(1)
