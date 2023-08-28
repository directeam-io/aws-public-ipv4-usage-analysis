# Public IPv4 Info

Recently AWS released a [statement](https://aws.amazon.com/blogs/aws/new-aws-public-ipv4-address-charge-public-ip-insights/) that starting February 2024 public IPv4 will be charged 0.005$ per hour.

As a way to help identifying and estimating the effect of this pricing update on the users, they released a tool called `Public IPv4 insights` in the IPAM console.

`Public IPv4 insights` shows how many public IPs exist per region and is based on the network interfaces.

`Public IPv4 insights` doesn't have API support, and for organizations with multiple accounts and regions it can be time consuming to iterate over all of them and estimate the future additional price.
As a solution for that, we created this repository that contains the followings scripts.

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

### Cost Estimation script

`public_ipv4_cost_estimation.py` provides retroactive cost estimation in USD based on Cost Explorer usage data.

You will be required to provide the start and end dates to run the script.

```bash
./public_ipv4_cost_estimation.py --start-date 2023-07-01 --end-date 2023-08-01
```

### Info script

`public_ipv4_info.py` provides information about current public IPv4 used in all regions.

```bash
./public_ipv4_info.py
```

