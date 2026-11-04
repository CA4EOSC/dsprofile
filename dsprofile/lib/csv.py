import csv
import pathlib
import sys

from dsprofile.lib.reader import Reader


class CSVReader(Reader):
	format = "csv"

	def __init__(self, filename):
		super().__init__()
		self.filename = filename
		self.dataset = self.read_dataset(filename)

	@staticmethod
	def read_dataset(filename):
		try:
			with open(filename, newline="", encoding="utf-8") as handle:
				reader = csv.DictReader(handle)
				return list(reader)
		except (OSError, PermissionError, FileNotFoundError) as e:
			print(f"Unable to read dataset '{filename}': {e}", file=sys.stderr)
			sys.exit(1)

	@classmethod
	def build_subparser(cls, sp):
		parser = sp.add_parser(cls.format, help="Extracts metadata from CSV files")
		parser.add_argument("filename", type=pathlib.Path)
		return parser

	@classmethod
	def handle_args(cls, args):
		if args.filename.is_dir():
			print(f"A valid file is required not directory '{args.filename}'", file=sys.stderr)
			sys.exit(1)
		return [args.filename], {}

	def process(self):
		return {
			"dataset": str(self.dataset)
		}
