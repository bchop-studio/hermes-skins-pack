import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"


class ReadmeShellTests(unittest.TestCase):
    def test_all_documented_bash_blocks_parse(self):
        text = README.read_text(encoding="utf-8")
        blocks = re.findall(r"```bash\n(.*?)```", text, re.DOTALL)

        self.assertEqual(len(blocks), 45)
        for index, block in enumerate(blocks, start=1):
            result = subprocess.run(
                ["bash", "-n"],
                input=block,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(
                result.returncode,
                0,
                f"README bash block {index} failed syntax check: {result.stderr.strip()}",
            )


if __name__ == "__main__":
    unittest.main()
