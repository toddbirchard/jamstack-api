"""Custom logger."""
from sys import stdout

import simplejson as json
from config import basedir, settings
from loguru import logger

DD_APM_FORMAT = (
    "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] "
    "[dd.service=%(dd.service)s dd.env=%(dd.env)s "
    "dd.version=%(dd.version)s "
    "dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s]"
    "- %(message)s"
)


def formatter(record):
    """Pass raw log to be serialized."""

    def serialize(log):
        """Parse log message into Datadog JSON format."""
        subset = {
            "time": log["time"].strftime("%m/%d/%Y, %H:%M:%S"),
            "message": log["message"],
            "level": log["level"].name,
            "function": log.get("function"),
            "module": log.get("name"),
        }
        if log.get("exception", None):
            subset.update({"exception": log["exception"]})
        return json.dumps(subset)

    record["extra"]["serialized"] = serialize(record)
    return "{extra[serialized]},\n"


def create_logger() -> logger:
    """Create custom logger."""
    logger.remove()
    logger.add(
        stdout,
        colorize=True,
        catch=True,
        format="<light-cyan>{time:MM-DD-YYYY HH:mm:ss}</light-cyan> | "
        + "<light-green>{level}</light-green>: "
        + "<light-white>{message}</light-white>",
    )
    # Readable logs
    if settings.ENVIRONMENT == "production":
        # Datadog
        logger.add(
            "/var/log/api/info.json",
            format=formatter,
            rotation="500 MB",
            compression="zip",
        )
        logger.add(
            "/var/log/api/apm.log",
            format=DD_APM_FORMAT,
            rotation="500 MB",
            compression="zip",
        )
        logger.add(
            f"/var/log/api/error.log",
            colorize=True,
            catch=True,
            format="<light-cyan>{time:MM-DD-YYYY HH:mm:ss}</light-cyan> | "
            + "<light-green>{level}</light-green>: "
            + "<light-white>{message}</light-white>",
            rotation="500 MB",
            compression="zip",
            level="ERROR",
        )
    else:
        logger.add(
            f"{basedir}/logs/error.log",
            colorize=True,
            catch=True,
            format="<light-cyan>{time:MM-DD-YYYY HH:mm:ss}</light-cyan> | "
            + "<light-green>{level}</light-green>: "
            + "<light-white>{message}</light-white>",
            rotation="500 MB",
            compression="zip",
            level="ERROR",
        )
    return logger


LOGGER = create_logger()
