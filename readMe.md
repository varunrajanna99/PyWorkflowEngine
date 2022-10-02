# <strong> WorflowEngine </strong>

This is an attempt to write a simple configurable workflow execution which must be able to execute custom functions and standalone python scripts with inputs from previous and current nodes

## Setup

The Workflow engine uses only the native python packages, but it is a good practice to use virtualenv for development hence use the below commands to setup one

```shell
$ python3 -m virtaulenv venv
$ source venv/bin/activate
```

## How To's

<ul>

### <li> Writing a workflow </li>

You can refer the <strong> exampleWorflowEngine.json </strong> for a simple configuration

### <li> Engine Settings </li>

Any settings related to the Workflow engine can be added to setting.py, please refer the class EngineConfig

### <li> Executing the workflow engine </li>

For executing the workflow engine we just have to read the workflow config and call the WorkflowEngine object

```python
import json
    
with open("./exampleWorkflowConf.json", "r") as file:
    workflow = json.loads(file.read())

WorkflowEngine(workflow)()
```

</ul>