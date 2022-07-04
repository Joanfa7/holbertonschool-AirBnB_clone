#!/usr/bin/python3
""" console contains the enery point of the command interpreter """
import cmd
import shlex
from models import classes
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):

    prompt = '(hbdb) '

    """This is a static method for keys & arguments for one place validation"""
    @staticmethod
    def key_for_command(command):
        new_command = command.split()
        count = len(new_command)
        key = None
        tmp_val = None
        if not command:
            print("** class name missing ** ")
        elif new_command[0] not in classes:
            print("** class doesn`t exist **")
        elif count < 2:
            print("** instance id missing **")
        else:
            new_command[1] = new_command[1].strip('",')
            tmp_val = '.'.join(new_command[0:2])
            if tmp_val not in storage.all():
                print("** no instance found **")
            else:
                key = tmp_val
        return key

    """This first 3 are the basic commands for the interpreter"""

    def emptyline(self):
        """ when user pres <ENTER> nothing is executed  """
        pass

    def do_EOE(self, command):
        """ End of file.. Ends program """
        return True

    def do_quit(self, command):
        """ Quit command to exit the program """
        return True

    def do_create(self, command):
        """Creates a new instance of BaseModel, saves it
        (in the JSON file) & prints id"""
        if command is None:
            print("** class name missing **")
        elif command in classes:
            n_class = classes[command]()
            print(n_class.id)
            storage.new(n_class)
            storage.save()
        else:
            print("** class doesn't exist **")

    def do_show(self, command):
        """Prints the string representation of an instance based
        on the name & id"""
        key = HBNBCommand.key_for_command(command)
        if key:
            print(storage.all()[key])

    def do_destroy(self, command):
        """Deletes an instance based on the class name and id"""
        key = HBNBCommand.key_for_command(command)
        if key:
            del storage.all()[key]
            storage.save()

    def do_all(self, command):
        """Prints all string representation of all
        instances based or not on the class name"""
        arguments = command.split()
        if not arguments:
            for a in storage.all().values():
                print(a)
        elif arguments[0] in classes:
            for b, c in storage.all().items():
                if b[0: b.index('.')] == arguments[0]:
                    print(c)
        else:
            print("** class doesn`t exist **")

    def do_update(self, command):
        """Updates the arguments.
        Usage: update <class name> <id> <attribute name> "<attribute value>"
        """
        key = HBNBCommand.key_for_command(command)
        if key:
            new_command = shlex.split(command)
            if len(new_command) < 3:
                print("** attribute name missing **")
            elif len(new_command) < 4 and '{' not in new_command[2]:
                print("** value missing **")
            else:
                obj = storage.all()[key]
                if '{' in new_command[2]:
                    str_dic = command[command.index('{'): command.index('}') + 1]
                    str_dic = str_dic.replace('"', "'")
                    adict = eval(str_dic)
                    for k, v in adict.items():
                        setattr(obj, k, v)
                else:
                    for i in range(2, len(new_command)):
                        new_command[i] = new_command[i].strip('",')
                        att_name, value = new_command[2:4]
                        if att_name in obj.__dict__:
                            cls = type(obj.__dict__[att_name])
                            value = cls(value)
                        setattr(obj, att_name, value)
                    obj.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
