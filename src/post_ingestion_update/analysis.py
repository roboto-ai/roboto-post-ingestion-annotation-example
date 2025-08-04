from roboto import RobotoClient
from roboto.domain import events, files, topics
from roboto.exceptions import RobotoNotFoundException
from .logging import DEFAULT_LOGGER as logger


class IngestedFileAnalyzer:
    def __init__(self, roboto_client: RobotoClient | None = None):
        self.__roboto_client: RobotoClient | None = roboto_client

    def run_post_ingestion_processing(self, fl: files.File):
        if not fl.ingestion_status == files.IngestionStatus.Ingested:
            logger.warning(f"File {fl} is not ingested, cannot run post ingestion processing")
            return

        self.__remove_flight_mode_events(fl)
        self.__add_cpu_load_metadata(fl)

    def __add_cpu_load_metadata(self, fl: files.File):
        tp: topics.Topic
        try:
            tp = fl.get_topic("cpuload")
        except RobotoNotFoundException:
            logger.warning(f"File {fl} does not have a 'cpuload' topic, cannot add average CPU load metadata")
            return

        tp_as_df = tp.get_data_as_df()
        max_cpu_load = tp_as_df.max()["load"]
        min_cpu_load = tp_as_df.min()["load"]
        avg_cpu_load = tp_as_df.mean()["load"]

        fl.put_metadata(
            {
                "max_cpu_load": max_cpu_load,
                "min_cpu_load": min_cpu_load,
                "avg_cpu_load": avg_cpu_load,
            }
        )

    def __remove_flight_mode_events(self, fl: files.File):
        file_events = events.Event.get_by_file(fl.file_id, roboto_client=self.__roboto_client)

        for event in file_events:
            if event.name.startswith("flight_mode."):
                event.delete()
