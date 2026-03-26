from abc import (
    ABC,
    abstractmethod
)

reader_type_map = {}


class Reader(ABC):
    """
      An abstract base for all Reader types, each subclass of this implements
      reader functionality for a particular dataset type.
      Each subclass must define the attribute referred to by
      <subclass_type_key> as a class attribute whose value indicates the
      type of dataset handled by that concrete type.
    """

    subclass_type_key = "format"

    def __init_subclass__(cls, /, **kwargs):
        """
          Derived types are validated to ensure they provide the attr
          identified by <subclass_type_key> and then added to the
          <reader_type_map> registry.
        """
        super().__init_subclass__(**kwargs)
        keyattr = __class__.subclass_type_key
        reader_type = getattr(cls, keyattr, None)
        if not reader_type or not isinstance(reader_type, str):
            raise NotImplementedError(f"Reader subclass {cls.__qualname__} "
                                      f"does not define a {keyattr} key")
        reader_type_map[reader_type] = cls

    @classmethod
    @abstractmethod
    def build_subparser(cls, sp):
        """
          Receives an argparse subparser argument <sp> and is responsible
          for adding all type-specific command line arguments.
        """
        pass

    @classmethod
    @abstractmethod
    def handle_args(cls, args) -> tuple[list, dict]:
        """
          Translates its argparse <args> argument into the positional
          and keyword arguments required to create an instance of this
          type.
          The returned tuple must consist of two elements:
            1. A list (or other sequence) of positional arguments
            2. A dict with str keys containing keyword arguments
          These are subsequently passed to the type's constructor
          to create an instance.
        """
        pass

    @abstractmethod
    def process(self) -> dict:
        """
          Processes the dataset and returns a type-specific dict containing
          the resulting metadata profile.
        """
        pass


def make_reader(args):
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
    cls = reader_type_map[args.command]
    ctor_args, ctor_kwargs = cls.handle_args(args)
    return cls(*ctor_args, **ctor_kwargs)
