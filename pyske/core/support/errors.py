class NotEqualSizeError(Exception):
    """
    Exception raised for different sizes between structures

    Attributes
    ----------
    message:
        explanation of the error
    """

    def __init__(self, message):
        self.message = "[NotEqualSizeError] "+ message


class EmptyError(Exception):
    """
    Exception raised if a function is applied to an empty structure

    Attributes
    ----------
    message:
        explanation of the error
    """

    def __init__(self, message):
        self.message = "[EmptyError] "+ message


class UnknownTypeError(Exception):
    """
    Exception raised if a type is unknown

    Attributes
    ----------
    message:
        explanation of the error
    """

    def __init__(self, message):
        self.message = "[UnknownTypeError] "+ message


class IllFormedError(Exception):
    """
    Exception raised if a function is applied to a ill formed structure

    Attributes
    ----------
    message:
        explanation of the error
    """

    def __init__(self, message):
        self.message = "[IllFormedError] "+ message


class ApplicationError(Exception):
    """
    Exception raised if a function is applied to not the good structure

    Attributes
    ----------
    message: 
        explanation of the error
    """
    
    def __init__(self, message):
        self.message = "[ApplicationError] "+ message


class NotSameTagError(Exception):
    """
    Exception raised if a function is applied to several tagged value with not the same tag

    Attributes
    ----------
    message: 
        explanation of the error
    """

    def __init__(self, message):
        self.message = "[EmptyError] "+ message


class ConstructorError(Exception):
    """
    Exception raised if an instance cannot be created

    Attributes
    ----------
    message: 
        explanation of the error
    """
    
    def __init__(self, message):
        self.message = "[ConstructorError] "+ message