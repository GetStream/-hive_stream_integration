# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = hive_response_from_dict(json.loads(json_string))

from uuid import UUID
from datetime import datetime
from typing import Any, List, TypeVar, Callable, Type, cast
import dateutil.parser


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


class Input:
    hash: str
    inference_client_version: str
    model: str
    model_type: str
    model_version: int
    text: str
    id: UUID
    created_on: datetime
    user_id: int
    project_id: int
    charge: float

    def __init__(self, hash: str, inference_client_version: str, model: str, model_type: str, model_version: int, text: str, id: UUID, created_on: datetime, user_id: int, project_id: int, charge: float) -> None:
        self.hash = hash
        self.inference_client_version = inference_client_version
        self.model = model
        self.model_type = model_type
        self.model_version = model_version
        self.text = text
        self.id = id
        self.created_on = created_on
        self.user_id = user_id
        self.project_id = project_id
        self.charge = charge

    @staticmethod
    def from_dict(obj: Any) -> 'Input':
        assert isinstance(obj, dict)
        hash = from_str(obj.get("hash"))
        inference_client_version = from_str(obj.get("inference_client_version"))
        model = from_str(obj.get("model"))
        model_type = from_str(obj.get("model_type"))
        model_version = from_int(obj.get("model_version"))
        text = from_str(obj.get("text"))
        id = UUID(obj.get("id"))
        created_on = from_datetime(obj.get("created_on"))
        user_id = from_int(obj.get("user_id"))
        project_id = from_int(obj.get("project_id"))
        charge = from_float(obj.get("charge"))
        return Input(hash, inference_client_version, model, model_type, model_version, text, id, created_on, user_id, project_id, charge)

    def to_dict(self) -> dict:
        result: dict = {}
        result["hash"] = from_str(self.hash)
        result["inference_client_version"] = from_str(self.inference_client_version)
        result["model"] = from_str(self.model)
        result["model_type"] = from_str(self.model_type)
        result["model_version"] = from_int(self.model_version)
        result["text"] = from_str(self.text)
        result["id"] = str(self.id)
        result["created_on"] = self.created_on.isoformat()
        result["user_id"] = from_int(self.user_id)
        result["project_id"] = from_int(self.project_id)
        result["charge"] = to_float(self.charge)
        return result


class Class:
    class_class: str
    score: int

    def __init__(self, class_class: str, score: int) -> None:
        self.class_class = class_class
        self.score = score

    @staticmethod
    def from_dict(obj: Any) -> 'Class':
        assert isinstance(obj, dict)
        class_class = from_str(obj.get("class"))
        score = from_int(obj.get("score"))
        return Class(class_class, score)

    def to_dict(self) -> dict:
        result: dict = {}
        result["class"] = from_str(self.class_class)
        result["score"] = from_int(self.score)
        return result


class Output:
    time: int
    start_char_index: int
    end_char_index: int
    classes: List[Class]

    def __init__(self, time: int, start_char_index: int, end_char_index: int, classes: List[Class]) -> None:
        self.time = time
        self.start_char_index = start_char_index
        self.end_char_index = end_char_index
        self.classes = classes

    @staticmethod
    def from_dict(obj: Any) -> 'Output':
        assert isinstance(obj, dict)
        time = from_int(obj.get("time"))
        start_char_index = from_int(obj.get("start_char_index"))
        end_char_index = from_int(obj.get("end_char_index"))
        classes = from_list(Class.from_dict, obj.get("classes"))
        return Output(time, start_char_index, end_char_index, classes)

    def to_dict(self) -> dict:
        result: dict = {}
        result["time"] = from_int(self.time)
        result["start_char_index"] = from_int(self.start_char_index)
        result["end_char_index"] = from_int(self.end_char_index)
        result["classes"] = from_list(lambda x: to_class(Class, x), self.classes)
        return result


