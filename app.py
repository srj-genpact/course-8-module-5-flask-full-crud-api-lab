from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# Helper function to find an event by ID
def find_event_by_id(event_id):
    # Loop through events to find the matching ID
    for event in events:
        if event.id == event_id:
            return event
    return None

# Welcome route
@app.route("/", methods=["GET"])
def welcome():
    return jsonify({"message": "Welcome to the Event API!"})

# Retrieve all events
@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events])

# Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    # Extract JSON data
    data = request.get_json()
    # Validate input: title is required
    if not data or "title" not in data or not data["title"]:
        return jsonify({"error": "Bad Request: title is required"}), 400

    # Process: Generate a unique ID (max ID + 1) and create Event
    new_id = max([event.id for event in events], default=0) + 1
    new_event = Event(new_id, data["title"])
    events.append(new_event)

    # Return the created event with 201 Created status
    return jsonify(new_event.to_dict()), 201

# Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    # Find the event by ID
    event = find_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    # Extract JSON data
    data = request.get_json()
    # Validate input: title is required
    if not data or "title" not in data or not data["title"]:
        return jsonify({"error": "Bad Request: title is required"}), 400

    # Update event title
    event.title = data["title"]

    # Return the updated event with 200 OK status
    return jsonify(event.to_dict()), 200

# Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    # Find the event by ID
    event = find_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    # Remove the event from the list
    events.remove(event)

    # Return 204 No Content
    return "", 204

if __name__ == "__main__":
    app.run(debug=True)
