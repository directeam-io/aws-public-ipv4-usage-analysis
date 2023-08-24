#!/usr/bin/env python

import json
import sys
import dataclasses
from dataclasses import dataclass
import logging
import ipaddress
from typing import Dict, List


logger = logging.getLogger("this")
shandler = logging.StreamHandler()
logger.addHandler(shandler)
logger.setLevel(logging.INFO)


# Make sure boto3 is installed
try:
    import boto3
    import boto3.session
except ImportError:
    print("Please install boto3 and try again")


class DataclassJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


@dataclass
class AwsPublicIp:
    address: ipaddress.IPv4Address
    region: str
    tags: List[Dict[str, str]]
    resource_type: str
    resource_name: str


def ips_from_eips(session: boto3.session.Session):
    client = session.client("ec2")
    addresses = client.describe_addresses()["Addresses"]
    response = []
    for address in addresses:
        response.append(
                AwsPublicIp(
                    address=address.get("PublicIp"),
                    region=session.region_name,
                    resource_type="eip",
                    tags=address.get("Tags", []),
                    resource_name=address.get("InstanceId", None)
                    )
                )

    return response


def ips_from_enis(session: boto3.session.Session):
    client = session.client("ec2")
    enis = client.describe_network_interfaces()["NetworkInterfaces"]
    response = []

    for eni in enis:
        association = eni.get("Association")
        if association:
            response.append(
                    AwsPublicIp(
                        address=association.get("PublicIp"),
                        region=session.region_name,
                        resource_type="eni",
                        tags=eni.get("TagSet", []),
                        resource_name=eni.get("NetworkInterfaceId", None)
                        )
                    )

    return response


def ips_from_vpn(session: boto3.session.Session):
    client = session.client("ec2")
    vpns = client.describe_vpn_connections()["VpnConnections"]
    response = []
    for vpn in vpns:
        for tunnel_options in vpn["Options"]["TunnelOptions"]:
            response.append(
                        AwsPublicIp(
                            address=tunnel_options.get("OutsideIpAddress"),
                            region=session.region_name,
                            resource_type="eni",
                            tags=vpn.get("Tags", []),
                            resource_name=vpn.get("VpnConnectionId", None)
                            )
                    )
        for vgw in vpn["VgwTelemetry"]:
            response.append(
                        AwsPublicIp(
                            address=vgw.get("OutsideIpAddress"),
                            region=session.region_name,
                            resource_type="eni",
                            tags=vpn.get("Tags", []),
                            resource_name=vpn.get("VpnConnectionId", None)
                            )
                    )

    return response


def main():
    client = boto3.client("ec2")
    sessions = [boto3.session.Session(region_name=region["RegionName"])
                for region in client.describe_regions()["Regions"]]

    ips = []
    for session in sessions:
        for source in [ips_from_eips, ips_from_enis, ips_from_vpn]:
            ips.extend(source(session=session))

    unique_ip_count = len(set([ip.address for ip in ips]))

    response = {
            "IpAddresses": ips,
            "UniqueIpCount": unique_ip_count,
            "EstimatedCostForIpCount": unique_ip_count * 0.005 * 730,
            }

    json.dump(response, sys.stdout, indent=4, cls=DataclassJSONEncoder)


main()
