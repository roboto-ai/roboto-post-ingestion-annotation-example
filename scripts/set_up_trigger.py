#!/usr/bin/env python3

from roboto.domain import actions
from roboto.exceptions import RobotoConflictException


def main():
    """
    This script creates a trigger which will launch `post_ingestion_update` after each ulog file has been fully
    ingested.
    """
    try:
        actions.Trigger.create(
            name="post_ingestion_ulg_decoration",
            action_name="post_ingestion_update",
            causes=[
                actions.TriggerEvaluationCause.FileIngest
            ],
            for_each=actions.TriggerForEachPrimitive.DatasetFile,
            required_inputs=["*.ulg"],
        )
    except RobotoConflictException:
        print("Trigger already exists, skipping creation")

if __name__ == "__main__":
    main()