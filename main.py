from model_viz.logging import get_logger
from model_viz.utils import set_project_name

logger = get_logger(__name__, level="INFO")

logger.info("Hello, world!")


project_name = "my-project"

set_project_name('model-viz')

logger.info(f"Project name is {project_name}")
