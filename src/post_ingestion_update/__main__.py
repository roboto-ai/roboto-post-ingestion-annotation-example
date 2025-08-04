from roboto.action_runtime import ActionRuntime

from .logging import DEFAULT_LOGGER as logger
from .analysis import IngestedFileAnalyzer as IngestedFileAnalyzer

action_runtime = ActionRuntime.from_env()
files_to_run_against = list(action_runtime.get_input().files)
logger.info("Found %s files to run against", len(files_to_run_against))

ingested_file_analyzer = IngestedFileAnalyzer(
    roboto_client=action_runtime.roboto_client
)

for fl, local_file in files_to_run_against:
    logger.info("Running against file %s", fl.relative_path)
    ingested_file_analyzer.run_post_ingestion_processing(fl)
