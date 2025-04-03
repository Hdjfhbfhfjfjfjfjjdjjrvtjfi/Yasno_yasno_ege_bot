__all__ = ["XLSXVisitor"]
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from typing import Any

from tg_bot.models import User, TestResult, TestResponse, KnowledgeAssesment, Excursion, Administrator
from tg_bot.utils.interfaces import IVisitor


class XLSXVisitor(IVisitor):
    def __init__(self):
        self._workbook: Workbook = Workbook()
        self._workbook.remove_sheet(self._workbook.active)

    async def visit_administrator(self) -> None:
        sheet: Worksheet = self._workbook.create_sheet(title="Администратор")
        annotations = ["ID администратора", "Может управлять администраторами"]
        objects = await Administrator.all().values_list("id", "can_manipulate_administrator_table")
        await self.export_data_to_xlsx_sheet(annotations, objects, sheet)

    async def visit_bot_user_profile(self) -> None:
        pass

    async def visit_excursion(self) -> None:
        sheet: Worksheet = self._workbook.create_sheet(title="Экскурсия")
        annotations = ["Адрес", "Дата"]
        objects = await Excursion.all()
        objects = tuple([(obj.address, obj.date) for obj in objects])
        await self.export_data_to_xlsx_sheet(annotations, objects, sheet)
        sheet = self._workbook.create_sheet(title="Купленные экскурсии")
        annotations = ["ID пользователя", "Дата экскурсии"]
        excursions = await Excursion.all()
        objects = []
        for excursion in excursions:
            users = [await profile.get_user() for profile in await excursion.bot_user_profiles.all()]
            for user in users:
                objects.append((user.id, excursion.date))
        objects = tuple(objects)
        await self.export_data_to_xlsx_sheet(annotations, objects, sheet)

    async def visit_knowledge_assesment(self) -> None:
        sheet: Worksheet = self._workbook.create_sheet(title="Проверка знаний")
        annotations = ["Ссылка", "Дата"]
        objects = await KnowledgeAssesment.all()
        objects = tuple([(obj.webinar_link, obj.date) for obj in objects])
        await self.export_data_to_xlsx_sheet(annotations, objects, sheet)
        sheet = self._workbook.create_sheet(title="Купленные проверки знаний")
        annotations = ["ID пользователя", "Дата проверки знаний"]
        assesments = await KnowledgeAssesment.all()
        objects = []
        for assesment in assesments:
            users = [await profile.get_user() for profile in await assesment.bot_user_profiles.all()]
            for user in users:
                objects.append((user.id, assesment.date))
        objects = tuple(objects)
        await self.export_data_to_xlsx_sheet(annotations, objects, sheet)

    async def visit_order(self) -> None:
        pass

    async def visit_school_grade(self) -> None:
        pass

    async def visit_test_answer(self) -> None:
        pass

    async def visit_test_question(self) -> None:
        pass

    async def visit_test_response(self) -> None:
        pass

    async def visit_test_result(self) -> None:
        sheet: Worksheet = self._workbook.create_sheet(title="Результаты тестирования")
        annotations = ["ID пользователя", "Класс"]
        test_results = await TestResult.all()
        users = [await (await obj.get_bot_user_profile()).get_user() for obj in test_results]
        objects: list[Any | None] = [None] * len(test_results)
        max_count_of_questions = -1
        for i in range(len(test_results)):
            objects[i] = [users[i].id, (await test_results[i].grade).grade]
            responses: list[TestResponse] = await test_results[i].test_responses.all()
            count_of_questions = 0
            for response in responses:
                count_of_questions += 1
                objects[i].append((await response.question).description)
                objects[i].append((await response.answer).description)
            max_count_of_questions = max(max_count_of_questions, count_of_questions)
        annotations += ["Вопрос", "Ответ"] * max_count_of_questions
        await self.export_data_to_xlsx_sheet(annotations, tuple(objects), sheet)

    async def visit_user(self) -> None:
        sheet = self._workbook.create_sheet(title="Пользователи")
        annotations = ["ID Пользователя", "ФИО", "Телефон"]
        objects = await User.all().values_list("id", "name_last_name_surname", "phone_number")
        await self.export_data_to_xlsx_sheet(annotations, objects, sheet)

    @property
    def workbook(self):
        return self._workbook

    @staticmethod
    async def export_data_to_xlsx_sheet(annotations: list[str], objects: tuple[tuple[Any, ...], ...], sheet: Worksheet):
        for i, annotation in enumerate(annotations):
            sheet[f"{chr(ord('A') + i)}1"] = annotation
        for i, obj in enumerate(objects, start=2):
            for j, field in enumerate(obj):
                sheet[f"{chr(ord('A') + j)}{i}"] = field