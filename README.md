# Fine Hotels + Resorts Deal Finder

This project enables you to find the best (priced) place to spend the Amex Platinum Card $200 hotel credit by querying real-time data to create an interactive graph of prices and dates.

See an example graph here: [https://tristanwhite.me/fhr.html](https://tristanwhite.me/fhr.html)

For an explanation of the motivation behind this project, see [this post](https://tristanwhite.me/optimizing-amex-hotel-credit.html)

Aggregates FHR search results from the Amex Travel website.

# Usage
Ensure `fhrlib.py` is in the same directory as `fhr_cli.py`.
Run `python3 fhr_cli.py -h` to see command line options.

```
$ python3 fhr_cli.py -h
usage: fhr_cli.py [-h] -b BEGIN -e END [-r REGION] [-s STATE] [-c CITY] [-o OUTPUT]

Aggregates FHR search results from the Amex Travel website.

options:
  -h, --help            show this help message and exit
  -b BEGIN, --begin BEGIN
                        The start date for data queries. Format: YYYY-MM-DD
  -e END, --end END     The end date for data queries. Format: YYYY-MM-DD
  -r REGION, --region REGION
                        The region used in the query.
  -s STATE, --state STATE
                        The state used in the query.
  -c CITY, --city CITY  The city used in the query. City name needs to be capitalized. This option isn't well tested - if not working, don't use this option and use only the state of the city; you should still be able to find
                        the hotel in the data.
  -o OUTPUT, --output OUTPUT
                        If provided, all data used to generate the final graph is saved to a csv file with this name.
```
