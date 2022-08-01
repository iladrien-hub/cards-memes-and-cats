# Start Game

Used to start game. Requires player to be room admin.

**URL** : `/api/v0/game/start`

**Method** : `POST`

**Auth required** : Yes

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

---

**Condition** : If user is not room admin.

**Code** : `403 FORBIDDEN`

**Content** :

```json
{
    "success": false,
    "data": {
        "type": "HttpError",
        "message": {
            "text": "not permitted"
        }
    }
}

```

---

**Condition** : If count of players is less than 2.

**Code** : `403 FORBIDDEN`

**Content** :

```json
{
    "success": false,
    "data": {
        "type": "HttpError",
        "message": {
            "text": "not enough players"
        }
    }
}
```