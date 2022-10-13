import logging
import asyncio
from influxdb import InfluxDBClient

from kasa import SmartStrip

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s {%(filename)s:%(lineno)d} %(name)s %(levelname)s:  %(message)s'
)
log = logging.getLogger('kasa_collector')
log.info("YAY I AM HERE")


def submit_metric_to_db(metric_name, metric_value):
    json_body = [
        {
            "measurement": "metric_name",
            "tags": {
                "host": "server01",
                "region": "us-west"
            },
            "time": "2009-11-10T23:00:00Z",
            "fields": {
                "value": metric_value
            }
        }
    ]
    client = InfluxDBClient('influxdb', 8086, None, None, 'kasa')
    client.write_points(json_body)


async def pull_power_strip_data(strip_host_name: str):
    strip = SmartStrip(strip_host_name)
    await strip.update()
    log.info(f"current strip.alias={strip.alias},power={strip.emeter_realtime.power:.2f}")
    submit_metric_to_db("something", strip.emeter_realtime)

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


if __name__ == "__main__":
    asyncio.run(pull_power_strip_data("192.168.69.136"))
    asyncio.run(pull_power_strip_data("192.168.69.132"))
