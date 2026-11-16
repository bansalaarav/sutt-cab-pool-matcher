from datetime import datetime
import json

CITIES_SERVED = ["delhi", "jaipur"]
TIME_SLOTS = ["morning", "afternoon", "evening", "night"]
MAX_STUDENT_YEAR = 5


def get_incomplete_requests():
    # sort ride requests in chronological order first
    reqs = sorted(ride_requests, key=lambda req: req.submitted_at)

    # then sort ride requests by seniority, this maintains relative order (called stable sort apparently)
    reqs = sorted(reqs, key=lambda req: req.student_year, reverse=True)

    # only requests that are incomplete ig
    reqs = [r for r in reqs if not r.completed]

    return reqs


def get_open_cabs():
    return [c for c in cabs if not c.has_departed]


def dispatch_cab(cab):
    for req in find_matches(cab):
        req.completed = True
        cab.student_list.append(req.student_name)

    cab.has_departed = True


def find_matches(cab, shown=[]):
    free = cab.seats - len(cab.student_list)
    matches = []
    for req in get_incomplete_requests():
        if (cab.destination == req.destination) and (cab.time_slot == req.time_slot) and req not in shown:
            matches.append(req)

    return matches[:free]


class RideRequest:
    def __init__(self, student_name, destination, time_slot, student_year, completed=False, submitted_at=None):
        self.student_name = student_name
        self.destination = destination
        self.time_slot = time_slot
        self.student_year = student_year
        self.completed = completed
        self.submitted_at = datetime.now()
        if submitted_at:
            self.submitted_at = submitted_at

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
        return f"{self.driver_name} | {self.destination} | {len(self.student_list)}/{self.seats} seats | {"Departed" if self.has_departed else "Not departed"} | {self.time_slot}"



# Initially get ride_requests from file
ride_requests = []

with open("ride_requests.json", "r") as file:
    for req in json.load(file):
        ride_requests.append(RideRequest(req["student_name"], req["destination"], req["time_slot"], req["student_year"], req["completed"], datetime.fromisoformat(req["submitted_at"])))

ride_requests = get_incomplete_requests()

# Initially load cabs from cabs.json
cabs = []
with open("cabs.json", "r") as file:
    for cab in json.load(file):
        cabs.append(Cab(cab["driver_name"], cab["seats"], cab["has_departed"], cab["destination"], cab["time_slot"], cab["student_list"]))


print("Welcome to the Cab Pool Matcher!")
print("1 Add a new ride request")
print("2 See everyone waiting + all cabs")
print("3 Find matches")
print("4 Dispatch a cab")
print("5 Quit")

while True:
    print()

    action = input("1/2/3/4/5 > ").strip()
    
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
        for req in get_incomplete_requests():
            print(req)

        print("Cabs:")
        for cab in cabs:
            print(cab)

    # find matches
    elif action == "3":
        shown = []
        for cab in get_open_cabs():
            matches = find_matches(cab, shown)
            shown += matches
            print(f"{cab.driver_name} matches: {[match.student_name for match in matches]}")


    elif action == "4":
        open_cabs = get_open_cabs()
        if not open_cabs:
            print("All cabs have left.")
            continue
        for cab in open_cabs:
            print(f"{open_cabs.index(cab)+1} {cab}")

        try:
            choice = int(input("Enter option number > ").strip())
        except ValueError:
            print(f"Please enter a number from 1 to {len(open_cabs)}.")
            continue

        if 1 <= choice <= len(open_cabs):
            cab = open_cabs[choice-1]
        else:
            print(f"Please enter a number from 1 to {len(open_cabs)}.")


        dispatch_cab(cab)
        print(f"{cab.driver_name} dispatched with: {', '.join(cab.student_list) or 'nobody'}")
    
    elif action == "5":
        print("Bye")
        break


# Save ride request data to json
data = []
for req in ride_requests:
    data.append(
        {
            "student_name": req.student_name,
            "destination": req.destination,
            "time_slot": req.time_slot,
            "student_year": req.student_year,
            "completed": req.completed,
            "submitted_at": req.submitted_at.isoformat()
        }
    )


with open("ride_requests.json", "w") as file:
    json.dump(data, file, indent=2)


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