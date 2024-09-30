from dataclasses import dataclass
from abc import ABC, abstractmethod
from datetime import date
from typing import List

class HotelReqInterface(ABC):
    @abstractmethod
    def get_hotel(dest: str, start: date, end: date):
        pass

@dataclass
class Hotel(HotelReqInterface):
    hotel: str
    price: int
    url: str
    
    arrival_date: date

@dataclass
class FlightData():
    flights: List[Hotel]

    def add(hotel: Hotel):
        pass