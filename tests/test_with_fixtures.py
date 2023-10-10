"""
Использование фикстур в тестах
"""
import logging

"""
1. Фикстуры не нужно явно импортировать, то есть "вносить" в область видимости модуля, где вы хотите их использовать. 
   Также, фикстуры не нужно вызывать явно, как стандартные функции. 
   Для того, чтобы фикстура была вызвана, нужно лишь указать ее имя в качестве аргумента теста 
   (здесь и далее "тест" = тестовая функция)
2. Когда pytest будет запущен и он найдет ваш тест, первым делом он проверит его аргументы. 
   Если один или более из аргументов теста это реально существующая фикстура 
   (объявленная в том же модуле, что и сам тест, или же, в conftest.py) - pytest сам вызовет эту фикстуру.
3. Фикстура вызывается ДО того, как начнет выполняться код внутри самого теста
"""


logger = logging.getLogger(__name__)


def test_with_one_fixture(my_fixture1):
    """
    my_fixture1 - фикстура из модуля conftest
    Мы ее не импортируем внутри данного модуля,
    однако, она существует в его области видимости
    """
    assert True


def test_with_fixtures_chain(fixture_chain2, fixture_no_chain):
    logger.debug("Hello from test 'test_with_fixtures_chain'!")

    # Здесь я умышленно делаю так, чтобы тест "падал" - иначе
    # вы не увидите в логах, как отрабатывают SETUP / TEARDOWN
    # используемых в тесте фикстур.
    assert False

    # После запуска теста внимательно посмотрите в логи - на порядок выполнения
    # SETUP / TEARDOWN.

    # Обратите внимание на то, что вызывают ли фикстуры друг друга, или же, фикстуры независимы
    # друг от друга и вызываются в рамках теста по порядку:
    # - выполнениe SETUP'ов фикстур будет происходить в порядке их вызова
    # - а вот порядок выполнения TEARDOWN'ов фикстур будет обратным!


def test_service(
    service,
):
    """
    Для проверки того, что SETUP-TEARDOWN для этого теста работают правильно,
    нужно запустить его несколько раз подряд следующим образом:

    pytest /{your_path_to_project_root}/tests_2/test_with_fixtures.py::test_service --count=10

    Если команда выше не работает:

    python -m pytest /{your_path_to_project_root}/tests_2/test_with_fixtures.py::test_service --count=10
    """
    # act
    assert service.is_cache_empty()

    service.set('key1', "value1")
    result = service.get('key1')

    # assert
    assert result == 'value1'