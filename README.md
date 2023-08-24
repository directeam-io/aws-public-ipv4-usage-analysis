# Public IPv4 Info

This repository was created as a response to the lack of API support for the new IPv4 (IPAM) Insights.

## Cost Estimation

the script `public_ipv4_cost_estimation.py` provides retroactive cost estimation based on Cost Explorer usage data.

You will be required to provide the start and end dates to run the script.

```bash
./public_ipv4_cost_estimation.py --start-date 2023-07-01 --end-date 2023-08-01
```

Note: Cost Explorer end dates are exclusive. the example above will provide information from 2023-07-01 to 2023-07-31.

## Info

The `public_ipv4_info.py` script provides information about current public IPv4 used in all regions.
The cost estimation is a projection of consistent usage for the IPv4s currently in use in your infrastructure.

```bash
./public_ipv4_info.py
```

## Additional Info

Note that all cost estimation calculations dependant on CE providing cost information in USD.
