from bson import ObjectId


def serialize_value(value):
    if isinstance(value, ObjectId):
        return str(value)
    if isinstance(value, dict):
        return {key: serialize_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [serialize_value(item) for item in value]
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return value


def serialize_document(document):
    serialized = serialize_value(document)
    if "_id" in serialized:
        serialized["id"] = serialized.pop("_id")
    return serialized


def serialize_documents(documents):
    return [serialize_document(document) for document in documents]
