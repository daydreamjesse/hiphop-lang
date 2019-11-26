import re
from core import *
from hiphoperrors import hiphop_error, hiphop_eval_error

"""
<HHE> ::= <id>
        | open <filename> as <id>
        | save <id> as <filename>
        | apply <func> to <id>
        | apply-all [<funcs>] to <id>
        | save-macro [<funcs>] as <id>

<filename> ::= "<literal>"

<funcs> ::= <func>
        | <func>, <funcs>

<func> ::= <id> <nums>

<literal> ::= STRING

<nums> ::=
         | <num> <nums>
"""

def is_open_expr(expr_str):
    # For one line of the program, if valid program return object,
    # otherwise False

    match_filename = re.findall('(?<=open ")(.*)(?=" as)', expr_str)
    match_id = re.findall('(?<=open ")*(?<=" as )(.*)$', expr_str)
    if (len(match_filename) != 1 or len(match_id) != 1):
        raise hiphop_error("ParserError", 'Invalid syntax for `open` expression.')
    else:
        return open_expr(match_filename[0], match_id[0])

def is_save_expr(expr_str):

    match_id = re.findall('(?<=save )(.*)(?= as)', expr_str)
    match_filename = re.findall('(?<=save ).*(?<= as ")(.*)"', expr_str)
    # print("filename: {}; id: {}".format(match_filename[0], match_id[0]))
    if (len(match_filename) != 1 or len(match_id) != 1):
        raise hiphop_error("ParserError", 'Invalid syntax for `save` expression.')
    else:
        return save_expr(match_id[0], match_filename[0])

def is_apply_expr(expr_str):

    match = re.findall('(?<=apply )(.*)( to )(.*)', expr_str)
    if (len(match) != 1):
        raise hiphop_error("ParserError", 'Invalid syntax for `apply` expression.')
    match_func, _, match_id = match[0]
    match_function= match_func.split()
    match_funcname, match_args = match_function[0], match_function[1:]
    # print("funcname: {}; args: {}; id: {}".format(match_funcname, match_args, match_id))
    return apply_expr(match_funcname, match_args, match_id)

def is_apply_all_expr(expr_str):

    match = re.findall('(?<=apply-all \[)(.*)] to (.*)', expr_str)
    if (len(match) != 1):
        raise hiphop_error("ParserError", 'Invalid syntax for `apply-all` expression.')
    match_funcs, match_id = match[0]
    lambda_funcs = []
    new_funcs = match_funcs.split(",")
    for new_func in new_funcs:
        new_lambda = make_lambda_func(new_func.strip())
        if (isinstance(new_lambda, hiphop_error)):
            raise hiphop_error("ParserError", 'Unable to make lambda function for {}'.format(new_func))
        lambda_funcs.append(new_lambda)
    return apply_all_expr(lambda_funcs, match_id)

def is_save_macro_expr(expr_str):

    match = re.findall('(?<=save-macro \[)(.*)] as (.*)', expr_str)
    if (len(match) != 1):
        raise hiphop_error("ParserError", 'Invalid syntax for `save-macro` expression.')
    match_funcs, match_id = match[0]
    return save_macro_expr(match_funcs, match_id)

def is_identifier(expr_str):
    
    if (saved_macros.get_var(expr_str) != -1):
        print(saved_macros.get_var(expr_str))
        return True
    if (not isinstance(saved_vars.get_var(expr_str), int)):
        cv2.imshow(expr_str, saved_vars.get_var(expr_str))
        cv2.waitKey(4000)
        return True
    return False

class open_expr():

    def __init__(self, filename, id):

        self.filename = filename
        self.id = id

    def evaluate(self):
        openfile(self.filename, self.id)


class save_expr():

    def __init__(self, id, filename):

        self.id = id
        self.filename = filename

    def evaluate(self):
        savefile(self.id, self.filename)

