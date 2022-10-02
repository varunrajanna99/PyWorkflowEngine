from settings import EngineConfig
from exceptions import *
from functions import *
import subprocess
import os

conf = EngineConfig()
bot_location = conf.bot_location
engine_logger = conf.engine_logger


class WorkflowEngine:
    
    def __init__(self, workflow = None):
        
        if not workflow:
            InvalidWorkflowConfiguration("Please provide a valid configuration")
        
        self.workflow = workflow
        self.workflow_name = self.workflow.get("name")
        self.workflow_nodes = self.workflow.get("nodes")
        
        engine_logger.info("Initiating worfklow engine with start node")
        self.current_node_name = "start"
        self.previous_node_name = "start"
        self.current_node = self.workflow_nodes.get("start")
        
        self.bot_input = None
        self.output_store = {}
        self.on_exception = None
        self.if_conditions = None
        self.else_conditions = None 
        
    def __call__(self):
        engine_logger.info(f"Starting worflow execution for {self.workflow_name}")

        while self.previous_node_name != "end":
            
            if not self.current_node:
                engine_logger.error(f"{self.previous_node_name} | Unable to determine the next node")
                raise NodeNotFound(f"{self.previous_node_name} | Unable to determine the next node")
            
            engine_logger.info(f"Proceeding from {self.previous_node_name} --> {self.current_node_name}")
            self.bot_input = self.current_node.get("bot_input")
            self.if_conditions = self.current_node.get("if", [])
            self.else_conditions = self.current_node.get("else", {})
            self.on_exception = self.current_node.get("on_exception")
            
            if self.current_node.get("function"):
                
                inputs = {}
                for param, init_value in self.current_node.get("input",{}).items():
                    inputs[param] = eval(init_value)
                
                try:
                    engine_logger.info(f"Executing function {self.current_node.get('function')} on {self.current_node_name}")
                    self.exec_function(
                        inputs, 
                        self.on_exception, 
                        self.if_conditions, 
                        self.else_conditions
                    )
                except Exception as e:
                    raise UnknownWorkflowError(e)
            
            elif self.current_node.get("bot"):
                try:
                    inputs = ""
                    if self.bot_input:
                        for arg, value in self.output_store[self.bot_input].items():
                            inputs += f"--{arg} {value} "
                    
                    engine_logger.info(f"Executing bot {self.current_node.get('bot')} on {self.current_node_name}")
                    self.exec_bot(
                        self.current_node.get("bot"),
                        inputs,
                        self.on_exception, 
                        self.if_conditions, 
                        self.else_conditions
                    )
                except Exception as e:
                    raise UnknownWorkflowError(e)
                
        

    def evaluate_conditions(self, if_cond, else_cond):
        for cond in if_cond:
            evaluation = eval(cond.get("condition", None))
            if evaluation:
                self.current_node_name = cond.get("call_node")
                self.current_node = self.workflow_nodes.get(self.current_node_name)
                return
        self.previous_node_name = self.current_node_name
        self.current_node_name = else_cond.get("call_node")
        self.current_node = self.workflow_nodes.get(self.current_node_name)
        
    def exec_function(self, inputs, on_exception, if_cond, else_cond):
        try:
            output = eval(f"{self.current_node.get('function')}(**inputs)")
            self.output_store[self.current_node_name] = output
            self.evaluate_conditions(if_cond, else_cond)
        except Exception as e:
            if not on_exception and (
                    on_exception is not self.current_node_name
                ):
                raise UnknownWorkflowError(e)
            self.previous_node_name = self.current_node_name
            self.current_node_name = on_exception
            self.current_node = self.workflow_nodes.get(on_exception)
            
    def exec_bot(self, bot, inputs, on_exception, if_cond, else_cond):
        try:
            output = subprocess.check_output([
                "python.exe", os.path.join(bot_location, bot)] + inputs.split(" "),
                stderr=subprocess.PIPE
            )
            self.output_store[self.current_node_name] = "success"
            self.output_store[f"stdout_{self.current_node_name}"] = output
            self.evaluate_conditions(if_cond, else_cond)
        except subprocess.CalledProcessError as e:
            if not on_exception and (
                    on_exception is not self.current_node_name
                ):
                raise UnknownWorkflowError(e.output)
            self.previous_node_name = self.current_node_name
            self.current_node_name = on_exception
            self.current_node = self.workflow_nodes.get(on_exception)


if __name__ == "__main__":
    import json
    
    with open("./exampleWorkflowConf.json", "r") as file:
        workflow = json.loads(file.read())
    
    WorkflowEngine(workflow)()