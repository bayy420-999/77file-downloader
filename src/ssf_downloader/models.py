import pydantic
from enum import Enum

class Keys(Enum):
    DELETE_KEY = 'dnqwg13g8q1p13'
    WAKE_KEY = 'linkcwqf12f1v31'

class UserInfo(pydantic.BaseModel):
    userid: int
    username: str
    email: str
    vip_end_time: int
    text: str
    status: int
    s: int

class FileDetails(pydantic.BaseModel):
    status: bool
    link: str
    file_name: str
    file_time: int
    file_size: int
    needtest: int