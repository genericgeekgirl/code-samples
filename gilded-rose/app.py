#!flask/bin/python
from flask import Flask, jsonify

# Assumption: Guests stay for a single entire night (TODO: rolling basis)
# Assumption: There's at least eight hours between check out and check in

class Room:
    def __init__(self, number, guests, luggage):
        self.number = number

        self.allowed_guests = guests
        self.allowed_luggage = luggage

        self.available_guests = guests
        self.available_luggage = luggage

        self.cost_per_person = 0
        
    def calculate_cost_per_person(self):
        guests_in_room = self.allowed_guests - self.available_guests
        luggage_in_room = self.allowed_luggage - self.available_luggage

        if guests_in_room > 0:
            room_cost = 10 / guests_in_room
            print room_cost
            # Note: The calculation in the assignment double-charges for luggage
            # and also charges guests without luggage for luggage in their shared room
            storage_cost = 2 * luggage_in_room
            self.cost_per_person = room_cost + storage_cost

    def book(self, guests, luggage):

        # double-check whether there's enough room for guests and/or luggage
        if guests > self.available_guests:
            return -1
        if luggage > self.available_luggage:
            return -2

        # reduce availability
        self.available_guests -= guests
        self.available_luggage -= luggage

        self.calculate_cost_per_person()
        
        # if success: return room number
        return str(self.number), str(self.cost_per_person)

    
    # calculate amount of time needed to clean a room,
    # based on minimum 1 hour plus 30 minutes per guest
    def time_to_clean(self):
        time = 0;
        if (self.available_guests < self.allowed_guests):
            time = 60;
            guests_in_room = self.allowed_guests - self.available_guests
            time += guests_in_room * 30
        return time

    # reset guests and luggage when room is cleaned
    # if a room could not be cleaned within the 8 hours,
    # it's not reset and therefore not available to be booked
    def clean_room(self):
        self.available_guests = self.allowed_guests
        self.available_luggage = self.allowed_luggage
        
        
        
def gnome_cleaning_schedule():
    schedule = []
    
    # The gnome cleaning squad can work maximum 8 hours per day
    # TODO: handle multiple cleaning squads
    max_time = 8*60
    total_time = 0

    # for each room, get the amount of time needed to clean it and add to total_time
    # if total_time exceeds max_time, break (literally)
    for room in rooms:
        time = room.time_to_clean()
        if time > 0:
            total_time += time
            if total_time <= max_time:
                schedule.append({"room" : room.number, "time" : time})
            else:
                print "gnome working time exceeded"
                break

    return schedule
            

def clean_now(schedule):
    for job in schedule:
        clean_room(rooms([job["room"]]))

    



def find_availability(guests, luggage):
# rooms are first-come, first-serve

    available_rooms = []
    best_room = None

    for room in rooms:
        if room.available_guests >= guests and room.available_luggage >= luggage:
            available_rooms.append(room)

    if len(available_rooms) == 1:
        best_room = str(available_rooms[0].number)

    room_weights = []
    sorted_weights = []
    
    # ideally, we'd book a single guest in a single-vacancy room, without wasting luggage space
    # prioritize fitting guests over fitting luggage
    for room in available_rooms:
        room_weights.append([room.number, room.available_guests - guests, room.available_luggage - luggage])
        sorted_weights = sorted(room_weights, key=lambda x: (x[1], x[2]))

    best_room = str(sorted_weights[0][0])

    return best_room

    

# initialize four rooms
rooms = [Room(0,2,1), Room(1,2,0), Room(2,1,2), Room(3,1,0)]


###############################################################################
    
app = Flask(__name__)
    
@app.route('/availability/<int:guests>/<int:luggage>', methods=['GET'])

def get_availability(guests, luggage):

    if guests > 2:
        return "Please break booking up into 1 or 2 guests (TODO)"
    if luggage > 2:
        return "We cannot accomodate more than two pieces of luggage"

    room = find_availability(guests,luggage)

    if room:
        return "Room " + room + " is available."
    else:
        return "No rooms available."
    

@app.route('/book/<int:room>/<int:guests>/<int:luggage>', methods=['GET'])

def book_room(room, guests, luggage):    
    response = rooms[room].book(guests, luggage)

    if response == -1:
        return "ERROR: not enough room for guests"
    if response == -2:
            return "ERROR: not enough room for luggage"
    
    return "Booked room " + response[0] + ". Cost per person is " + response[1] + "."
    

@app.route('/schedule/', methods=['GET'])

def get_schedule():
    schedule = gnome_cleaning_schedule()

    string = ""
    for job in schedule:
        string += "Room " + str(job["room"]) + ": " + str(job["time"]) + " minutes<br />"

    if string is "":
        string = "The gnomes don't have any work to do!"
        
    return string



if __name__ == '__main__':
    app.run(debug=True)

    
