import sys

import cachetools
import pytest
import logging

logging.basicConfig(
    format="%(asctime)s.%(msecs)03d %(levelname)s "
           "[%(name)s:%(funcName)s:%(lineno)s] -> %(message)s",
    datefmt="%Y-%m-%d,%H:%M:%S",
    level=logging.DEBUG,
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


"""
Концепция SETUP - TEARDOWN:

for each test case do the following:
1. make SETUP
    - SETUP is executed BEFORE EACH test
    - if SETUP FAILED: test should NOT be run
    - if SETUP PASSED: run tests_2
2. execute the TEST BODY
3. make TEARDOWN
    - TEARDOWN is executed AFTER EACH test
    - if TEARDOWN FAILED: test are FAILED too
"""

"""   
ФИКСТУРЫ (FIXTURES)

Визуально фикстуры выглядят как обычные питоновские функции, лишь обернутые декоратором pytest.fixture."""


@pytest.fixture
def my_fixture1():
    print("Hello!")
    yield


"""Однако, однако контекст и способы их использования в тестах отличаются от стандартных функций 
(cм. test_with_fixtures.py)"""


"""
ДЛЯ ЧЕГО НУЖНЫ ФИКСТУРЫ ?

Фикстуры позволяют реализовать концепцию setup - teardown в рамках одного блока кода (тело функции-фикстуры), 
без разделения на отдельные setup / teardown функции.

1. SETUP:
Код, который написан внутри фикстуры ДО return / yield - это SETUP, то есть то, что выполняется ДО начала самого теста.

Пример: В фикстуре 'my_fixture1', объявленной выше, SETUP - это вызов print("Hello!")

2. ВОЗВРАТ ЗНАЧЕНИЯ ИЗ ФИКСТУРЫ: 

Если фикстура содержит return или yield - то, что указано после return / yield (ссылка на объект или None), 
будет возвращено в точку вызова фикстуры, а далее, мы можем использовать ссылку на возвращенный Объект через ИМЯ ФИКСТУРЫ
внутри теста (или другой фикстуры):"""


def hello_fixture():
    yield "hello"  # just returns "hello" string


def caller_fixture(hello_fixture):
    """
    - На уровне аргументов фикстуры caller_fixture, hello_fixture - это ссылка на объект фикстуры hello_fixture,
    объявленной выше.
    - Внутри же тела фикстуры caller_fixture, hello_fixture - это ссылка на строку "hello",
    которую возвращает фикстура hello_fixture.
    """
    assert hello_fixture.startswith("he")


"""
TEARDOWN:
- если фикстура return'ит что-либо - значит у нее нет и не может быть никакого TEARDOWN, 
  так как после вызова return стэк-фрейм фикстуры (как у стандартной пайтон-функции) уничтожается"""


def fixture_with_no_teardown():
    print("Hello World")  # SETUP
    return 1  # value which the fixture returns into the caller's context
    # NO TEARDOWN


"""
- если же фикстура содержит yield, то в момент вызова yield ссылка на Объект (или None) будет возвращена 
в точку вызова фикстуры, сама же фикстура "уснет" и будет ждать завершения теста (или другой фикстуры) 
в рамках которого она используется. 
По завершении контекста вызова, фикстура "проснется", и далее, будет выполнен код внутри нее, который следует ЗА yield. 
Это и есть наш TEARDOWN!
"""


@pytest.fixture
def fixture_with_teardown():
    logger.debug("SETUP my_fixture1")  # SETUP
    yield 1  # value which the fixture returns into the caller's context
    logger.debug("TEARDOWN my_fixture1")  # TEARDOWN


"""
Фикстуры не могут принимать произвольные аргументы!
То есть, их нельзя параметризировать, потому что что фикстуры не вызываются явно в коде, 
а их вызывает сам pytest. Но фикстуры могут принимать в качестве аргументов имена других фикстур 
(как вы уже видели в примерах выше)
в этом случае, вызов фикстур будет происходить по цепочке - в порядке того, как pytest резолвит фикстуры в целом"""


@pytest.fixture
def fixture_chain1():
    logger.debug("SETUP fixture_chain1")   # SETUP
    yield
    logger.debug("TEARDOWN fixture_chain1")  # teardown


@pytest.fixture
def fixture_chain2(fixture_chain1):
    logger.debug("SETUP fixture_chain2")   # SETUP
    yield
    logger.debug("TEARDOWN fixture_chain2")  # TEARDOWN


@pytest.fixture
def fixture_no_chain():
    logger.debug("SETUP fixture_no_chain")   # SETUP
    yield
    logger.debug("TEARDOWN fixture_no_chain")  # TEARDOWN


"""
Как вызываются фикстуры выше: см. "test_with_fixtures.py::test_with_fixtures_chain"
"""


"""
"Перекрестный" вызов фикстур из друг друга запрещен, например,
 2 фикстуры ниже: если вы укажете одну из них в качестве аргумента
 в тесте, то получите ошибку!
"""


@pytest.fixture
def fixture_cross_call_1(fixture_cross_call_2):
    pass


@pytest.fixture
def fixture_cross_call_2(fixture_cross_call_1):
    pass


"""
Более реальный пример фикстуры с SETUP и TEARDOWN
"""


class MyService:
    CACHE = cachetools.TTLCache(maxsize=10, ttl=60*100)

    def get(self, key):
        return self.CACHE.get(key)

    def set(self, key, item):
        self.CACHE[key] = item

    def is_cache_empty(self):
        return self.CACHE.currsize == 0

    def clear_cache(self):
        self.CACHE.clear()


@pytest.fixture
def service():
    # SETUP
    logger.debug("SETUP MyService")
    service = MyService()
    assert service.is_cache_empty()
    # return the reference to MyService object created above
    yield service
    # TEARDOWN
    logger.debug("TEARDOWN my_fixture3")
    service.clear_cache()


"""
Использование фикстуры service: см. "test_with_fixtures.py::test_service"
"""