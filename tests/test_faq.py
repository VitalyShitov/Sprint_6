import pytest

from faq_data import FAQ_DATA


@pytest.mark.parametrize("index,question,expected_answer", [(i, q, a) for i, (q, a) in enumerate(FAQ_DATA)])
def test_faq_question_opens_answer(faq_page, index, question, expected_answer):
    # Прокручиваем до секции FAQ
    faq_page.scroll_to_faq_section()

    # Кликаем на вопрос и проверяем, что он раскрылся
    faq_page.click_question(index)
    actual = faq_page.get_answer_text(index)
    assert actual != "", f"Вопрос №{index} («{question}») не раскрылся после клика"

    # Проверяем текст ответа
    assert actual == expected_answer, (
        f"Вопрос №{index} («{question}»): текст ответа не совпадает с ожидаемым.\n"
        f"Ожидалось: {expected_answer!r}\n"
        f"Фактически: {actual!r}"
    )
