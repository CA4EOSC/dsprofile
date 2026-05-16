from abc import (
    ABC,
    abstractmethod
)

writer_type_map = {}


class Writer(ABC):
    subclass_type_key = "format"

    def __init_subclass__(cls, /, **kwargs):
        """
          Derived types are validated to ensure they provide the attr
          identified by <subclass_type_key> and then added to the
          <write_type_map> registry.
        """
        super().__init_subclass__(**kwargs)
        keyattr = __class__.subclass_type_key
        writer_type = getattr(cls, keyattr, None)
        if not writer_type or not isinstance(writer_type, str) or ' ' in writer_type:
            raise NotImplementedError(f"Writer subclass {cls.__qualname__} "
                                      f"does not define a valid {keyattr} key")
        writer_type_map[writer_type] = cls

    @abstractmethod
    def write(self):
        pass


def make_writer(args):
    """
      1. Receives an argparse <args> argument containing command-line
         arguments
      2. Identifies the subtype required using the <command> attr which
         must match an entry in the reader_type_map
      3. Translates the argparse arguments into the specific form required
         by the constructor for the type identified in (2) above
      4. Returns an instance of that type constructed using these
         arguments
    """
    cls = writer_type_map[args.command]
    ctor_args, ctor_kwargs = cls.handle_args(args)
    return cls(*ctor_args, **ctor_kwargs)
