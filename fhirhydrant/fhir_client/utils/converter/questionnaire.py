from typing import Dict

from fhir.resources.questionnaireresponse import (
    QuestionnaireResponse,
    QuestionnaireResponseItemAnswer,
    QuestionnaireResponseItem
)

from ..converter.base import BaseFHIRConverter


class QuestionnaireAnswersConverter(BaseFHIRConverter):
    DEFAULT_STATUS = 'completed'

    TYPE_MAP = {
        int: 'valueInteger',
        float: 'valueDecimal',
        bool: 'valueBoolean',
        str: 'valueString'
    }

    DEFAULT_ANSWER_TYPE = (str, 'valueString')

    @classmethod
    def to_fhir(cls,
                responses: Dict,
                status: str = None) -> QuestionnaireResponse:
        response = QuestionnaireResponse()
        response.status = status or cls.DEFAULT_STATUS
        response.item = []

        for name, item in responses.items():
            response_item = cls.make_response(name, item)
            response.item.append(response_item)

        return response

    @classmethod
    def from_fhir(cls, resource: QuestionnaireResponse) -> Dict:
        result = dict()

        for response in resource.item:
            result.update(cls._extract_response_item(response))

        return result

    @classmethod
    def make_response(cls, name: str, response) -> QuestionnaireResponseItem:
        response_item = QuestionnaireResponseItem()
        response_item.text = name

        if not cls._is_group(response):
            answer = QuestionnaireResponseItemAnswer()
            val_type, fhir_type = cls._deduct_type(response)
            setattr(answer, fhir_type, val_type(response))
            response_item.answer = answer
        else:
            response_item.item = []
            for name, item in response.items():
                response_item.item.append(cls.make_response(name, item))

        return response_item

    @classmethod
    def _is_group(cls, candidate):
        return isinstance(candidate, dict)

    @classmethod
    def _deduct_type(cls, value):
        value_type = type(value)
        if value_type not in cls.TYPE_MAP:
            return cls.DEFAULT_ANSWER_TYPE

        return value_type, cls.TYPE_MAP.get(value_type)

    @classmethod
    def _extract_response_item(cls, response_item: QuestionnaireResponseItem) -> Dict:
        result = None

        if response_item.answer is not None:
            result = cls._extract_answer(response_item.answer)
        else:
            if result is None:
                result = dict()

            for item in response_item.item:
                result.update(cls._extract_response_item(item))

        return {response_item.text: result}

    @classmethod
    def _extract_answer(cls, answer: QuestionnaireResponseItemAnswer):
        for _, fhir_type in cls.TYPE_MAP.items():
            attr = getattr(answer, fhir_type)
            if attr is not None:
                return attr
        return answer.valueString
