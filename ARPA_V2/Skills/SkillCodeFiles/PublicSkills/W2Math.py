from ARPA_V2.Skills.SkillCodeFiles.Skill import Skill
import math
import re


class W2Math(Skill):
    triggerIntent = "calculate"
    simple_mapper = None
    single_arg_mapper = None
    parsed_expression = None
    skillType = "public"

    def __init__(self):
        self.simple_mapper = {
            "plus": "+",
            "minus": "-",
            "multiply": "*",
            "into": "*",
            "divide": "/",
            "by": "/",
            "of": "*",
            "power": "**",
            "pow": "**",
            "*": "*",
            "^": "**",
            "pi": "math.pi",
            "e": "math.e",
            "upon": "/"
        }
        self.single_arg_mapper = {
            "sqrt": "math.sqrt",
            "sin": "math.sin",
            "cos": "math.cos",
            "tan": "math.tan",
            "log": "math.log",
            "deg": "math.degrees",
            "rad": "math.radians"
        }

        super(W2Math, self).__init__(trigger_intent=self.triggerIntent, skill_type=self.skillType)

    @staticmethod
    def __matchBrackets__(expr):
        bracket_stack = []
        token_list = [*expr]
        for token in token_list:
            if token == "(":
                bracket_stack.append(token)
            elif token == ")":
                try:
                    last = bracket_stack.pop()
                    if last != "(":
                        break
                except Exception as e:
                    return 0
        else:
            if len(bracket_stack) != 0:
                return 0
            else:
                return 1

    def __replaceSimpleOperators__(self, expr):
        ret_expr = ""
        pattern = re.compile("([a-z^]+)")
        tokens = pattern.finditer(expr)
        simple_maps = self.simple_mapper.keys()
        s_ind = 0
        for x in tokens:
            if x.group() in simple_maps:
                e_ind = x.span()[0]
                ret_expr += expr[s_ind:e_ind]
                ret_expr += f" {self.simple_mapper[x.group()]} "
                s_ind = x.span()[1]
        ret_expr += expr[s_ind:]
        return ret_expr

    def __replaceSingleArgMaps__(self, expr):
        ret_expr = ""
        pattern = re.compile("([a-z]+)\(")
        tokens = pattern.finditer(expr)
        single_arg_maps = self.single_arg_mapper.keys()
        s_ind = 0
        for x in tokens:
            if x.groups()[0] in single_arg_maps:
                e_ind = x.span()[0]
                ret_expr += expr[s_ind:e_ind]
                ret_expr += f" {self.single_arg_mapper[x.groups()[0]]}"
                s_ind = x.span()[1] - 1
        ret_expr += expr[s_ind:]
        return ret_expr

    def __processString__(self, raw_expr):
        ret_str = ""
        is_matched = self.__matchBrackets__(raw_expr)
        if is_matched == 0:
            return "[!] Syntax error: Unmatched Parenthesis."
        else:
            raw_expr = self.__replaceSimpleOperators__(raw_expr)
            raw_expr = self.__replaceSingleArgMaps__(raw_expr)
            try:
                return eval(raw_expr)
            except Exception as e:
                return raw_expr
        # return ret_str

    def run(self, raw_expression):
        self.parsed_expression = self.__processString__(raw_expression)


    def endSkill(self):
        print(self.parsed_expression)
