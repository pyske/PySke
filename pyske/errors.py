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


class EmptyError(Exception):
    """
    Exception raised if a function is applied to an empty list that is not fit for

    Attributes
    ----------
    message: 
        explanation of the error
    """
    
    def __init__(self, message):
        self.message = "[EmptyError] "+ message