import re
from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator, EmailStr
from pydantic import Field


class SProductCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra='forbid')
    description_id: int = Field(..., description="Description id", example='1')
    name: str = Field(..., max_length=120, example='Vitamin C',
                      description="Product name")
    price: float = Field(..., description="Product price", example=10.0, min_value=0.0)
    product_type_id: int = Field(..., description="Product type id", example='1')
    photo: str | None = Field(None, description="Product photo")
    manufacturer_id: int = Field(..., description="Manufacturer id", example='1')
    analog_code: int | None = Field(None, description="Analog code")

    @classmethod
    @field_validator("photo", mode='before')
    def check_photo(cls, url: str):
        pattern = re.compile(r'^https?://.*\.(jpg|jpeg|png|gif)$', re.IGNORECASE)
        if not bool(pattern.match(url)):
            raise ValueError('Invalid photo url')
        return url

    @classmethod
    @field_validator("analog_code", mode='before')
    def check_analog_code(cls, code: int):
        pattern = re.compile(r'^\d{4}$')
        if not bool(pattern.match(str(code))):
            raise ValueError('Invalid analog code')
        return code


class SProductResult(SProductCreate):
    id: int = Field(..., description="Product id", example='1')


class SProductInfo(BaseModel):
    id: int = Field(description="Product id", example='1')
    description: str = Field(description="Description", example='1')
    name: str = Field(max_length=120, example='Vitamin C',
                      description="Product name")
    price: float = Field(description="Product price", example=10.0)
    product_type: str = Field(description="Product type", example='1')
    photo: str | None = Field(None, description="Product photo")
    manufacturer: str = Field(description="Manufacturer", example='1')
    analog_code: int | None = Field(None, description="Analog code")


class SPurchaseInfo(BaseModel):
    order_id: int = Field(..., description="ID заказа", example=1)
    order_date: str = Field(..., description="Дата заказа", example="2023-12-31T23:59:59")
    product_name: str = Field(..., description="Название продукта", example="Vitamin C")
    product_quantity: int = Field(..., description="Количество продукта", example=2)
    street: str = Field(..., description="Улица аптеки", example="Main Street")
    building: int = Field(..., description="Здание аптеки", example=10)
    client_name: str = Field(..., description="Имя клиента", example="John Doe")
    manufacturer_name: str = Field(..., description="Название производителя", example="Pharma Inc.")
    product_type: str = Field(..., description="Тип продукта", example="Medicine")


class SStockInfo(BaseModel):
    id: int = Field(..., description="ID продукта", example=1)
    product_name: str = Field(..., description="Название продукта", example="Vitamin C")
    product_type: str = Field(..., description="Тип продукта", example="Medicine")
    in_stock: int | None = Field(..., description="Количество продукта", example=2)
    price: float | None = Field(..., description="Цена продукта", example=10.0)
    pharmacy_id: int | None = Field(..., description="ID аптеки", example=1)
    pharmacy_street: str | None = Field(..., description="Улица аптеки", example="Main Street")
    pharmacy_building: int | None = Field(..., description="Здание аптеки", example=10)
    manufacturer_name: str = Field(..., description="Название производителя", example="Pharma Inc.")
    manufacturer_country: str = Field(..., description="Страна производителя", example="USA")


class SProductType(BaseModel):
    id: int = Field(..., description="Product type id", example='1')
    name: str = Field(..., max_length=120, example='Medicine',
                      description="Product type name")


class SStatistics(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra='forbid')
    first_name: str = Field(..., description="First name", example="John")
    last_name: str = Field(..., description="Last name", example="Doe")
    email: EmailStr = Field(..., description="Email", example="example@example.com")
    product_name: str = Field(..., description="Product name", example="Vitamin C")
    purchase_count: int = Field(..., description="Purchase count", example=5)


class SPriceFilter(BaseModel):
    min_price: float | None = Field(None, description="Price from", example=10.0)
    max_price: float | None = Field(None, description="Price to", example=100.0)
