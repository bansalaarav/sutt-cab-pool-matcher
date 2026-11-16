from datetime import datetime
import json

CITIES_SERVED = ["delhi", "jaipur"]
TIME_SLOTS = ["morning", "afternoon", "evening", "night"]
MAX_STUDENT_YEAR = 5


class RideRequest:
    def __init__(self, student_name, destination, time_slot, student_year):
        self.student_name = student_name
        self.destination = destination
        self.time_slot = time_slot
        self.student_year = student_year
        self.submitted_at = datetime.now()

    def __str__(self):
        return f"{self.student_name} | {self.destination} | {self.time_slot} | Year {self.student_year} | {self.submitted_at}"


class Cab:
    def __init__(self, driver_name, seats, has_departed, destination, time_slot, student_list):
        self.driver_name = driver_name
        self.seats = seats
        self.has_departed = has_departed
        self.destination = destination
        self.time_slot = time_slot
        self.student_list = student_list

    def __str__(self):
        return f"{self.driver_name} | {self.seats} seats | {"Departed" if self.has_departed else "Not departed"} | {self.time_slot}"




ride_requests = []
cabs = []

# Load cabs from cabs.json
with open("cabs.json", "r") as file:
    for cab in json.load(file):
        cabs.append(Cab(cab["driver_name"], cab["seats"], cab["has_departed"], cab["destination"], cab["time_slot"], cab["student_list"]))


print("Welcome to the Cab Pool Matcher!")
print("Enter 1 to add a new ride request")
print("Enter 2 to see everyone still waiting plus all cabs")
print("Enter 3 to quit")
while True:
    print()

    action = input("1/2/3 > ").strip()
    
    if action == "1":
        student_name = input("Student name: ").strip()

        destination = input("Destination: ").strip().lower()
        if destination not in CITIES_SERVED:
            print("Sorry, we don't go to that city.")
            continue

        time_slot = input("Time Slot: ").strip().lower()
        if time_slot not in TIME_SLOTS:
            print("Please enter a valid time slot.")
            continue

        try:
            student_year = int(input("Student year: ").strip())
        except ValueError:
            print(f"Student year should be an integer from 1 to {MAX_STUDENT_YEAR}.")
            continue
        if student_year < 1 or student_year > MAX_STUDENT_YEAR:
            print(f"Please enter a valid student year (1 to {MAX_STUDENT_YEAR}).")
            continue

        req = RideRequest(student_name, destination, time_slot, student_year)
        ride_requests.append(req)

        print("Ride request added to queue!")

    elif action == "2":
        print("Students:")
        for req in ride_requests:
            print(req)

        print("Cabs:")
        for cab in cabs:
            print(cab)

    elif action == "3":
        print("Bye")
        break


# Save cab data to cabs.json
data = []
for cab in cabs:
    data.append(
        {
            "driver_name": cab.driver_name,
            "seats": cab.seats,
            "destination": cab.destination,
            "time_slot": cab.time_slot,
            "has_departed": cab.has_departed,
            "student_list": cab.student_list
        }
    )
with open("cabs.json", "w") as file:
    json.dump(data, file, indent=2)

print()