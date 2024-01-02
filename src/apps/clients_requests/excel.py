import openpyxl
from openpyxl.writer.excel import save_virtual_workbook

from .choices import StatusClientsRequest


class ExportClientsRequest:

    def export_to_excel(self, data):
        """
        Export list of client`s request
        """

        status = dict(StatusClientsRequest.CHOICES)
        status[None] = ''

        workbook = openpyxl.Workbook(write_only=True)
        worksheet = workbook.create_sheet(title='Заявки')
        headers, fields_call = zip(
            ('ID', lambda item: item.id),
            ('Заголовок', lambda item: item.title),
            ('Контрагент', lambda item: item.client_name),
            ('ИНН', lambda item: item.inn),
            ('Телефон', lambda item: item.phone),
            ('E-mail', lambda item: item.email),
            ('Продукт', lambda item: item.product_name),
            ('Дата создания', lambda item: item.created_at.strftime("%d.%m.%Y %H:%M:%S")),
            ('Дата изменения', lambda item: item.updated_at.strftime("%d.%m.%Y %H:%M:%S")),
            ('Статус', lambda item: str(status.get(item.status))),
        )

        worksheet.append(headers)
        for row in data:    # type: ClientsRequest
            worksheet.append([f_call(row) for f_call in fields_call])

        wb_bytes = save_virtual_workbook(workbook)
        return wb_bytes
