# Join Room

Used to join game session and retrieve access token.

**URL** : `/api/v0/room/join`

**Method** : `POST`

**Auth required** : NO

**Data constraints** :

| parameter | type | required | default | example        |
|-----------|------|----------|---------|----------------|
| username  | str  | YES      | -       | Stepan Bandera |
| room_id   | int  | YES      | -       | 10000          |

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "success": true,
    "data": {
        "token": "eyJwaWQiOjEsInJpZCI6MTAwMDJ9.e748501fc5d9abf4dcfc11bd81c83ee63b93f00d"
    }
}
```

## Error Responses

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
                "username",
                "room_id"
            ]
        }
    }
}
```

---

**Condition** : If room with such room_id does not exists.

**Code** : `404 NOT FOUND`

**Content** :

```json
{
    "success": false,
    "data": {
        "type": "HttpError",
        "message": {
            "text": "room not found"
        }
    }
}
```