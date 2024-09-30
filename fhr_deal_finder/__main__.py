#!/usr/bin/env python3

import datetime
import click
from . import fhrlib as fhr

class BeginDate(click.ParamType):
    name = "BeginDate"

    def convert(self, value, param, ctx):
        print(type(value), value)
        if isinstance(value, datetime.date):
            return value
        try:
            ret = datetime.date.fromisoformat(value)
        except:
            self.fail(f"Failed to convert {value!r} to yyyy-mm-dd format.")

        if ret < datetime.datetime.date(datetime.datetime.today()):
            raise click.BadParameter("Date cannot be earlier than today.")

        return ret

def checkBeginDate(ctx, param, value):
    if not value:
        return
    try:
        value = datetime.datetime.date(value)
    except:
        raise click.BadParameter("Begin date must be today or later")
    return value

@click.command()
@click.option('-b', '--begin',
    help="The start date for data queries. Format: yyyy-mm-dd",
    prompt="Enter a begin date (yyyy-mm-dd)",
    type=click.DateTime(formats=["%Y-%m-%d"]),
)
@click.option('-e', '--end',
    help="The end date for data queries. Format: yyyy-mm-dd",
    prompt="Enter an end date (yyyy-mm-dd)",
    type=click.DateTime(formats=["%Y-%m-%d"]),
)
@click.option('-o', '--output',
    help="""Name of the output csv file used to save the graph's source data""",
    default="output.csv",
    show_default=True,
)
@click.option('-s', '--state',
    help="State used in query. Required if city is given.",
    type=click.Choice(fhr.US_STATES, case_sensitive=False),
)
@click.option('-r', '--region',
    help="Region used in query.",
    type=click.Choice(fhr.REGIONS, case_sensitive=True),
    prompt=True,
    required=True,
)
@click.option("-c", "--city",
    help="""The city used in the query.
    City name needs to be capitalized.
    This option isn't well tested - if not working,
    don't use this option and use only the state of the city; you
    should still be able to find the hotel in the data.""",
    )
def cli(begin, end, output, city, state, region):
    # convert datetime params to date params
    begin = datetime.datetime.date(begin)
    end = datetime.datetime.date(end)
    # check that begin and end are valid
    if begin < datetime.datetime.date(datetime.datetime.today()):
        raise click.BadOptionUsage("begin", "begin date must be today or later")
    if end <= begin:
        raise click.BadOptionUsage("end", "end date must be later than begin date")

    df = fhr.getDfForDatesInLoc(
        state=state,
        start_date=begin, 
        end_date=end, 
        city=city, 
        fname=output, 
        region=region
    )

    if len(df) == 0:
        print('no hotels to show')
        exit(1)

    fig = fhr.dfToFig(df)
    fig.show()


if __name__=="__main__":
    cli() 

    '''
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

    # args = parser.parse_args()
    # checkArgs(vars(args))

    '''
