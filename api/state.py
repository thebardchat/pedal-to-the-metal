"""In-memory store — replace with SQLite/Postgres for production."""

from api.models.driver import Driver

ROSTER = [
    "Marcus", "Brittany", "Eboni", "Deletra", "Stacey", "Alexis",
    "Kenny", "Charlie", "Jamie", "Bryant", "Jonathon", "Jimmy", "Eddie", "Roberto",
]


class AppState:
    def __init__(self):
        self.drivers: dict[int, Driver] = {}
        self.loads: dict[int, object] = {}
        self._driver_seq = 0
        self._load_seq = 0
        self._seed_roster()

    def _seed_roster(self):
        for name in ROSTER:
            self._driver_seq += 1
            self.drivers[self._driver_seq] = Driver(id=self._driver_seq, name=name)

    def next_driver_id(self) -> int:
        self._driver_seq += 1
        return self._driver_seq

    def next_load_id(self) -> int:
        self._load_seq += 1
        return self._load_seq


db = AppState()
