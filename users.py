
print("let's get started")

def get_users():

    f = open('users.txt', 'r')
    users = f.readlines()
    userlist = [elem.strip() for elem in users]
    
    f.close()


    return userlist