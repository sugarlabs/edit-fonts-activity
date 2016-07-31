import weakref
from defcon.objects.base import BaseDictObject


class Kerning(BaseDictObject):
    """
    This object contains all of the kerning pairs in a font.

    **This object posts the following notifications:**

    ===================
    Name
    ===================
    Kerning.Changed
    Kerning.BeginUndo
    Kerning.EndUndo
    Kerning.BeginRedo
    Kerning.EndRedo
    Kerning.PairSet
    Kerning.PairDeleted
    Kerning.Cleared
    Kerning.Updated
    ====================

    This object behaves like a dict. For example, to get a list of all kerning pairs::

        pairs = kerning.keys()

    To get all pairs including the values::

        for (left, right), value in kerning.items():

    To get the value for a particular pair::

        value = kerning["a", "b"]

    To set the value for a particular pair::

        kerning["a", "b"] = 100

    And so on.

    **Note:** This object is not very smart in the way it handles zero values,
    exceptions, etc. This may change in the future.
    """

    changeNotificationName = "Kerning.Changed"
    beginUndoNotificationName = "Kerning.BeginUndo"
    endUndoNotificationName = "Kerning.EndUndo"
    beginRedoNotificationName = "Kerning.BeginRedo"
    endRedoNotificationName = "Kerning.EndRedo"
    setItemNotificationName = "Kerning.PairSet"
    deleteItemNotificationName = "Kerning.PairDeleted"
    clearNotificationName = "Kerning.Cleared"
    updateNotificationName = "Kerning.Updated"
    representationFactories = {}

    def __init__(self, font=None):
        self._font = None
        if font is not None:
            self._font = weakref.ref(font)
        super(Kerning, self).__init__()
        self.beginSelfNotificationObservation()

    # --------------
    # Parent Objects
    # --------------

    def getParent(self):
        return self.font

    def _get_font(self):
        if self._font is not None:
            return self._font()
        return None

    font = property(_get_font,
                    doc="The :class:`Font` that this object belongs to.")

    # -------------
    # Pair Handling
    # -------------

    def get(self, pair, default=0):
        return super(Kerning, self).get(pair, default)

    # ------------------------
    # Notification Observation
    # ------------------------

    def endSelfNotificationObservation(self):
        super(Kerning, self).endSelfNotificationObservation()
        self._font = None


def _test():
    """
    >>> from defcon.test.testTools import getTestFontPath
    >>> from defcon.objects.font import Font

    # keys
    >>> font = Font(getTestFontPath())
    >>> keys = font.kerning.keys()
    >>> keys.sort()
    >>> keys
    [('A', 'A'), ('A', 'B')]

    # items
    >>> font = Font(getTestFontPath())
    >>> items = font.kerning.items()
    >>> items.sort()
    >>> items
    [(('A', 'A'), -100), (('A', 'B'), 100)]

    # values
    >>> font = Font(getTestFontPath())
    >>> values = font.kerning.values()
    >>> values.sort()
    >>> values
    [-100, 100]

    # __contains__
    >>> font = Font(getTestFontPath())
    >>> ('A', 'B') in font.kerning
    True
    >>> ('NotInFont', 'NotInFont') in font.kerning
    False

    # get
    >>> font = Font(getTestFontPath())
    >>> font.kerning.get(('A', 'A'))
    -100
    >>> font.kerning.get(('NotInFont', 'NotInFont'), 0)
    0

    # __getitem__
    >>> font = Font(getTestFontPath())
    >>> font.kerning['A', 'A']
    -100
    >>> font.kerning['NotInFont', 'NotInFont']
    Traceback (most recent call last):
        ...
    KeyError: ('NotInFont', 'NotInFont')

    # __setitem__
    >>> font = Font(getTestFontPath())
    >>> font.kerning['NotInFont', 'NotInFont'] = 100
    >>> keys = font.kerning.keys()
    >>> keys.sort()
    >>> keys
    [('A', 'A'), ('A', 'B'), ('NotInFont', 'NotInFont')]
    >>> font.kerning.dirty
    True

    # clear
    >>> font = Font(getTestFontPath())
    >>> font.kerning.clear()
    >>> font.kerning.keys()
    []
    >>> font.kerning.dirty
    True

    # update
    >>> font = Font(getTestFontPath())
    >>> other = {('X', 'X'):500}
    >>> font.kerning.update(other)
    >>> keys = font.kerning.keys()
    >>> keys.sort()
    >>> keys
    [('A', 'A'), ('A', 'B'), ('X', 'X')]
    >>> font.kerning.dirty
    True
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod()
