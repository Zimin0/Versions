from pydantic import BaseModel

class __VersionMeta(type(BaseModel)):
    IMMUTABLE_ATTRIBUTES = {
        "REGEX",
        "EXAMPLE",
    }

    def __setattr__(self, name, value):
        if (name in self.IMMUTABLE_ATTRIBUTES) and (name in self.__dict__):
            raise AttributeError(f"__VersionMeta.{name!r} attribute is immutable.")
        
        return super().__setattr__(name, value)
