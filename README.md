# Blinkist2Kindle
Convert and send Blinkist to Kindle or other devices.

## Usage
```
virtualenv venv
source env/bin/activate
pip install -r requirements.txt
# fill config.json
python main.py
```

### Configuration
See ```config_example.json``` for an example configuration.

The available formats are:

- Markdown: ```md```
- EPUB: ```epub```
- HTML (for Kindle): ```html```