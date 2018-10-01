# gilded-rose

# Setup & Running the App

To run the API, you'll need Python and Flask (http://flask.pocoo.org/).

Then `python app.py` will run it on http://localhost:5000/

## Endpoints:

Check availability, given number of guests and luggage requirements:
`/availability/<int:guests>/<int:luggage>`

Book a given room:
`/book/<int:room>/<int:guests>/<int:luggage>`

Gnome Cleaning Squad schedule:
`/schedule/`

# How does it work?

Assumptions were made: Guests stay for a single entire night, and there's at least eight hours between check out and check in.

## availability endpoint

Given 1-2 guests and luggage up to 2 pieces, it tries to find the best available room. First we find all the rooms that fit the criteria (enough sleeping and storage space), then we weight the rooms based on how much space will be leftover if we book there. We try to minimize left-over space (i.e. a single guest should book in a single-vacancy room before taking a spot in a multiple-vacancy room; similarily with luggage space).

## booking endpoint

First we double-check that there is enough space in the given room for guests and luggage, then we reduce the availability of sleeping and storage spaces in the room and calculate the cost per person.

Note: The calculation in the assignment seems to double-charges for luggage, also charges guests without luggage for luggage in their shared room. I suppose this is for simplicity's sake, but really, luggage fees should only be charged to the guests with the luggage.

## schedule endpoint

For each room, we get the amount of time needed to clean in and add it to the schedule. If the schedule would go beyond 8 hours, that room isn't added to the schedule.

There's an unused cleaning function, which resets the availability of the rooms once they've been cleaned, according to the schedule. Therefore a room that could not be cleaned within 8 hours is not reset and will not be available for the next night.

# Extending it

More rooms would be easy to add, because we'd simply initialize them in the script, and they'd be handled the same as any other room. We need functionality to handle multiple gnome cleaning services. Extending their hours per squad just means changing the "max time" value. For multiple squads, we'd need to balance the cleaning load across the squads, rather than booking up one team at a time.

# Consultation

I checked the Python documentation for general syntax questions.

# Third-party tools

I used Flask to create the endpoints and Python.

Why? I like Python, and I feel very comfortable with it, and I've been using Flask a lot lately.

# Time

It took me about three hours, including a lunch and coffee breaks. Finishing the documentation took another 20 minutes on a different day.

Given more time, I'd need to implement a function that simulates time so the rooms are actually cleaned and re-booked. This would also allow me to figure out how to handle rolling bookings (multiple guests per day, although I think simulating it like a regular hotel is fine, too). I'd also write the code to handle multiple cleaning squads. And I'd also extend the code to handle parties larger than 2 people by splitting them across rooms, rather than requiring the end user to split their party before booking.

# Automated testing

We'd need to test various configurations of guests and luggage and room bookings, to make sure the expected responses are being returned. We'd also want to confirm that scheduling is working properly.