from benchopt.base import BaseSolver
from benchopt.util import safe_import


with safe_import() as solver_import:
    from cyanure import Regression


class Solver(BaseSolver):
    name = 'Cyanure'

    install_cmd = 'pip'
    requirements = ['cyanure-mkl']
    requirements_import = ['cyanure']

    def set_objective(self, X, y, lmbd):
        self.X, self.y, self.lmbd = X, y, lmbd

        n_samples = self.X.shape[0]

        self.solver = Regression(loss='square', penalty='l1',
                                 fit_intercept=False)
        self.solver_parameter = dict(
            lambd=self.lmbd / n_samples, solver='auto',
            tol=1e-12, verbose=False
        )

    def run(self, n_iter):
        self.solver.fit(self.X, self.y, max_epochs=n_iter,
                        **self.solver_parameter)

    def get_result(self):
        return self.solver.get_weights().flatten()
