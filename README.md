# Export and Visualize your Python Model with py-model

Generate class diagrams or code in another programming language from you Python classes. 

### Supported Graph Types
- .dot: DOT files
- .png: Images, generated from .dot-files with graphviz

### Supported Programming Languages
- .ts: TypeScript

# Usage
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Command Line Interface (CLI)](#command-line-interface-cli)
- [Supported Class Structures](#supported-class-structures)

## Quick Start
Let's assume your file `models.py` contains following code: 
```python
class Person:
    def __init__(name:str, age:int):
        self.name: str
        self.age: int

class Developer(Person):
    def __init__(name:str, age:int, languages: list[str]):
        super().__init__(name=name, age=age)
        self.languages: list[str] = languages

    def brag() -> str:
        return "Look at me, I know all these languages: " + ",".join(self.languages) + "."
```
Create the file you want with specifying the file extension:
```shell
python -m py-model --files models.py --output models.ts
```
this would then create following `models.ts` file:
```typescript
class Person {
 #TODO
}
```
or to generate a class diagram
```shell
python -m py-model --files models.py --output models.png
```
#TODO

## Installation
Install py-model with your common package manager. For `pip` this would look like
```shell
pip install py-model
```

## Command Line Interface (CLI)
To be filled in...

## Supported Class Structures
When parsing the structure of your python models regular classes and dataclasses are supported. However, if you also want to export your datatypes, then **only** annotated assignments will have a datatype, as an example
```python
ann_assign: int = 5
assign = 5 
```
will be parsed as something similar to `{ann_assign: int, assign: undefined}`:
```python
from dataclasses import dataclass

@dataclass
class Person:
    self.name: int # datatype will be picked up

class Company:
    def __init__(self, num_employees: int):
        self.num_employees = num_employees # datatype will NOT be picked up (not annotated)
```
It is important that only the specified datatypes in the assignments are used, not the ones specified in the constructor`s signature. This has the simple reason, that the variables in the constructor don't need to be the resulting attributes and it would be too complicated to check any conversions etc. Also, only attributes that are set within the constructor are considered to be instance attributes:
```python 
class Tree:
    def __init__(self, height: int)
        self.heigt = float(number) # datatype will NOT be picked up (not annotated)

    def cut_branches(cut_branches: int) -> None:
        self.cut_branches: int = cut_branches # attribute will NOT be picked up (not in constructor)
```

# Python Datatypes
Following data types are supported, with their equivalent in the other languages implemented:
- None
- bool
- int
- float
- str
- dict
- list
- tuple
- set 
- class

Also the union is supported (please rewrite `Optional[int]` to `int | None`). Any combination of supported datatypes does work, like
```python
some_attribute: list[tuple[str, bool | int]]
```

## Not supported
Not implemented yet, but planned and listed in their order of planned implementation:
- Enum
- complex
- frozenset
- range
- bytes
- bytearray


# Planned Features
> "Never. Ever. Buy a tech prouct based on the promise of future software updates - Marques Brownlee, around 2021

Lucky you, it's open source... 👀 These are the planned features for future versions.
## Graphs
### Cardinality
Additional cardsupport for class diagrams, where 
```python
from dataclasses import dataclass
from py_model.decorators import cardinality

class Wagon:
    pass

@dataclass
@cardinality(wagons=('1', '1..*'))
class Train:
    wagons: list[Wagon]
```
which would result in something like:
#TODO 

## Languages
- Nested Classes: parsing them correctly etc.

# Contribution
This is a fairly young project and any type of contribution is welcome. Just open a pull request and I am happy to check it. Please make sure to write some tests for it. The contribution for the following languages is highly appreciated (and wanted)...

## Graphs
- .puml (Plant UML)

## Languages
This is a list that came to my mind where I think implementation is useful, I am open to any other suggestions though and happy to merge a pull request for them. 
- .java (Java)
- .kt (Kotlin)
- .dart (Dart)
- .swift (Swift)

# License
To be filled in
