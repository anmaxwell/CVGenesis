def get_users():

    with open ("users.txt", "r") as f:
        userlist = [elem.strip() for elem in f.readlines()]
    return userlist