class InvalidWorkflowConfiguration(Exception):
    """
    Raised when workflow configuration is not provided to WorkflowEngine
    """
    
    
class UnknownWorkflowError(Exception):
    """
    Raised when an error occurs on bot/function execution
    """
    
class NodeNotFound(Exception):
    """
    Raised when unable to determine the next node
    """