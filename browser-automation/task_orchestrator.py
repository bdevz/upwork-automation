import asyncio
import re
import uuid
from pathlib import Path
import logging
from typing import List, Dict, Any

from director import DirectorOrchestrator, WorkflowDefinition, WorkflowStep


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def parse_tasks_from_markdown(file_path: Path) -> List[Dict[str, Any]]:
    """
    Parses the tasks from a markdown file, skipping the first 6 tasks.
    """
    with open(file_path, 'r') as f:
        content = f.read()

    tasks = []
    # Regex to find tasks, assuming they start with '- [ ]' or '- [x]'
    task_pattern = re.compile(r'- \[( |x)\] (\d+)\. (.*?)(\n\s{2,4}- .*?)*', re.DOTALL)
    matches = task_pattern.finditer(content)

    for i, match in enumerate(matches):
        if i < 6:
            continue

        status = match.group(1).strip()
        task_number = int(match.group(2))
        title = match.group(3).strip()
        details = match.group(4) or ''
        
        if status != 'x':
            tasks.append({
                'task_number': task_number,
                'title': title,
                'description': details.strip(),
            })

    return tasks


async def main():
    """
    Main function to orchestrate the execution of tasks.
    """
    logging.info("Starting task orchestration.")
    tasks_file = Path('specifications/tasks.md')
    tasks = parse_tasks_from_markdown(tasks_file)
    
    if not tasks:
        logging.info("No new tasks to execute.")
        return


if __name__ == "__main__":
    asyncio.run(main())
