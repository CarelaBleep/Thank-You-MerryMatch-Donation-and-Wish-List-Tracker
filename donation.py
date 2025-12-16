class Donation:
    def __init__(self, donor, item, quantity, category, status, date):
        self.donor = donor
        self.item = item
        self.quantity = quantity
        self.category = category
        self.status = status  # "Available" or "Matched"
        self.date = date

    def to_dict(self):
        #Converts object attributes to a dictionary
        return {
            "donor": self.donor,
            "item": self.item,
            "quantity": self.quantity,
            "category": self.category,
            "status": self.status,
            "date": self.date
        }
