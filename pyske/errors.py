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