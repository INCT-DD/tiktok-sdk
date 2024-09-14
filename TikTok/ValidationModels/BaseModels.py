"""
Defines base models for Pydantic that enforce strict validation rules
to ensure data integrity and consistency when interacting with APIs.

The `NoExtraFieldsBaseModel` class is designed to prevent the inclusion of extra fields
during model instantiation. This is crucial for avoiding issues where changes in the API
could lead to unknown or unexpected data being accepted by the models. By forbidding extra
fields, we ensure that only explicitly defined attributes are allowed, which helps maintain
the integrity of the data being processed and reduces the risk of errors due to unexpected
input.

The `HeadersModel` class extends `NoExtraFieldsBaseModel` and is specifically tailored for
HTTP headers. By setting `populate_by_name=True` and `by_alias=True`, we ensure that the
header names match the exact HTTP header names required by the API. This configuration allows for more
flexible handling of header names, ensuring that they are correctly mapped to the expected HTTP header names,
thus preventing potential issues when making requests.
"""

from pydantic import BaseModel, ConfigDict


class NoExtraFieldsBaseModel(BaseModel):
    """
    A base model that forbids extra fields during instantiation.

    This class extends Pydantic's BaseModel and configures it to raise
    validation errors when extra fields are provided during object creation.
    This helps ensure that only explicitly defined fields are allowed in
    model instances.

    Attributes:
        model_config (ConfigDict): Configuration dictionary for the model,
            set to forbid extra fields.

    Example:
        class User(NoExtraFieldsBaseModel):
            name: str
            age: int

        # This will work:
        user = User(name="Alice", age=30)

        # This will raise a validation error:
        # user = User(name="Bob", age=25, extra_field="Not allowed")
    """

    model_config: ConfigDict = ConfigDict(extra="forbid")


class HeadersModel(NoExtraFieldsBaseModel):
    """
    A model for headers that ensures only the specified fields are allowed.

    This class extends `NoExtraFieldsBaseModel` and configures it to allow
    population by field name. It is specifically designed for headers that
    must match the exact HTTP header names required by the API.
    """

    model_config: ConfigDict = ConfigDict(populate_by_name=True)
