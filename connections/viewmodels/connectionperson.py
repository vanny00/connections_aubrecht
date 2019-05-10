class ConnectionPerson():
    # Simple ViewModel for passing values to json
    def __init__(self, connection, from_person, to_person):
        self.connection = connection
        self.from_person = from_person
        self.to_person = to_person
