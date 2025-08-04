import logging

logging.basicConfig(
    format="[%(levelname)4s:%(filename)s %(lineno)4s %(asctime)s] %(message)s",
)
DEFAULT_LOGGER = logging.getLogger(name="post_ingestion_update")
DEFAULT_LOGGER.setLevel(logging.INFO)