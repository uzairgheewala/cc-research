"""Import shims for third-party engines, shared by the audit scripts (AB-02, AB-03). Behaviour of the engines is unchanged.

torch_stub(): gCastle imports torch at package import for algorithms we never call (PC, GES, DirectLiNGAM, NOTEARS-linear,
TTPM/THP use numpy). This installs a meta-path finder that returns inert modules for torch*, so `import castle` works
without torch. Any code path that really uses torch fails loudly (calls return an inert object, not numbers that look
valid), which is why only numpy algorithms are run through it.
"""
import importlib.abc, importlib.machinery, sys, types


def torch_stub():
    if "torch" in sys.modules:
        return

    class _Any:
        def __call__(self, *a, **k):
            return a[0] if len(a) == 1 and callable(a[0]) else self

        def __getattr__(self, name):
            return self

        def __mro_entries__(self, bases):
            return (object,)

    class _Stub(types.ModuleType):
        def __getattr__(self, name):
            return object if name in ("Module", "Dataset") else _Any()

    class _TorchFinder(importlib.abc.MetaPathFinder, importlib.abc.Loader):
        def find_spec(self, name, path=None, target=None):
            if name == "torch" or name.startswith("torch."):
                return importlib.machinery.ModuleSpec(name, self, is_package=True)
            return None

        def create_module(self, spec):
            mod = _Stub(spec.name)
            mod.__path__ = []
            return mod

        def exec_module(self, module):
            pass

    sys.meta_path.insert(0, _TorchFinder())
