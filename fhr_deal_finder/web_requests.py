from datetime import date, time
from flights import Flight, FlightReqInterface
from hotels import Hotel, HotelReqInterface
from dataclasses import dataclass

from bs4 import BeautifulSoup
import re

from playwright.sync_api import sync_playwright

@dataclass
class WebRequester(FlightReqInterface, HotelReqInterface):

    def get_flight(self, start: str, dest: str, begin: date, end: date):
        # Construct URL
        
        url = f"https://www.kayak.com/flights/{start}-{dest}/"
        url += f"{begin.isoformat()}/{end.isoformat()}?sort=bestflight_a"

        # Make the web request

        with sync_playwright() as p:
            browser = p.firefox.launch()
            context = browser.new_context()
            page = context.new_page()

            page.goto(url)

            soup=BeautifulSoup(page.content())
            deptimes = soup.find_all('div', attrs={'class': 'vmXl vmXl-mod-variant-large'})
            for d in deptimes:
                print(d)
                print()

        return
    
    def _parse_flight_date_outbound(soup: BeautifulSoup) -> date:
        pass

    def _parse_flight_depart_time_outbound(soup: BeautifulSoup) -> time:
        pass

    def _parse_flight_arrival_time_outbound(soup: BeautifulSoup) -> time:
        pass

    def _parse_flight_date_returning(soup: BeautifulSoup) -> date:
        pass

    def _parse_flight_depart_time_returning(soup: BeautifulSoup) -> time:
        pass

    def _parse_flight_arrival_time_returning(soup: BeautifulSoup) -> time:
        pass

    def get_hotel(dest: str, start: date, end: date):
        return super().get_hotel(start, end)


if __name__=="__main__":
    wr = WebRequester()
    begin = date(2024, 10, 29)
    end = date(2024, 11, 5)
    wr.get_flight(start="WAS", dest="LAX", begin=begin, end=end)