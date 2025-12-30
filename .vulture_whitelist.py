# Vulture whitelist for intentionally unused code
# Pydantic field validators use 'cls' as the first parameter (classmethod convention)
# but the parameter is often not used in the validator body

# Whitelisting the 'cls' variable name globally for validator methods
cls  # Used as first parameter in @classmethod validators per Python/Pydantic convention
