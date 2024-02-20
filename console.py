#!/usr/bin/python3
""" Console Module """
import cmd
from datetime import datetime
import uuid
import re
from os import getenv
import shlex
import sys
import ast
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models import storage
# from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float
            }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for advanced command syntax.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = ''  # initialize line elements

        # scan for general formating - i.e '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # parse line left to right
            pline = line[:]  # parsed line

            # isolate <class name>
            _cls = pline[:pline.find('.')]

            # isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            # if parantheses contain arguments, parse them
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')  # pline convert to tuple

                # isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')
                # possible bug here:
                # empty quotes register as empty _id when replaced

                # if arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # check for *args or **kwargs
                    if pline[0] == '{' and pline[-1] == '}'\
                            and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
                        # _args = _args.replace('\"', '')
            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception as mess:
            pass
        finally:
            return line
    
    def __init__(self):
        super().__init__()
        self.storage = storage

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        exit()

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        exit()

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def convert_value(self, value, type_key):
        """Convert value based on the specified type."""
        if type_key == 't_str':
            return value[1:-1].replace('_', ' ')
        elif type_key == 't_float':
            return float(value)
        elif type_key == 't_int':
            return int(value)
        else:
            return value

    def do_create(self, args):
        """Create an object of any class"""
        ignored_attrs = ('id', 'created_at', 'updated_at', '__class__')
        class_nm = ''
        name_pattern = r'(?P<name>(?:[a-zA-Z]|_)(?:[a-zA-Z]|\d|_)*)'
        class_match = re.match(name_pattern, args)
        obj_kwargs = {}

        if class_match != None:
            class_name = class_match.group('name')
            prms_str = args[len(class_name):].strip()
            prms = prms_str.split(' ')
            prms_pattern = r'{}=({}|{}|{})'.format(name_pattern,
                r'(?P<t_str>"([^"]|\")*")',
                r'(?P<t_float>[-+]?\d+\.\d+)',
                r'(?P<t_int>[-+]?\d+)'
            )

            for prm in prms:
                prm_match = re.fullmatch(prms_pattern, prm)
                if prm_match != None:
                    key_name = prm_match.group('name')
                    type_key = next((k, v) for k, v in prm_match.groupdict().items() if v is not None)[0]
                    value = prm_match.group(type_key)
                    obj_kwargs[key_name] = self.convert_value(value, type_key)

                else:
                    class_name = args
                if not class_name:
                    print("** class name missing **")
                    return
                if getenv('HBNB_TYPE_STORAGE') == 'db':
                    if not hasattr(obj_kwargs, 'id'):
                        obj_kwargs['id'] = str(uuid.uuid4())
                    if not hasattr(obj_kwargs, 'created_at'):
                        obj_kwargs['created_at'] = str(datetime.now().isoformat())
                    if not hasattr(obj_kwargs, 'updated_at'):
                        obj_kwargs['updated_at'] = str(datetime.now().isoformat())
                        
                    new_instance = HBNBCommand.classes[class_name](**obj_kwargs)
                    new_instance.save()
                    print(new_instance.id)

                else:
                     new_instance = HBNBCommand.classes[class_name]()
                     for key, value in obj_kwargs.items():
                         if key not in ignored_attrs:
                             setattr(new_instance, key, value)
                     new_instance.save()
                     print(new_instance.id)

        """ Create an object of any class"""
        if not args:
            print("** class name missing **")
            return
        arguments = shlex.split(args)
        class_name = arguments[0]

        try:
            if class_name not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return

            pairs = arguments[1:]
            #new_instance = HBNBCommand.classes[class_name]()
            obj_kwargs = {}
            for pair in pairs:
                key, value = pair.split("=")
                value = value.replace('_', ' ')

                try:
                    obj_kwargs[key] = eval(value)
                    #setattr(new_instance, key, eval(value))
                except (SyntaxError, NameError):
                    obj_kwargs[key] = value
                    #setattr(new_instance, key, value)

            if getenv('HBNB_TYPE_STORAGE') == 'db':
                if 'id' not in obj_kwargs:
                    obj_kwargs['id'] = str(uuid.uuid4())
                if 'created_at' not in obj_kwargs:
                    obj_kwargs['created_at'] = str(datetime.now().isoformat())
                if 'updated_at' not in obj_kwargs:
                    obj_kwargs['updated_at'] = str(datetime.now().isoformat())

                new_instance = HBNBCommand.classes[class_name](**obj_kwargs)
                new_instance.save()
                print(new_instance.id)
            else:
                new_instance = HBNBCommand.classes[class_name]()
                for key, value in obj_kwargs.items():
                    setattr(new_instance, key, value)
                new_instance.save()
                print(new_instance.id)

        except Exception as e:
            print(f"Error: {e}")

        '''
        try:
            if class_name not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            new_instance = self.classes[class_name]()
            for i in arguments[1:]:
                key, value = shlex.split(i, posix=False).split("=")
        
                #if not hasattr(new_instance, key):
                   # print ("** attribute does not exist **")
                   # return
                #elif hasattr(new_instance, key):
                    #if value[0] == '"' and value[-1] == '"':
                     #   value = value[1:-1].replace('_', ' ')
                    #if '.' in value:
                     #   value = float(value)
                    #elif value.isdigit():
                     #   value = int(value) 
                setattr(new_instance, key, value)
        except Exception:
            pass
        new_instance.save()
        print(new_instance.id)
        storage.save()
        '''
    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, args):
        """ Method to show an individual object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]

        # guard against trailing args
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id
        try:
            print(storage._FileStorage__objects[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """ Destroys a specified object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id

        try:
            del(storage.all()[key])
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """ Shows all objects, or all objects of a class"""
        from models.engine.db_storage import DBStorage
        from models.engine.file_storage import FileStorage
        print_list = []

        if args:
            args = args.split(' ')[0]  # remove possible trailing args
            if args not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            objects = self.storage.all(HBNBCommand.classes[args])
            for k, v in objects.items():
                if k.split('.')[0] == args:
                    print_list.append(str(v))
        else:
            for cls_name in HBNBCommand.classes:
                objects = self.storage.all(HBNBCommand.classes[cls_name])
                for k,v in objects.items():
                    print_list.append(str(v))

        print(print_list)

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        count = 0
        for k, v in storage._FileStorage__objects.items():
            if args == k.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def do_update(self, args):
        """ Updates a certain object with new info """
        c_name = c_id = att_name = att_val = kwargs = ''

        # isolate cls from id/args, ex: (<cls>, delim, <id/args>)
        args = args.partition(" ")
        if args[0]:
            c_name = args[0]
        else:  # class name not present
            print("** class name missing **")
            return
        if c_name not in HBNBCommand.classes:  # class name invalid
            print("** class doesn't exist **")
            return

        # isolate id from args
        args = args[2].partition(" ")
        if args[0]:
            c_id = args[0]
        else:  # id not present
            print("** instance id missing **")
            return

        # generate key from class and id
        key = c_name + "." + c_id

        # determine if key is present
        if key not in storage.all():
            print("** no instance found **")
            return

        # first determine if kwargs or args
        if '{' in args[2] and '}' in args[2] and type(eval(args[2])) is dict:
            kwargs = eval(args[2])
            args = []  # reformat kwargs into list, ex: [<name>, <value>, ...]
            for k, v in kwargs.items():
                args.append(k)
                args.append(v)
        else:  # isolate args
            args = args[2]
            if args and args[0] == '\"':  # check for quoted arg
                second_quote = args.find('\"', 1)
                att_name = args[1:second_quote]
                args = args[second_quote + 1:]

            args = args.partition(' ')

            # if att_name was not quoted arg
            if not att_name and args[0] != ' ':
                att_name = args[0]
            # check for quoted val arg
            if args[2] and args[2][0] == '\"':
                att_val = args[2][1:args[2].find('\"', 1)]

            # if att_val was not quoted arg
            if not att_val and args[2]:
                att_val = args[2].partition(' ')[0]

            args = [att_name, att_val]

        # retrieve dictionary of current objects
        new_dict = storage.all()[key]

        # iterate through attr names and values
        for i, att_name in enumerate(args):
            # block only runs on even iterations
            if (i % 2 == 0):
                att_val = args[i + 1]  # following item is value
                if not att_name:  # check for att_name
                    print("** attribute name missing **")
                    return
                if not att_val:  # check for att_value
                    print("** value missing **")
                    return
                # type cast as necessary
                if att_name in HBNBCommand.types:
                    att_val = HBNBCommand.types[att_name](att_val)

                # update dictionary with name, value pair
                new_dict.__dict__.update({att_name: att_val})

        new_dict.save()  # save updates to file

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")

if __name__ == "__main__":
    HBNBCommand().cmdloop()
