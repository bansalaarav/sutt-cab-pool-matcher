from datetime import datetime
import json
import heapq

CITIES_SERVED = ["delhi", "jaipur"]
TIME_SLOTS = ["morning", "afternoon", "evening", "night"]
MAX_STUDENT_YEAR = 5


# this is what queues should look like:
# queues = {
    # ("delhi", "morning"): this is the queue -> [
#         (comparers, req),
#         (comparers, req),
#     ]
# }

queues = {(city, slot): [] for city in CITIES_SERVED for slot in TIME_SLOTS}


def add_req_to_queue(req):
    key = (req.destination, req.time_slot)
    value = (-req.student_year, req.submitted_at, req) # first checks student_year then submitted_at
    if key not in queues:
        queues[key] = []
    heapq.heappush(queues[key], value)


def get_waiting_requests():
    values = []
    for queue in queues.values():
        for entry in queue:
            values.append(entry)

    return [value[-1] for value in values]


def get_open_cabs():
    return [c for c in cabs if not c.has_departed]


def find_open_cab(destination, time_slot):
    for cab in get_open_cabs():
        if cab.destination == destination and cab.time_slot == time_slot:
            return cab
    return None


def dispatch_cab(destination, time_slot):
    cab = find_open_cab(destination, time_slot)
    queue = queues[(destination, time_slot)]

    if cab is None:
        print("There's no open cab for that trip.")
        return

    if not queue:
        print("Nobody is waiting for that trip.")
        return

    free = cab.seats - len(cab.student_list)
    for _ in range(min(free, len(queue))): # min bw free seats and no. of ppl in that queue
        req = heapq.heappop(queue)[-1] # see example queues at top of file if confused
        cab.student_list.append(req.student_name)
    
    cab.has_departed = True

    print(f"{cab.driver_name} dispatched with: {', '.join(cab.student_list) or 'nobody'}")


def find_matches():
    shown = {}

    for cab in get_open_cabs():
        key = (cab.destination, cab.time_slot)
        start = shown.get(key, 0)
        free = cab.seats - len(cab.student_list)
        picks = heapq.nsmallest(start+free, queues[key])[start:] # this is genius btw (inspired by ctp lab test)
        shown[key] = start + len(picks)
        print(f"{cab.driver_name} matches: {[entry[-1].student_name for entry in picks]}")


class RideRequest:
    def __init__(self, student_name, destination, time_slot, student_year, submitted_at=None):
        self.student_name = student_name
        self.destination = destination
        self.time_slot = time_slot
        self.student_year = student_year
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



# Initially get ride_requests from file and add to queue
ride_requests = []
try:
    with open("ride_requests.json", "r") as file:
        for req in json.load(file):
            add_req_to_queue(RideRequest(req["student_name"], req["destination"], req["time_slot"], req["student_year"], datetime.fromisoformat(req["submitted_at"])))
except FileNotFoundError:
    print("No ride_requests.json file found, working fresh")

# Initially load cabs from cabs.json
cabs = []
try:
    with open("cabs.json", "r") as file:
        for cab in json.load(file):
            cabs.append(Cab(cab["driver_name"], cab["seats"], cab["has_departed"], cab["destination"], cab["time_slot"], cab["student_list"]))
except FileNotFoundError:
    print("No cabs.json file found, working fresh")

print("Welcome to the Cab Pool Matcher!")


while True:
    print()
    print("1 Add a new ride request")
    print("2 See everyone waiting + all cabs")
    print("3 Find matches (preview)")
    print("4 Dispatch a cab")
    print("5 Quit")
    print()

    action = input("> ").strip()
    
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

        add_req_to_queue(RideRequest(student_name, destination, time_slot, student_year))

        print("Ride request added to queue!")

    elif action == "2":
        print("Students:")
        for req in get_waiting_requests():
            print(req)

        print("Cabs:")
        for cab in cabs:
            print(cab)

    # find matches
    elif action == "3":
        find_matches()

    elif action == "4":
        destination = input("Destination: ").strip().lower()
        if destination not in CITIES_SERVED:
                print("Sorry, we don't go to that city.")
                continue
        
        time_slot = input("Time Slot: ").strip().lower()
        if time_slot not in TIME_SLOTS:
            print("Please enter a valid time slot.")
            continue

        dispatch_cab(destination, time_slot)
    
    elif action == "5":
        print("Bye")
        break


# Save ride request data to json
data = []
for req in get_waiting_requests():
    data.append(
        {
            "student_name": req.student_name,
            "destination": req.destination,
            "time_slot": req.time_slot,
            "student_year": req.student_year,
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