class TextFilter:
    value: str
    start_index: int
    end_index: int
    type: str

    def __init__(self, value: str, start_index: int, end_index: int, type: str) -> None:
        self.value = value
        self.start_index = start_index
        self.end_index = end_index
        self.type = type

    @staticmethod
    def from_dict(obj: Any) -> 'TextFilter':
        assert isinstance(obj, dict)
        value = from_str(obj.get("value"))
        start_index = from_int(obj.get("start_index"))
        end_index = from_int(obj.get("end_index"))
        type = from_str(obj.get("type"))
        return TextFilter(value, start_index, end_index, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["value"] = from_str(self.value)
        result["start_index"] = from_int(self.start_index)
        result["end_index"] = from_int(self.end_index)
        result["type"] = from_str(self.type)
        return result


class Response:
    input: Input
    custom_classes: List[Any]
    text_filters: List[TextFilter]
    pii_entities: List[Any]
    urls: List[Any]
    language: str
    moderated_classes: List[str]
    output: List[Output]

    def __init__(self, input: Input, custom_classes: List[Any], text_filters: List[TextFilter], pii_entities: List[Any], urls: List[Any], language: str, moderated_classes: List[str], output: List[Output]) -> None:
        self.input = input
        self.custom_classes = custom_classes
        self.text_filters = text_filters
        self.pii_entities = pii_entities
        self.urls = urls
        self.language = language
        self.moderated_classes = moderated_classes
        self.output = output

    @staticmethod
    def from_dict(obj: Any) -> 'Response':
        assert isinstance(obj, dict)
        input = Input.from_dict(obj.get("input"))
        custom_classes = from_list(lambda x: x, obj.get("custom_classes"))
        text_filters = from_list(TextFilter.from_dict, obj.get("text_filters"))
        pii_entities = from_list(lambda x: x, obj.get("pii_entities"))
        urls = from_list(lambda x: x, obj.get("urls"))
        language = from_str(obj.get("language"))
        moderated_classes = from_list(from_str, obj.get("moderated_classes"))
        output = from_list(Output.from_dict, obj.get("output"))
        return Response(input, custom_classes, text_filters, pii_entities, urls, language, moderated_classes, output)

    def to_dict(self) -> dict:
        result: dict = {}
        result["input"] = to_class(Input, self.input)
        result["custom_classes"] = from_list(lambda x: x, self.custom_classes)
        result["text_filters"] = from_list(lambda x: to_class(TextFilter, x), self.text_filters)
        result["pii_entities"] = from_list(lambda x: x, self.pii_entities)
        result["urls"] = from_list(lambda x: x, self.urls)
        result["language"] = from_str(self.language)
        result["moderated_classes"] = from_list(from_str, self.moderated_classes)
        result["output"] = from_list(lambda x: to_class(Output, x), self.output)
        return result


class StatusStatus:
    code: int
    message: str

    def __init__(self, code: int, message: str) -> None:
        self.code = code
        self.message = message

    @staticmethod
    def from_dict(obj: Any) -> 'StatusStatus':
        assert isinstance(obj, dict)
        code = int(from_str(obj.get("code")))
        message = from_str(obj.get("message"))
        return StatusStatus(code, message)

    def to_dict(self) -> dict:
        result: dict = {}
        result["code"] = from_str(str(self.code))
        result["message"] = from_str(self.message)
        return result


class StatusElement:
    status: StatusStatus
    response: Response

    def __init__(self, status: StatusStatus, response: Response) -> None:
        self.status = status
        self.response = response

    @staticmethod
    def from_dict(obj: Any) -> 'StatusElement':
        assert isinstance(obj, dict)
        status = StatusStatus.from_dict(obj.get("status"))
        response = Response.from_dict(obj.get("response"))
        return StatusElement(status, response)

    def to_dict(self) -> dict:
        result: dict = {}
        result["status"] = to_class(StatusStatus, self.status)
        result["response"] = to_class(Response, self.response)
        return result


class HiveResponse:
    id: UUID
    code: int
    project_id: int
    user_id: int
    created_on: datetime
    status: List[StatusElement]
    from_cache: bool

    def __init__(self, id: UUID, code: int, project_id: int, user_id: int, created_on: datetime, status: List[StatusElement], from_cache: bool) -> None:
        self.id = id
        self.code = code
        self.project_id = project_id
        self.user_id = user_id
        self.created_on = created_on
        self.status = status
        self.from_cache = from_cache

    @staticmethod
    def from_dict(obj: Any) -> 'HiveResponse':
        assert isinstance(obj, dict)
        id = UUID(obj.get("id"))
        code = from_int(obj.get("code"))
        project_id = from_int(obj.get("project_id"))
        user_id = from_int(obj.get("user_id"))
        created_on = from_datetime(obj.get("created_on"))
        status = from_list(StatusElement.from_dict, obj.get("status"))
        from_cache = from_bool(obj.get("from_cache"))
        return HiveResponse(id, code, project_id, user_id, created_on, status, from_cache)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = str(self.id)
        result["code"] = from_int(self.code)
        result["project_id"] = from_int(self.project_id)
        result["user_id"] = from_int(self.user_id)
        result["created_on"] = self.created_on.isoformat()
        result["status"] = from_list(lambda x: to_class(StatusElement, x), self.status)
        result["from_cache"] = from_bool(self.from_cache)
        return result


def hive_response_from_dict(s: Any) -> HiveResponse:
    return HiveResponse.from_dict(s)


def hive_response_to_dict(x: HiveResponse) -> Any:
    return to_class(HiveResponse, x)
