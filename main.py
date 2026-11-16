from datetime import datetime

CITIES_SERVED = ["delhi", "jaipur"]
TIME_SLOTS = ["morning", "afternoon", "evening", "night"]
MAX_STUDENT_YEAR = 5


class RideRequest:
    def __init__(self, student_name, destination, time_slot, student_year, submitted_at=datetime.now()):
        self.student_name = student_name

        if destination not in CITIES_SERVED:
            raise ValueError("Sorry, we don't go to that city.")
        self.destination = destination

        if time_slot not in TIME_SLOTS:
            raise ValueError("Please enter a valid time slot.")
        self.time_slot = time_slot

        if student_year < 1 or student_year > MAX_STUDENT_YEAR:
            raise ValueError("Please enter a valid student year.")
        self.student_year = student_year

        self.submitted_at = submitted_at

    def __str__(self):
        return f"{self.student_name} | {self.destination} | {self.time_slot} | Year {self.student_year} | {self.submitted_at}"


class Cab:
    def __init__(self, driver_name, seats, has_departed, destination, time_slot, student_list):
        self.driver_name = driver_name
        self.seats = seats
        self.has_departed = has_departed

        if destination not in CITIES_SERVED:
            raise ValueError("Sorry, we don't go to that city.")
        self.destination = destination

        if time_slot not in TIME_SLOTS:
            raise ValueError("Please enter a valid time slot.")
        self.time_slot = time_slot

        self.student_list = student_list

    def __str__(self):
        return f"{self.driver_name} | {self.seats} seats | {"Departed" if self.has_departed else "Not departed"} | {self.time_slot}"



ride_requests = []
cabs = []

print("Welcome to the Cab Pool Matcher!")
print("Enter 1 to add a new ride request")
print("Enter 2 to see everyone still waiting plus all cabs")
print("Enter 3 to quit")
while True:
    print()
    action = int(input("> "))
    
    if action == 1:
        student_name = input("Student name: ").strip()
        destination = input("Destination: ").strip().lower()
        time_slot = input("Time Slot: ").strip().lower()
        student_year = int(input("Student year: ").strip())

        req = RideRequest(student_name, destination, time_slot, student_year)
        ride_requests.append(req)

        print("Ride request added to queue!")

    elif action == 2:
        print("Students:")
        for req in ride_requests:
            print(req)

        print("Cabs:")
        for cab in cabs:
            print(cab)

    elif action == 3:
        print("Bye")
        break

print()