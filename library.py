from riotwatcher import ApiError
import functools
from click._compat import raw_input
from enum import Enum, unique
from math import ceil

@unique
class Log_Mode(Enum):
    USER = 0 # ask for user response
    SILENT = 1 # silently handle errors
    VEBOSE = 2 # always print errors

def error_handler(func):
    @functools.wraps(func)
    def wrapper(*a, **kw):
        self = a[0]
        try:
            return func(*a, **kw)
        except ApiError as err:
            if err.response.status_code == 429:
                print('API Request Limit Exceeded')
            elif err.response.status_code == 404:
                print('404 command not found({}).'.format(func.__name__))
                while(self.debug != Log_Mode.SILENT):
                    if self.debug == Log_Mode.VEBOSE:
                        inp = "y"
                    else:
                        inp = raw_input("Print extended error? (YyNn): ")
                    if(inp.lower() == "y"):
                        print(err)
                        break
                    elif(inp.lower() == "n"):
                        break
                    
            else:
                raise
    return wrapper


