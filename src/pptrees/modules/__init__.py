from importlib import import_module
from pathlib import Path

for f in Path(__file__).parent.glob("*.py"):
    module_name = f.stem
    if (not module_name.startswith("_")) and (module_name not in globals()):
        import_module(f".{module_name}", __package__)
    del f, module_name
del import_module, Path

__all__ = ['modules']

imported = [globals()[x] for x in dir() if x[0]!='_']
modules = {}
for x in imported:
    modules[getattr(x,"name")] = getattr(x,"data")
