from src.data.load_faq import load_faq_data, load_faq_as_documents


def test_load_faq_data():
    data = load_faq_data()

    assert isinstance(data, list)
    assert len(data) > 0


def test_faq_required_fields():
    data = load_faq_data()

    for item in data:
        assert "question" in item
        assert "answer" in item

        assert isinstance(item["question"], str)
        assert isinstance(item["answer"], str)


def test_load_faq_as_documents():
    documents = load_faq_as_documents()

    assert isinstance(documents, list)
    assert len(documents) > 0

    for document in documents:
        assert document.page_content
        assert isinstance(document.metadata, dict)