#!/usr/bin/env python

import datetime
import json
import sys

from argparse import ArgumentParser

try:
    import boto3
except ImportError:
    print("Please install boto3 and try again")


def get_ipaddress_quantities(
        start_date: datetime.datetime,
        end_date: datetime.datetime) -> float:

    client = boto3.client("ce")

    usage_type_values = client.get_dimension_values(
            TimePeriod={
                "Start": str(start_date),
                "End": str(end_date),
                },
            Dimension='USAGE_TYPE',
            )["DimensionValues"]

    usage_types = [value["Value"] for value in usage_type_values
                   if "PublicIPv4" in value["Value"]]

    values = client.get_cost_and_usage(
            TimePeriod={
                "Start": str(start_date),
                "End": str(end_date),
                },
            Granularity="MONTHLY",
            Filter={
                "Dimensions": {
                    "Key": "USAGE_TYPE",
                    "Values": usage_types,
                    "MatchOptions": ["EQUALS"],
                    }
                },
            Metrics=["UsageQuantity"]
            )

    quantities = []
    for result in values["ResultsByTime"]:
        quantities.append(float(result["Total"]["UsageQuantity"]["Amount"]))

    return sum(quantities)


def main():
    parser = ArgumentParser()

    parser.add_argument(
            "--start-date", default=None,
            required=True, dest="start",
            type=datetime.date.fromisoformat
            )

    parser.add_argument(
            "--end-date", default=None,
            required=True, dest="end",
            type=datetime.date.fromisoformat
            )

    args = parser.parse_args()

    quantities = get_ipaddress_quantities(start_date=args.start, end_date=args.end)
    response = {"TotalHoursUsed": quantities, "EstimatedCost": quantities * 0.005}

    json.dump(response, sys.stdout, indent=4)


main()
