import pytest
from airflow.models import DagBag

@pytest.fixture
def dag_bag():
    """Load all DAGs in the dags/ folder."""
    return DagBag(dag_folder="dags", include_examples=False)

def test_no_import_errors(dag_bag):
    """Ensure DAGs import correctly with no syntax/import errors."""
    assert len(dag_bag.import_errors) == 0, f"Import errors: {dag_bag.import_errors}"

def test_example_dag_loaded(dag_bag):
    """Check that example_dag is present."""
    assert "example_dag" in dag_bag.dags
    dag = dag_bag.get_dag("example_dag")
    assert dag is not None
    assert len(dag.tasks) == 2   # start and end
