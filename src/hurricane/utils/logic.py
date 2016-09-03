import aenum


class Null:
    def __init__(self):
        pass

    def __str__(self):
        return 'null'


class Expression:
    """
    Expression building class for SQL where expression
    """

    def __init__(self):
        pass

    def __str__(self, *args, **kwargs):
        raise NotImplementedError()


class Condition(aenum.Enum):
    AND = 'and'
    OR = 'or'


class Comparator(aenum.Enum):
    EQ = '='
    NE = '!='
    GT = '>'
    GE = '>='
    LT = '<'
    LE = '<='
    IS = 'is'
    IS_NOT = 'is not'


class SingleExpression(Expression):
    def __init__(self, key, val, comparator):
        Expression.__init__(self)
        self.key = key
        self.val = val
        self.comparator = comparator

    def get_val_str(self):
        return str(self.val)

    def __str__(self, *args, **kwargs):
        return '{} {} {}'.format(str(self.key), str(self.comparator.value), self.get_val_str())


class ConditionalExpression(Expression):
    def __init__(self, left, right, condition):
        Expression.__init__(self)
        self.left = left
        self.right = right
        self.condition = condition

    def __str__(self, *args, **kwargs):
        return '({} {} {})'.format(str(self.left), str(self.condition.value), str(self.right))