class apply_expr():

    def __init__(self, funcname, args, img):

        """
        funcname: function to call when expression is evaluated
        args: list of arguments going into the function
        img: img expression
        """

        self.funcname = funcname
        self.args = args
        self.img = img

    def evaluate(self):

        if (self.funcname == "blur"):
            if (len(self.args) != 1):
                raise hiphop_eval_error("InvalidFunctionError", "Invalid number of arguments for `blur`. Usage: blur {radius}")
            blur(self.img, int(self.args[0]))
        elif (self.funcname == "grayscale"):
            if (len(self.args) != 0):
                raise hiphop_eval_error("InvalidFunctionError", "Invalid number of arguments for `grayscale`")
            grayscale(self.img)
        elif (self.funcname == "erode"):
            if (len(self.args) != 1):
                raise hiphop_eval_error("InvalidFunctionError", "Invalid number of argments for `erode`. Usage: erode {radius}")
            erode(self.img, int(self.args[0]))
        elif (self.funcname == "dilate"):
            if (len(self.args) != 1):
                raise hiphop_eval_error("InvalidFunctionError", "Invalid number of argments for `erode`. Usage: outline {radius}")
            dilate(self.img, int(self.args[0]))
        elif (self.funcname == "outline"):
            if (len(self.args) != 1):
                raise hiphop_eval_error("InvalidFunctionError", "Invalid number of argments for `outline. Usage: outline {radius}`")
            outline(self.img, int(self.args[0]))
        elif (self.funcname == "filtercolor"):
            if (len(self.args) != 6):
                raise hiphop_eval_error("InvalidFunctionError", "Invalid number of arguments for `filtercolor {lowR} {lowG} {lowB} {highR} {highG} {highB}`")
            filtercolor(self.img, int(self.args[0]), int(self.args[1]), int(self.args[2]),
                                  int(self.args[3]), int(self.args[4]), int(self.args[5]))
        elif (self.funcname == "scale"):
            if (len(self.args) != 2):
                raise hiphop_eval_error("InvalidFunctionError", "Invalid number of argments for `scale`")
            scale(self.img, float(self.args[0]), float(self.args[1]))
        elif (self.funcname == "crop"):
            if (len(self.args) != 4):
                raise hiphop_eval_error("InvalidFunctionError", "Invalid number of arguments for `crop {widthlow} {widthhigh} {heightlow} {heighthigh}`")
            crop(self.img, float(self.args[0]), float(self.args[1]), float(self.args[2]), float(self.args[3]))
        elif (saved_macros.get_var(self.funcname) != -1):
            if len(self.args) != 0:
                raise hiphop_eval_error("InvalidFunctionError", "Invalid number of arguments for `{}`".format(self.funcname))
            apply_all_expr(saved_macros.get_var(self.funcname), self.img).evaluate()
        else:
            raise hiphop_eval_error("InvalidFunctionError", "Function name does not exist.")

class apply_all_expr():

    def __init__(self, apply_funcs, img):

        """
        apply_funcs: lambda functions
        img: img expression
        """

        self.apply_funcs = apply_funcs
        self.img = img

    def evaluate(self):

        for func in self.apply_funcs:
            res = func(self.img)
            if (isinstance(res, hiphop_error)):
                return res

class save_macro_expr():

    def __init__(self, funcs, id):

        self.funcs = []

        # Parse the string of functions into lambda functions
        new_funcs = funcs.split(",")
        for new_func in new_funcs:
            lambda_func = make_lambda_func(new_func.strip())
            if (isinstance(lambda_func, hiphop_error)):
                raise hiphop_error("FunctionNotFound", "Could not create lambda function.")
            self.funcs.append(lambda_func)

        self.id = id

    def evaluate(self):
        saved_macros.add_var(self.id, self.funcs)


def make_lambda_func(str):
    # From a string representation, creates a lambda function
    # ie. grayscale 50

    func_tokens = str.split(" ")
    funcname, func_args = func_tokens[0], func_tokens[1:]
    # print("Making lambda function - funcname: {}, args: {}".format(funcname, func_args))

    if (funcname == "blur"):
        if (len(func_args) != 1):
            raise hiphop_eval_error("InvalidFunctionError", "Invalid number of arguments for `blur`")
        return lambda img: blur(img, int(func_args[0]))
    elif (funcname == "grayscale"):
        if (len(func_args) != 0):
            raise hiphop_eval_error("InvalidFunctionError", "Invalid number of arguments for `grayscale`")
        return lambda img: grayscale(img)
    elif (funcname == "erode"):
        if (len(func_args) != 1):
            raise hiphop_eval_error("InvalidFunctionError", "Invalid number of argments for `erode`")
        return lambda img: erode(img, int(func_args[0]))
    elif (funcname == "dilate"):
        if (len(func_args) != 1):
            raise hiphop_eval_error("InvalidFunctionError", "Invalid number of argments for `erode`")
        return lambda img: dilate(img, int(func_args[0]))
    elif (funcname == "outline"):
        if (len(func_args) != 1):
            raise hiphop_error("InvalidFunctionError", -1, "Invalid number of argments for `outline`")
        return lambda img: outline(img, int(func_args[0]))
    elif (funcname == "filtercolor"):
        if (len(func_args) != 6):
            raise hiphop_eval_error("InvalidFunctionError", "Invalid number of arguments for `filtercolor lowR lowG lowB highR highG highB`")
        return lambda img: filtercolor(img, int(func_args[0]), int(func_args[1]), int(func_args[2]),
                                int(func_args[3]), int(func_args[4]), int(func_args[5]))
    elif (funcname == "scale"):
        if (len(func_args) != 2):
            raise hiphop_eval_error("InvalidFunctionError", "Invalid number of argments for `scale`")
        return lambda img: scale(img, float(func_args[0]), float(func_args[1]))
    elif (funcname == "crop"):
        if (len(func_args) != 4):
            raise hiphop_eval_error("InvalidFunctionError", "Invalid number of arguments for `crop widthlow widthhigh heightlow heighthigh`")
        return lambda img: crop(img, float(func_args[0]), float(func_args[1]), float(func_args[2]), float(func_args[3]))
    else:
        raise hiphop_eval_error("InvalidFunctionError",  "Function name does not exist.")


class apply_funcs():

    def __init__(self, funcs_strings):
        """
        Parse string of functions and return list of lambda functions
        funcs_string: list of string representation of functions
        """
        self.apply_funcs = []
        for func_string in funcs_strings:
            self.apply_funcs.append(make_lambda_func(func_string))


class identifier():

    def __init__(self, boundvar):

        self.boundvar = boundvar

    def get_value(self):

        return self.boundvar
