class Wish:
    def __init__(self, recipient, item, quantity, category, status, date):
        self.recipient = recipient
        self.item = item
        self.quantity = quantity
        self.category = category
        self.status = status  # "Pending" or "Fulfilled"
        self.date = date

    def to_dict(self):
        #Converts object attributes to a dictionary
        return {
            "recipient": self.recipient,
            "item": self.item,
            "quantity": self.quantity,
            "category": self.category,
            "status": self.status,
            "date": self.date
        }