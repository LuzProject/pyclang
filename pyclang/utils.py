# module imports
from shutil import which
from typing import Union


def cmd_in_path(cmd: str) -> Union[None, str]:
	'''Check if command is in PATH'''
	path = which(cmd)

	if path is None:
		return None

	return path
