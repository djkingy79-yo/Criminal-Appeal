# app.py

class Document:
    def __init__(self, title, content):
        self.title = title
        self.content = content


class CaseManagementSystem:
    def __init__(self):
        self.documents = {
            "case_info": None,
            "briefs": [],
            "case_notes": [],
            "judgments": [],
            "sentencing_reports": [],
            "psychological_reports": []
        }

    def upload_case_info(self, title, content):
        self.documents["case_info"] = Document(title, content)

    def upload_brief(self, title, content):
        self.documents["briefs"].append(Document(title, content))

    def upload_case_notes(self, title, content):
        self.documents["case_notes"].append(Document(title, content))

    def upload_judgment(self, title, content):
        self.documents["judgments"].append(Document(title, content))

    def upload_sentencing_report(self, title, content):
        self.documents["sentencing_reports"].append(Document(title, content))

    def upload_psychological_report(self, title, content):
        self.documents["psychological_reports"].append(Document(title, content))

    def analyze_merit(self):
        # Perform an analysis of the grounds of merit based on documents
        # Placeholder for analysis logic
        return "Analysis of grounds of merit completed."


if __name__ == "__main__":
    cms = CaseManagementSystem()
    print("Criminal Appeal Document Management System")