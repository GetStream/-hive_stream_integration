# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = moderation_from_dict(json.loads(json_string))

from typing import Optional, Any, List, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class ModerationElement:
    input: str
    moderation_class: Optional[str]
    score: Optional[int]
    is_moderated: bool
    moderated_word: Optional[str]
    reason: Optional[str]

    def __init__(self, input: str, moderation_class: Optional[str], score: Optional[int], is_moderated: bool, moderated_word: Optional[str], reason: Optional[str]) -> None:
        self.input = input
        self.moderation_class = moderation_class
        self.score = score
        self.is_moderated = is_moderated
        self.moderated_word = moderated_word
        self.reason = reason

    @staticmethod
    def from_dict(obj: Any) -> 'ModerationElement':
        assert isinstance(obj, dict)
        input = from_str(obj.get("input"))
        moderation_class = from_union([from_str, from_none], obj.get("class"))
        score = from_union([from_int, from_none], obj.get("score"))
        is_moderated = from_bool(obj.get("is_moderated"))
        moderated_word = from_union([from_str, from_none], obj.get("moderated_word"))
        reason = from_union([from_str, from_none], obj.get("reason"))
        return ModerationElement(input, moderation_class, score, is_moderated, moderated_word, reason)

    def to_dict(self) -> dict:
        result: dict = {}
        result["input"] = from_str(self.input)
        result["class"] = from_union([from_str, from_none], self.moderation_class)
        result["score"] = from_union([from_int, from_none], self.score)
        result["is_moderated"] = from_bool(self.is_moderated)
        result["moderated_word"] = from_union([from_str, from_none], self.moderated_word)
        result["reason"] = from_union([from_str, from_none], self.reason)
        return result


def moderation_from_dict(s: Any) -> List[ModerationElement]:
    return from_list(ModerationElement.from_dict, s)


def moderation_to_dict(x: List[ModerationElement]) -> Any:
    return from_list(lambda x: to_class(ModerationElement, x), x)
