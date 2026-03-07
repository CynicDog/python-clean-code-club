from greet.api import Message


def test_static_greet():
    result = Message.greet("eunsang")

    assert result == "Hello, eunsang !"
    assert isinstance(result, str)


def test_message_instantiation():
    msg_content = "Deep dive into Polars"
    m = Message(msg_content)

    assert msg_content in repr(m)

    assert m._msg.inner_text == msg_content


def test_empty_string():
    result = Message.greet("")
    assert result == "Hello,  !"
