from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from datetime import datetime, timedelta
from marshmallow import fields

@dataclass_json
@dataclass
class DataClassWithIsoDatetime:
    created_at: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format='iso')
        )
    )


just_now = DataClassWithIsoDatetime(datetime.now())
print(just_now)
print(just_now.to_dict())
print(just_now.to_json())

# end_date = datetime.now() - timedelta(days=10,hours=7)
# print(end_date)

from_date = DataClassWithIsoDatetime.from_dict({"created_at": "2022-06-25 16:41:33"})
print(from_date)
print(from_date.created_at)

from_date = DataClassWithIsoDatetime.from_json('{"created_at": "2022-06-05"}')
print(from_date)
print(from_date.created_at)

from_date = DataClassWithIsoDatetime.from_json('{"created_at": "2023-06-09T10:20:02.988968Z"}')
print(from_date)
print(from_date.created_at)


@dataclass_json
@dataclass
class DataClassWithIsoDatetime:
    created_at: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format='iso')
        )
    )


just_now = DataClassWithIsoDatetime(datetime.now())
print(just_now)
print(just_now.to_dict())
print(just_now.to_json())

# end_date = datetime.now() - timedelta(days=10,hours=7)
# print(end_date)

from_date = DataClassWithIsoDatetime.from_dict({"created_at": "2022-06-25 16:41:33"})
print(from_date)
print(from_date.created_at)

from_date = DataClassWithIsoDatetime.from_json('{"created_at": "2022-06-05"}')
print(from_date)
print(from_date.created_at)

from_date = DataClassWithIsoDatetime.from_json('{"created_at": "2023-06-09T10:20:02.988968Z"}')
print(from_date)
print(from_date.created_at)


@dataclass_json
@dataclass
class StrictlySpecifiedDataFormatDataclass:
    created_at: datetime = field(
        metadata=config(
            encoder=lambda date: date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            decoder=lambda date: datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ"),
        )
    )


just_now = StrictlySpecifiedDataFormatDataclass(datetime.now())
print(just_now)
print(just_now.to_dict())
print(just_now.to_json())

from_date = StrictlySpecifiedDataFormatDataclass.from_json('{"created_at": "2023-06-09T10:20:02.988968Z"}')
print(f"{from_date=}")
print(f"{from_date.created_at=}")
print(f"{from_date.to_dict()=}")
print(f"{from_date.to_json()=}")
