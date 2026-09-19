import hashlib
import os
import subprocess
from datetime import datetime, timezone
from markdown import Extension
from markdown.postprocessors import Postprocessor
from markdown.preprocessors import Preprocessor


class FileMatcherCache:
    """Caches file hashes for exact, instant mapping during zensical build."""
    _cache = {}

    @classmethod
    def get_file_for_content(cls, target_text, docs_dir="docs", placeholder="{{ last_updated }}"):
        if not cls._cache:
            cls._build_cache(docs_dir, placeholder)

        # Normalize content to handle line ending differences
        normalized_target = cls._normalize(target_text)
        target_hash = hashlib.md5(normalized_target.encode("utf-8")).hexdigest()

        if target_hash in cls._cache:
            return cls._cache[target_hash]

        # Substring / partial match fallback for pre-rendered snippets
        for file_hash, file_path in cls._cache.items():
            if file_path:
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        file_content = cls._normalize(f.read())
                        # If target_text is a subset/superset of the file
                        if normalized_target in file_content or file_content in normalized_target:
                            return file_path
                except Exception:
                    continue

        return None

    @classmethod
    def _build_cache(cls, docs_dir, placeholder):
        if not os.path.exists(docs_dir):
            docs_dir = "."

        for root, _, files in os.walk(docs_dir):
            for file in files:
                if file.endswith(".md"):
                    full_path = os.path.abspath(os.path.join(root, file))
                    try:
                        with open(full_path, "r", encoding="utf-8") as f:
                            content = f.read()

                        if placeholder in content:
                            normalized = cls._normalize(content)
                            content_hash = hashlib.md5(normalized.encode("utf-8")).hexdigest()
                            cls._cache[content_hash] = full_path
                    except Exception:
                        continue

    @staticmethod
    def _normalize(text):
        # Remove extra whitespace and standardize newlines
        return "\n".join(line.strip() for line in text.splitlines() if line.strip())


def _get_git_date(file_path, use_utc=True, fallback_to_mtime=True, date_type="author"):
    if file_path and os.path.exists(file_path):
        fmt = "%at" if date_type == "author" else "%ct"
        try:
            cmd = [
                "git",
                "log",
                "-1",
                f"--format={fmt}",
                "--",
                file_path,
            ]
            result = subprocess.run(
                cmd,
                cwd=os.path.dirname(file_path) or ".",
                capture_output=True,
                text=True,
                check=True,
            )
            timestamp_str = result.stdout.strip()

            if timestamp_str:
                tz = timezone.utc if use_utc else None
                return datetime.fromtimestamp(int(timestamp_str), tz=tz)
        except Exception:
            pass

        if fallback_to_mtime:
            try:
                mtime = os.path.getmtime(file_path)
                tz = timezone.utc if use_utc else None
                return datetime.fromtimestamp(mtime, tz=tz)
            except Exception:
                pass

    return None


class GitDatesPreprocessor(Preprocessor):
    def __init__(self, md, postprocessor):
        super().__init__(md)
        self.postprocessor = postprocessor

    def run(self, lines):
        raw_text = "\n".join(lines)
        self.postprocessor.last_raw_text = raw_text
        return lines


class GitDatesPostprocessor(Postprocessor):
    def __init__(self, md, config):
        super().__init__(md)
        self.config = config
        self.last_raw_text = ""

    def run(self, text):
        placeholder = self.config["placeholder"]
        if placeholder not in text:
            return text

        # Use the raw markdown preprocessor text to find exact matching source file
        raw_content = self.last_raw_text or text
        docs_dir = self.config.get("docs_dir") or "docs"

        file_path = FileMatcherCache.get_file_for_content(raw_content, docs_dir, placeholder)

        print(f"[DEBUG] Matched File: {file_path}")

        commit_date = _get_git_date(
            file_path,
            use_utc=self.config["use_utc"],
            fallback_to_mtime=self.config["fallback_to_mtime"],
            date_type=self.config["date_type"],
        )

        if commit_date:
            formatted_date = commit_date.strftime(self.config["date_format"])
        else:
            formatted_date = "Unknown"

        return text.replace(placeholder, formatted_date)


class GitDatesExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
            "placeholder": ["{{ last_updated }}", "Placeholder string"],
            "date_format": ["%Y-%m-%d", "strftime format string"],
            "fallback_to_mtime": [True, "Fallback to file mtime if untracked"],
            "use_utc": [True, "Use UTC timezone"],
            "date_type": ["author", "author (%at) or committer (%ct)"],
            "docs_dir": ["docs", "Directory containing markdown source files"],
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        postprocessor = GitDatesPostprocessor(md, self.getConfigs())
        preprocessor = GitDatesPreprocessor(md, postprocessor)

        md.preprocessors.register(preprocessor, "git_dates_prep", priority=100)
        md.postprocessors.register(postprocessor, "git_dates_post", priority=10)


def makeExtension(**kwargs):
    return GitDatesExtension(**kwargs)
