from dataclasses import dataclass
from abc import ABC, abstractmethod
from datetime import time, date
from typing import List

class FlightReqInterface(ABC):
    @abstractmethod
    def get_flight(dest: str, start: date, end: date):
        pass

@dataclass
class Flight(FlightReqInterface):
    airline: str
    price: int

    depature_date: date
    depature_time: time
    arrival_date: date
    arrival_time: time

@dataclass
class FlightData():
    flights: List[Flight]

    def add(flight: Flight):
        pass