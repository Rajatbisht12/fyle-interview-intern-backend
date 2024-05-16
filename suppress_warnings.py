import warnings

# Filter the warnings related to LooseVersion in marshmallow
warnings.filterwarnings(
    "ignore",
    message="distutils Version classes are deprecated. Use packaging.version instead.",
    category=DeprecationWarning,
    module="marshmallow.*"
)

# Filter the warnings related to LooseVersion in marshmallow-sqlalchemy
warnings.filterwarnings(
    "ignore",
    message="distutils Version classes are deprecated. Use packaging.version instead.",
    category=DeprecationWarning,
    module="marshmallow_sqlalchemy.*"
)