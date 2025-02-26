import yaml
from omegaconf import OmegaConf
import importlib.resources


class Config:
    _default_config = None
    _user_config = None
    _config = None  # Private class variable to store the configuration

    @classmethod
    def load_default_config(cls) -> object:
        """
        Load configuration from a YAML file and store it in the class.
        """

        # Open the YAML resource file from the package using importlib.resources
        with importlib.resources.open_text("ddd_llm_app.config", 'default-config.yaml') as f:
            # Load the YAML file content with OmegaConf
            cls._default_config = OmegaConf.load(f)
        # cls._default_config = OmegaConf.load(file_path)
        cls._config = cls._default_config


    @classmethod
    def load_user_config(cls, file_path: str):
        """
        Load configuration from a YAML file and store it in the class.
        """
        cls._user_config = OmegaConf.load(file_path)
        cls._config = OmegaConf.merge(cls._default_config, cls._user_config)

    @classmethod
    @property
    def config(cls):
        """
        Getter for the configuration object. Ensures it is loaded before access.
        """
        if cls._config is None:
            raise ValueError("Configuration not loaded. Call load_config() first.")
        return cls._config



