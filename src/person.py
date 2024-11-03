import os.path
import re
from datetime import datetime


class InvalidPersonImage(Exception):
    pass

class PersonManager:
    def __init__(self):
        self.persons = []
    def load_persons_from_directory(self, dir_path: str):
        # to_m = datetime.now().month
        # to_d = datetime.now().day
        to_m = 10
        to_d = 7
        for root, path, files in os.walk(dir_path):
            for file in files:
                try:
                    person = Person(os.path.join(*(root.split('/') + [file])))
                except InvalidPersonImage as e:
                    print(e.__repr__())
                else:
                    if person.month == to_m and person.day == to_d:
                        self.persons.append(person)
        return self

class Person:
    def __init__(self, img_path: str):
        img_name = os.path.split(img_path)[-1]
        pattern = r'(.*?)-(\d{4})(\d{2})(\d{2}).(png|jpg)'
        matchObj = re.match(pattern, img_name)
        if matchObj is None:
            raise InvalidPersonImage(img_name)
        self.month = int(matchObj.group(3))
        self.day = int(matchObj.group(4))
        self.img_path = img_path
        self.name = matchObj.group(1)
