
class UserDatabase():

    """
    Holds dictionary with entries for each user. Contains all user IDs of people that are monitored for each telegram user as a list
    """

    def __init__(self):
        self.__data = {}

    def add_user(self, telegram_id: int, user_id: int):
        if telegram_id in self.__data.keys():
            self.__data[telegram_id].append(user_id)
        else:
            self.__data[telegram_id] = [user_id]

    def get_monitored(self, telegram_id: int):
        if telegram_id in self.__data.keys():
            return self.__data[telegram_id]
        else:
            return []