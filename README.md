# Public IPv4 Info

Recently AWS released a [statement](https://aws.amazon.com/blogs/aws/new-aws-public-ipv4-address-charge-public-ip-insights/) that starting February 2024 public IPv4 will be charged 0.005$ per hour.

As a way to help identifying and estimating the effect of this pricing update on the users, AWS released a feature called [Public IPv4 insights](https://aws.amazon.com/about-aws/whats-new/2023/07/aws-public-ip-insights-vpc-ip-address-manager/) in the IPAM console.

The "AWS Public IPv4 Insights" feature provides information on the number of public IP addresses available in each region, sourced from network interfaces. However, this feature __does not have API support__.

For large organizations it can be time consuming to iterate over all regions and accounts in the AWS console to create an estimation of future additional cost.

As a solution, we created this repository that contains the followings scripts.

## Installation

Clone the repository:
``` bash
git clone https://github.com/directeam-io/aws-public-ipv4-usage-analysis.git
```

Create python virtual environment:
``` bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Usage

Both scripts provide their output to `stdout` in JSON format. 
logs are be sent to `stderr`.

### Cost Estimation script

`public_ipv4_cost_estimation.py` provides retroactive cost estimation in USD based on Cost Explorer usage data.

You will be required to provide the start and end dates to run the script.

```bash
# ./public_ipv4_cost_estimation.py --start-date 2023-07-01 --end-date 2023-08-01
```

### Info script

`public_ipv4_info.py` provides information about current public IPv4 used in all regions.

```bash
# ./public_ipv4_info.py
```

