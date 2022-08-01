# Room List

Used to collect a list of existing rooms.

**URL** : `/api/v0/room/list`

**Method** : `GET`

**Auth required** : NO

**Data constraints** :

| parameter | type | required | default | example |
|-----------|------|----------|---------|---------|
| offset_id | int  | NO       | 0       | 10000   |

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "success": true,
    "data": [
        {
            "room_id": 10001,
            "name": "test2"
        }
    ]
}
```