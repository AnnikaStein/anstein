import os
import subprocess
from datetime import datetime, timezone
from markdown import Extension
from markdown.preprocessors import Preprocessor
from markdown.postprocessors import Postprocessor


class GitDatesPreprocessor(Preprocessor):
    """Captures the current file path from the Markdown instance before parsing."""
    def __init__(self, md, postprocessor):
        super().__init__(md)
        self.postprocessor = postprocessor

    def run(self, lines):
        # MkDocs / Zensical attaches 'file' object or 'doc_path' to the md instance
        file_path = None
        if hasattr(self.md, "file") and hasattr(self.md.file, "abs_src_path"):
            file_path = self.md.file.abs_src_path
        elif hasattr(self.md, "doc_path") and self.md.doc_path:
            file_path = self.md.doc_path

        # Store the current file path on the postprocessor
        self.postprocessor.current_file_path = file_path
        return lines


class GitDatesPostprocessor(Postprocessor):
    """Replaces the placeholder using the captured file path."""
    def __init__(self, md, config):
        super().__init__(md)
        self.config = config
        self.current_file_path = None

    def run(self, text):
        placeholder = self.config["placeholder"]
        if placeholder not in text:
            return text

        file_path = self.current_file_path
        commit_date = self._get_last_updated_date(file_path)

        if commit_date:
            formatted_date = commit_date.strftime(self.config["date_format"])
        else:
            formatted_date = "Unknown"

        return text.replace(placeholder, formatted_date)

    def _get_last_updated_date(self, file_path):
        if not file_path or not os.path.exists(file_path):
            return None

        try:
            # Run git log on the exact file path
            cmd = [
                "git",
                "log",
                "-1",
                "--format=%ct",  # Commit timestamp
                "--",
                file_path,
            ]
            result = subprocess.run(
                cmd,
                cwd=os.path.dirname(file_path),
                capture_output=True,
                text=True,
                check=True,
            )
            timestamp_str = result.stdout.strip()

            if timestamp_str:
                tz = timezone.utc if self.config["use_utc"] else None
                return datetime.fromtimestamp(int(timestamp_str), tz=tz)
        except Exception:
            pass

        # Fallback to file mtime if git log returned nothing (e.g. untracked file)
        if self.config["fallback_to_mtime"]:
            try:
                mtime = os.path.getmtime(file_path)
                tz = timezone.utc if self.config["use_utc"] else None
                return datetime.fromtimestamp(mtime, tz=tz)
            except Exception:
                pass

        return None


class GitDatesExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
            "placeholder": ["{{ last_updated }}", "Placeholder string to replace"],
            "date_format": ["%Y-%m-%d", "strftime format string"],
            "fallback_to_mtime": [True, "Fallback to file mtime if untracked"],
            "use_utc": [True, "Use UTC timezone"],
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        postprocessor = GitDatesPostprocessor(md, self.getConfigs())
        preprocessor = GitDatesPreprocessor(md, postprocessor)

        # Register preprocessor to capture the path early
        md.preprocessors.register(preprocessor, "git_dates_prep", priority=100)
        # Register postprocessor to perform the string replacement
        md.postprocessors.register(postprocessor, "git_dates_post", priority=10)


def makeExtension(**kwargs):
    return GitDatesExtension(**kwargs)
