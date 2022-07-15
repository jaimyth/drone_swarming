#Simple function to give every agent a unique ID
#Every time the function is called, the given ID is removed from the list of assignable IDs

ids = list(range(1,100))

def get_id():
    return ids.pop(0)