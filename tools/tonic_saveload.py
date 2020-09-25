from models.customer import Customer as Customer
from models.drink_order import DrinkOrder as DrinkOrder
from models.drink import Drink as Drink
from os import path as path
from typing import Iterable
import json


class_flag = "  "


def json_save(save_path: str, instances: Iterable[type]) -> str:
    "Saves an interable of class instances to a JSON. Returns True if successfully saved, or False otherwise."
    
    if path.exists(save_path) == False:
        with open(save_path, "x"):
            pass
    
    try:
        with open(save_path, "w") as file_:
            serializable_instances = []

            for instance in instances:
                serializable_instances.append(_get_instance_vars(instance))
            
            json.dump(serializable_instances, file_)
        
        #print("SAVE SUCCESS!")
        return True
    except:
        #print("SAVE FAIL!")
        return False


def json_load(load_path: str) -> [type]:
    "Returns a list of class instances from a JSON. Returns a list of the specified Class type if successful, or None otherwise."
    
    if path.exists(load_path) == False:
        with open(load_path, "x"):
            pass
    
    try:
        with open(load_path, "r") as file_:
            instance_list = []
            
            for dict_ in json.load(file_):
                new_instance = _make_instance_from_vars(dict_)
                instance_list.append(new_instance)

        #print("LOAD SUCCESS!")
        return instance_list
    except:
        #print("LOAD FAIL!")
        return None


def _get_instance_vars(instance):
    dict_vars = (list(vars(instance).values()))

    for i, var in enumerate(dict_vars):
        is_any_instance = hasattr(var, '__dict__') or hasattr(var, '__slots__')
        
        if is_any_instance == True:
            dict_vars[i] = _get_instance_vars(var)

    return_dict = {(class_flag + type(instance).__name__): dict_vars}
    return return_dict


def _make_instance_from_vars(dict_):
    instance_type_as_string = list(dict_.keys())[0].replace(class_flag, "")
    return_instance = eval(instance_type_as_string)()
    var_names = list(vars(return_instance).keys())

    for i, var in enumerate(list(dict_.values())[0]):
        if type(var) == dict:
            key = list(var.keys())[0]
            if type(key) == str:
                if key.find(class_flag) != -1:
                    var = _make_instance_from_vars(var)
        
        var_name = var_names[i]
        vars(return_instance)[var_name] = var

    return return_instance