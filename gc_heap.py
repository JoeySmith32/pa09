"""
PA 9: The Garbage Collector -- starter.

Complete GCHeap below. See the assignment, Part B,
for the full requirements.

Use gc_heap.py as specified in the assignment and imported by the harness.

Design note: GCHeap.allocate(obj) takes exactly one argument per the
spec, so an allocated object that references OTHER heap handles must
expose them itself for decref's cascade to find -- via a
get_child_handles() -> list[int] method. HeapNode below is a given
example object shaped this way, used by the cyclic-structure test.
"""

from typing import Any, Dict, List, Tuple


class HeapNode:
    """
    Given: a minimal heap object whose fields may hold OTHER handles
    (ints). get_child_handles() is what GCHeap.decref's cascade calls
    to find them -- it must reflect the CURRENT field values, not a
    snapshot taken at creation time.
    """

    def __init__(self, **fields: Any) -> None:
        self.fields = fields

    def get_child_handles(self) -> List[int]:
        return [v for v in self.fields.values() if isinstance(v, int)]


class GCHeap:
    def __init__(self) -> None:
        # handle -> (obj, refcount)
        self._table: Dict[int, Tuple[Any, int]] = {}
        self._next_handle: int = 1

    def allocate(self, obj: Any) -> int:
        """Store obj, return a new handle. Initial refcount is 1 (the creating reference)."""
        handle = self._next_handle
        self._next_handle += 1
        self._table[handle] = (obj, 1)
        return handle

    def incref(self, handle: int) -> None:
        if handle not in self._table:
            return
        obj, count = self._table[handle]
        self._table[handle] = (obj, count + 1)

    def decref(self, handle: int) -> None:
        """
        Decrement the refcount. When it hits 0: free the object, AND
        cascade-decref every handle returned by the freed object's
        get_child_handles() (if it has that method), recursively.
        """
        if handle not in self._table:
            return

        obj, count = self._table[handle]
        count -= 1
        if count > 0:
            self._table[handle] = (obj, count)
            return

        del self._table[handle]
        get_children = getattr(obj, "get_child_handles", None)
        if get_children is not None:
            for child_handle in get_children():
                self.decref(child_handle)

    def is_alive(self, handle: int) -> bool:
        return handle in self._table

    def live_count(self) -> int:
        """Number of currently-alive (refcount > 0) handles."""
        return len(self._table)
