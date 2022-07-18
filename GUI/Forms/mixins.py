# +====================================================================================================================+
# Pythonic
import typing
# +====================================================================================================================+


class FormBoxElementMixin:
    def __init__(self, is_harvestable=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if type(is_harvestable) is bool:
            self.harvestable = lambda value=is_harvestable: value
        else:
            raise TypeError()

    def harvest(self):
        raise NotImplemented()


class FormBoxHarvestableElementMixin(FormBoxElementMixin):
    def __init__(self, is_harvestable=True, *args, **kwargs):
        super().__init__(is_harvestable=is_harvestable, *args, **kwargs)


class FormBoxNonHarvestableElementMixin(FormBoxElementMixin):
    def __init__(self, is_harvestable=False, *args, **kwargs):
        super().__init__(is_harvestable=is_harvestable, *args, **kwargs)


class FormBoxMixin():
    def __init__(self, title: str, *args, **kwargs):
        self.elements_to_harvest = []
        self.elements_attributes = []
        super().__init__(*args, **kwargs)
        self.setTitle(title)

    def harvest(self):
        return {k: getattr(self, k).harvest() for k in self.elements_to_harvest}

    def set(self, **kwargs):
        """Set the element to the form, in accordance with the FormBoxMixin."""

        for attr_name, element in kwargs.items():
            element.setParent(self)  # parent the element to us
            setattr(self, attr_name, element)  # save the element as our attribute under the passed name
            self.elements_attributes.append(attr_name)  # register as form element
            if element.harvestable():  # if data will be collected from this element
                self.elements_to_harvest.append(attr_name)  # register the element as a harvestable

    def set_as_pairs(self, *kwargs):
        """Same as set(), but if we are creating the attribute names dynamically, we can't pass them as kwarg keys, so
        instead we pass in (key, value) tuples to this method."""

        for kwarg in kwargs:
            attr_name, element = kwarg
            element.setParent(self)  # parent the element to us
            setattr(self, attr_name, element)  # save the element as our attribute under the passed name
            self.elements_attributes.append(attr_name)  # register as form element
            if element.harvestable():  # if data will be collected from this element
                self.elements_to_harvest.append(attr_name)  # register the element as a harvestable


class FormMixin:

    def __init__(self, *args, **kwargs):
        self.boxes: typing.List[FormBoxMixin] = []
        super().__init__(*args, **kwargs)

    @property
    def elements_to_harvest(self):
        which = []
        for box in self.boxes:
            which += box.elements_to_harvest
        return which

    @property
    def elements_attributes(self):
        attributes = []
        for box in self.boxes:
            attributes += box.elements_attributes
        return attributes

    def __getattr__(self, item):
        for box in self.form_boxes:
            if item in box.attributes:
                return getattr(box, item)

    def harvest(self):
        return {k: getattr(self, k).harvest() for k in self.to_harvest}
