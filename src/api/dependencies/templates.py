from fastapi.templating import Jinja2Templates


class Templates():
	def __init__(self) -> None:
		self._templates = Jinja2Templates(directory="templates")

	def __call__(self) -> Jinja2Templates:
		return self._templates


templates = Templates()
