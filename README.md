#Bad Events to Good Epochs

## Installation
From source

```bash
python3 -m build .
python3 -m pip install dist/betge-1.1.0-py3-none-any.whl
```

## Utilisation
```python
from betge import *

symmetry = "Neuroscans_OCD_metacognition/sub-044_task-symmetry.cnt"
epochs_sym = betge_symmetry(symmetry)

lucifer = "Neuroscans_OCD_metacognition/sub-042_task-lucifer.cnt"
epochs_luc = betge_lucifer(lucifer)
```
