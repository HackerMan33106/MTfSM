from core.config import load_config, load_translations

# Load configuration and translations on module import
config = load_config()
texts = load_translations(config["lang"])
