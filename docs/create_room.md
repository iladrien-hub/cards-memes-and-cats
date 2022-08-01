# Create Room

Used to create room with game session.

**URL** : `/api/v0/room/create`

**Method** : `POST`

**Auth required** : NO

**Data constraints** :

| parameter | type | required | default | example   |
|-----------|------|----------|---------|-----------|
| name      | str  | YES      | -       | test-room |

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "success": true,
    "data": {
        "room_id": 10001
    }
}
```

## Error Response

**Condition** : If any of required parameters was not provided.

**Code** : `400 BAD REQUEST`

**Content** :

```json
{
    "success": false,
    "data": {
        "type": "HttpError",
        "message": {
            "text": "missed required parameters",
            "params": [
                "name"
            ]
        }
    }
}
```