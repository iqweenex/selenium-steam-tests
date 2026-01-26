import sys

print(f"PyCharm Python: {sys.executable}")
print(f"PyCharm version: {sys.version}")

try:
    import pytest

    print(f"✓ Pytest imported: {pytest.__version__}")
except ImportError as e:
    print(f"✗ Import error: {e}")

# Проверьте пути
print("\nSearch paths in PyCharm:")
for p in sys.path[:5]:  # первые 5 путей
    print(f"  {p}")