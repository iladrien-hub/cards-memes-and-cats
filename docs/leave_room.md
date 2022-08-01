# Join Room

Used to join leave game session.

**URL** : `/api/v0/room/leave`

**Method** : `POST`

**Auth required** : YES

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "success": true,
    "data": {}
}
```

## Error Responses

**Condition** : If token is invalid.

**Code** : `403 FORBIDDEN`

**Content** :

```json
{
    "success": false,
    "data": {
        "type": "HttpError",
        "message": {
            "text": "token invalid"
        }
    }
}
```