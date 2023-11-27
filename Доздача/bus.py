from random import randint
import threading
import time


class Polling:
    def poll(self):
        pass

    def runPolling(self):
        while True:
            self.poll()

    def runPollingInThread(self):
        threading.Thread(target=self.runPolling).start()


class Street:
    title = "unknown street"
    previous = None

    def has_previous(self, street):
        return self.previous is not None and self.previous == street

    def __init__(self, title="unknown street", previous=None):
        self.title = title
        self.previous = previous


class BusStop(Polling, Street):
    persons = 0
    person_appear_chance = 0.5

    def poll(self):
        if randint(0, 10) > 10 * self.person_appear_chance:
            self.persons += 1
        time.sleep(0.5)

    def __init__(self, title, person_appear_chance=0.5):
        super().__init__(title)
        self.person_appear_chance = person_appear_chance

    def __str__(self) -> str:
        return f"[{self.title}]: {self.persons}🧍"


class Direction:
    streets = []
    number = 1

    def __init__(self, streets, number):
        self.streets = streets
        for i, street in enumerate(streets):
            street.previous = streets[i - 1] if i > 0 else None
        self.number = number


class CarPart(Polling):
    health = 1
    damage = 0.05
    title = "unknown part"

    def poll(self):
        self.health -= self.damage
        self.health = round(self.health, 2)
        time.sleep(1)

    def __init__(self, title, damage=0.05):
        self.title = title
        self.damage = damage

    def __str__(self) -> str:
        return f"[{self.title}]: {self.health}"


class Bus(Polling):
    direction = None
    street = None
    capacity = 0
    filling = 0
    speed = 1
    movement_direction = 'forward'
    last_collected_street = None
    bank = 1
    parts = (
        CarPart("Engine", 0.005),
        CarPart("Wheels", 0.1),
        CarPart("Doors", 0.001),
        CarPart("Windows", 0.005),
        CarPart("Seats", 0.1),
    )

    def refill(self):
        self.street = Street("Gas station")
        while self.bank < 1:
            self.bank += 0.1
            self.bank = round(self.bank, 2)
            time.sleep(0.5)
        self.street = self.direction.streets[0]

    def move(self, streets):
        if self.bank <= 0: return False

        next_street = list(filter(lambda x: x.has_previous(self.street), streets))

        if self.movement_direction == 'forward':
            next_street = next_street[0]
        else:
            next_street = self.street.previous

        if next_street is None:
            return False

        self.bank -= 0.1
        # round bank
        self.bank = round(self.bank, 2)
        self.street = next_street
        return True

    def collect(self):
        if self.last_collected_street != self.street and isinstance(self.street, BusStop):
            if self.filling > 0:
                self.filling = 0

        # if self.filling < self.capacity:

        self.last_collected_street = self.street

        diff = self.capacity - self.filling
        if (diff > self.street.persons):
            diff = self.street.persons
        self.filling += diff
        self.street.persons -= diff

    def poll(self):
        if self.bank <= 0:
            self.refill()
            return

        if isinstance(self.street, BusStop) and self.street.persons > 0 and self.last_collected_street != self.street:
            self.collect()
        else:
            index_of_street = self.direction.streets.index(self.street)
            if self.movement_direction == 'forward':
                self.movement_direction = 'forward' if index_of_street < len(self.direction.streets) - 1 else 'backward'
            else:
                self.movement_direction = 'backward' if index_of_street > 0 else 'forward'
            self.move(self.direction.streets)
        time.sleep(self.speed)

    def __init__(self, direction, capacity):
        self.direction = direction
        self.capacity = capacity
        self.street = direction.streets[0]

        for part in self.parts:
            part.runPollingInThread()

    def __str__(self) -> str:
        return f"[Bus {self.bank}/1]: {self.filling}/{self.capacity} on {self.street.title if self.street is not None else 'unknown street'}\n{str.join(';', [str(s) for s in self.parts])}"


stopA = BusStop("A", 0.2)
stopB = BusStop("B", 0.75)
stopC = BusStop("C", 0.5)

direction1 = Direction([stopA, Street("ab1"), Street("ab2"), Street("ab3"), stopB, Street('ac1'), Street("ac2"), stopC],
                       1)

stopA.runPollingInThread()
stopB.runPollingInThread()
stopC.runPollingInThread()

bus = Bus(direction1, 10)
bus.runPollingInThread()
bus.speed = 0.25

bus2 = Bus(direction1, 40)
bus2.runPollingInThread()

while (True):
    time.sleep(.25)
    print(stopA)
    print(stopB)
    print(stopC)
    print(bus)
    print(bus2)
    print("============================")
