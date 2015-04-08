from zope.interface import (
    Interface,
    Attribute,
    )


class IElastic(Interface):
    """
    IElastic adapter.
    """

    __elastic_parent__ = Attribute("The elastic parent")

    def elastic_mapping():
        """
        Return an ES mapping.
        """

    def elastic_document():
        """
        Apply the class ES mapping to the current context
        """
