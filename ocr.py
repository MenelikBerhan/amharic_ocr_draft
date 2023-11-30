#!/usr/bin/env python3
"""
Command line interface for app
"""

import cmd
from datetime import datetime
# import models
# from models.amenity import Amenity
# from models.base_model import BaseModel
# from models.city import City
# from models.place import Place
# from models.review import Review
# from models.state import State
# from models.user import User
import shlex  # for splitting the line along spaces except in double quotes


class OCRCommand(cmd.Cmd):
    """ OCR CLI """
    prompt = '(ocr) '

    def do_EOF(self, arg):
        """Exits CLI"""
        print()
        return True

    def emptyline(self):
        """ overwriting the emptyline method """
        return False

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_ocr(self, arg):
        """Prints an instance as a string based on the class and id"""
        pass


if __name__ == '__main__':
    OCRCommand().cmdloop()
