import joblib
from tqdm.auto import tqdm


class ProgressParallel(joblib.Parallel):

    # subclassing Parallel allows us to override the print_progress() method
    # see https://stackoverflow.com/questions/37804279/how-can-we-use-tqdm-in-a-parallel-execution-with-joblib/61027781#61027781

    def __init__(self, use_tqdm=True, total=None, *args, **kwargs):
        self._use_tqdm = use_tqdm
        self._total = total
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        with tqdm(disable=not self._use_tqdm, total=self._total) as self._pbar:
            return joblib.Parallel.__call__(self, *args, **kwargs)

    def print_progress(self):
        if self._total is None:
            self._pbar.total = self.n_dispatched_tasks
        self._pbar.n = self.n_completed_tasks
        self._pbar.refresh()


def process_parallel(iterable, func, n_jobs=10):
    return ProgressParallel(n_jobs=n_jobs, verbose=0, total=len(iterable))(
        joblib.delayed(func)(x) for x in iterable
    )
