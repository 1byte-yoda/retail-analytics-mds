from ..data_analytics.definitions import defs


def test_defs_can_load():
    assert defs.get_job_def("indebted_ae_exam_job")
    assert defs.get_all_job_defs()
