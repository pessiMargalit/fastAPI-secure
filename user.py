from datetime import datetime

from pydantic import BaseModel, field_validator, constr, Field, EmailStr, computed_field

fakeDB = {
    "johndoe": {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "city":"Jerusalem",
        "street":"Rabi Akiva",
        "number_in_family":5,
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
        "created_time": "13:45:00",
        "birthday": "19/07/1983"
    }
}


class BaseUser(BaseModel):
    username: constr(min_length=3)
    email: EmailStr
    disabled: bool
    created_time: datetime = Field(default_factory=datetime.now)
    birthday: str  # datetime  # = DateTimeStr(formats=["%d/%m/%Y", "%d-%m-%Y"])
    is_admin: bool = False

    @field_validator("birthday")
    def convert_birthday_to_date(cls, birthday):
        # todo
        formats = ["%d/%m/%Y", "%d-%m-%Y"]
        for fmt in formats:
            try:
                return datetime.strptime(birthday, fmt)
            except ValueError:
                pass
        raise ValueError("Invalid date format. Please provide a date in the format 'dd/mm/yyyy' or 'dd-mm-yyyy'")

    # @computed_field
    # @property
    # def age(self) -> int:
    #     return datetime.now().year - datetime(self.birthday).year


class RegistrationUser(BaseUser):
    password: constr(min_length=8)
    confirm_password: constr(min_length=8)

    @classmethod
    @field_validator("confirm_password")
    def compare_passwords(cls, confirm_password):
        if confirm_password == cls.password:
            return confirm_password
        raise ValueError("confirm password must be the equals to password")


class DBUser(BaseUser):
    hashed_password: str
