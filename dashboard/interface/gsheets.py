from .base import TabularInterface


class SheetInterface(TabularInterface):
    BASE_URL = "https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"

    def __init__(self, sheet_id: str):
        self.sheet_id = sheet_id

    def poll(self):
        import urllib.request
        import openpyxl
        import io
        print(self.BASE_URL.format(sheet_id=self.sheet_id))
        with urllib.request.urlopen(self.BASE_URL.format(sheet_id=self.sheet_id)) as response:
            xmlx = response.read()
            with io.BytesIO(xmlx) as f:
                wb = openpyxl.load_workbook(f)
            print(wb.sheetnames)


def main():
    i = SheetInterface('1Q6JSzWr_XH5A3qYEss994y72btPhpFb3NW6782P9as4')
    i.poll()


if __name__ == "__main__":
    main()
