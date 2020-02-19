import multiprocessing
import pytest
import threading

from uuid import uuid4

import ns1.helpers

try:  # Python 3.3 +
    import queue
except ImportError:
    import Queue as queue


JOIN_TIMEOUT = 2


class A(ns1.helpers.SingletonMixin):
    def __init__(self):
        self.uuid = uuid4()


class B(ns1.helpers.SingletonMixin):
    def __init__(self):
        self.uuid = uuid4()


def test_singleton_mixin():
    """
    it should be the same instance per mixed-in class
    it should not be the same instance across subclassers
    """
    a, a2 = A(), A()
    b, b2 = B(), B()

    assert a is a2
    assert b is b2

    assert a is not b


@pytest.mark.parametrize(
    "queue_class,process,repetitions",
    [
        (multiprocessing.Queue, multiprocessing.Process, 64),
        (queue.Queue, threading.Thread, 64),
    ],
)
def test_singleton_mixin_with_concurrency(queue_class, process, repetitions):
    """
    it should hold up under multiple processes or threads
    """

    def inner(queue):
        a = A()
        b = A()
        queue.put((a.uuid, b.uuid))

    test_queue = queue_class()
    processes = []
    for _ in range(repetitions):
        p = process(target=inner, args=(test_queue,))
        p.start()
        processes.append(p)

    seen_uuids = set()
    while len(seen_uuids) < repetitions:
        a, b = test_queue.get(timeout=JOIN_TIMEOUT)
        assert a is b
        assert a not in seen_uuids
        seen_uuids.add(a)


@pytest.mark.parametrize(
    "headers, want",
    [
        ({}, None),
        (
            {
                "link": "<http://a.co/b.jpg>; rel=next; type='image/jpeg',"
                "<http://b.co/c.jpg>; rel=last;type='image/jpeg'"
            },
            "https://a.co/b.jpg",
        ),
        (
            {
                "Link": "<http://a.co/b.jpg>; rel=next; type='image/jpeg',"
                "<http://b.co/c.jpg>; rel=last;type='image/jpeg'"
            },
            "https://a.co/b.jpg",
        ),
        (
            {
                "Link": "<https://a.co/b.jpg>; rel=next; type='image/jpeg',"
                "<http://b.co/c.jpg>; rel=last;type='image/jpeg'"
            },
            "https://a.co/b.jpg",
        ),
        (
            {
                "link": "<http://a.co/b.jpg>; rel=front; type='image/jpeg',"
                "<http://b.co/c.jpg>; rel=back;type='image/jpeg'"
            },
            None,
        ),
    ],
)
def test_next_page(headers, want):
    """
    it should get the "next" link
    it should "https-ify" http links
    it is not case-sensitive when reading header dict
    """
    got = ns1.helpers.get_next_page(headers)
    assert got == want
