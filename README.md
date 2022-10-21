#Bad Events to Good Epochs

## Installation
Build from source

```bash
python3 -m build .
```

Install
(preferably inside a virtual environment such as venv, conda, etc..)

```bash
python3 -m pip install dist/betge-x.x.x-py3-none-any.whl
```

## Utilisation
```python
from betge.betge import *

symmetry = "Neuroscans_OCD_metacognition/sub-044_task-symmetry.cnt"
epochs_sym = betge_symmetry(symmetry)

lucifer = "Neuroscans_OCD_metacognition/sub-042_task-lucifer.cnt"
epochs_luc = betge_lucifer(lucifer)
```
