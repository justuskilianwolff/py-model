# py-model

This package aims at improved workflows with Python data models. The main functionality using your Python model is to
- generate class diagrams from it
- convert to other coding languages.

## Example
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
```
We could then either create a class diagram (look at supported formats below), like here:
TODO

or convert this to typescript:
```typescript
interface and so on
```

## Support
"Normal" Python and dataclasses are supported by this package. However, only attributes within the constructor will be considered. 
```python
from dataclasses import dataclass

@dataclass
class Tree:
    heigt: float # will be picked up as float

    def cut_branches(cut_branches: int) -> None:
        self.cut_branches: int = cut_branches # attribute will NOT be picked up since not in constructor

class Bush:
    def __init__(volume:int) -> None:
        self.volumne = volumne # datatype will NOT be picked up since no annotated assignment
```

### Datatypes
Following data types are supported, with their equivalent in other languages
- None
- bool
- int
- float
- str
- dict
- list
- tuple
-  set 
- class

Following conjunctions are supported:
- union: | (please rewrite `Optional[int]` to `int | None`)

#### Not supported

- Enum (planned)
- complex
- frozenset
- range
- bytes
- bytearray

## Upcoming
### Cardinality
Additional cardsupport for class diagrams, where 
```python
from dataclasses import dataclass
from py_model import cardinality

class Wagon:
    pass

@dataclass
@cardinality(wagons=('1', '1..*'))
class Train:
    wagons: list[Wagon]
```
which would result in following plot:
-todo- 

### Nested Classes

be able to also plot and work with nested classes

### Miscalleneous
