from pathlib import Path

from dagster_dbt import DbtProject


def get_project_root():
    current_path = Path(__file__).resolve()
    for parent in current_path.parents:
        if (parent / "dbt").exists():
            return parent
    return None


DBT_PROJECT_DIR = get_project_root() / "dbt" / "data_analytics"

dbt_project = DbtProject(
    project_dir=DBT_PROJECT_DIR,
)
