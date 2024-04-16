import fhrlib as fhr
import argparse
import datetime

def checkArgs(args: dict):
    # check that start date is today or later
    assert args['begin'] >= datetime.datetime.date(datetime.datetime.today()), "Start date must be no earlier than today."
    assert args['end'] > args['begin'], "End date cannot be today or earlier."
    if 'city' in args:
        assert 'state' in args, "State and region must be provided if city is given."

if __name__=="__main__":

    parser = argparse.ArgumentParser(
        description="Aggregates FHR search results from the Amex Travel website."
        )
    parser.add_argument('-b', '--begin', 
        required=True, 
        type=datetime.date.fromisoformat,
        help="The start date for data queries. Format: YYYY-MM-DD"
        )
    parser.add_argument('-e', '--end',
        required=True,
        type=datetime.date.fromisoformat,
        help="The end date for data queries. Format: YYYY-MM-DD"
        )
    parser.add_argument("-r", "--region",
        required=True,
        type=str,
        help="Required. The region used in the query.",
        choices=fhr.REGIONS,
        metavar="REGION"
        )
    parser.add_argument("-s", "--state",
        required=False,
        type=str,
        help="The state used in the query. Required if city is given.",
        choices=fhr.US_STATES,
        metavar="STATE"
        )
    parser.add_argument("-c", "--city",
        required=False,
        default=None,
        type=str,
        help="""The city used in the query.
        City name needs to be capitalized.
        This option isn't well tested - if not working,
        don't use this option and use only the state of the city; you
        should still be able to find the hotel in the data."""
        )
    parser.add_argument("-o", "--output",
        required=False,
        type=str,
        help="""If provided, all data used to generate the final graph
        is saved to a csv file with this name."""
        )

    args = parser.parse_args()
    checkArgs(vars(args))

    df = fhr.getDfForDatesInLoc(state=args.state, start_date=args.begin, end_date=args.end, city=args.city, fname=args.output, region=args.region)

    fig = fhr.dfToFig(df)
    fig.show()