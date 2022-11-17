#Bad Events to Good Epochs

BEtGE is a MNE based framework developed by two EPITA (Ecole Pour l'Informatique et les Techniques Avancées) students for our end of studies project.  
In collaboration with iCrin work on OCD through EEG analysis, BEtGE offers to parse events extracted from a file and eliminates any false positive for ulterior processing.  

Designed on iCrin experiments (called Lucifer - Symmetry - 7 Diffs and Toki), BEtGE is a simple tool making sure that no artefacts remain among the events previously recorded, and returns created epochs already preprocessed.

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

## Usage
```python
from betge.betge import *

symmetry = "Neuroscans_OCD_metacognition/sub-044_task-symmetry.cnt"
epochs_sym = betge_symmetry(symmetry)

lucifer = "Neuroscans_OCD_metacognition/sub-042_task-lucifer.cnt"
epochs_luc = betge_lucifer(lucifer)
```
