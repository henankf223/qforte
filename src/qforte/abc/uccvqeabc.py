import qforte as qf
from abc import abstractmethod
from qforte.abc.vqeabc import VQE
from qforte.abc.ansatz import UCC
from qforte.utils.op_pools import *

from qforte.experiment import *
from qforte.utils.transforms import *
from qforte.utils.state_prep import ref_to_basis_idx
from qforte.utils.trotterization import trotterize

import numpy as np

class UCCVQE(VQE, UCC):

    @abstractmethod
    def get_num_ham_measurements(self):
        pass

    @abstractmethod
    def get_num_commut_measurements(self):
        pass

    def fill_commutator_pool(self):
        print('\n\n==> Building commutator pool for gradient measurement.')
        self._commutator_pool = self._pool_obj.get_quantum_op_pool()
        self._commutator_pool.join_as_commutator(self._qb_ham)
        print('==> Commutator pool construction complete.')

    def measure_operators(self, operators, Ucirc, idxs=[]):
        """
        Parameters
        ----------
        operators : QuantumOpPool
            All operators to be measured

        Ucirc : QuantumCircuit
            The state preparation circuit.

        idxs : list of int
            The indices of select operators in the pool of operators. If provided, only these
            operators will be measured.
        """

        if self._fast:
            myQC = qforte.QuantumComputer(self._nqb)
            myQC.apply_circuit(Ucirc)
            if not idxs:
                grads = myQC.direct_oppl_exp_val(operators)
            else:
                grads = myQC.direct_idxd_oppl_exp_val(operators, idxs)

        else:
            raise NotImplementedError("Must have self._fast to measure an operator.")

        np.testing.assert_allclose(np.imag(grads), np.zeros_like(grads), atol=1e-7)

        return np.real(grads)

    def measure_gradient(self, params=None, use_entire_pool=False):
        """
        Parameters
        ----------
        HAm : QuantumOpPool
            The commutator to measure.

        Ucirc : QuantumCircuit
            The state preparation circuit.
        """

        if not self._fast:
            raise ValueError("self._fast must be True for gradient measurement.")

        grads = np.zeros(len(self._tamps))

        if use_entire_pool:
            M = len(self._pool)
            pool_amps = np.zeros(M)
            for tamp, top in zip(self._tamps, self._tops):
                pool_amps[top] = tamp
        else:
            M = len(self._tamps)

        grads = np.zeros(M)

        if params is None:
            Utot = self.build_Uvqc()
        else:
            Utot = self.build_Uvqc(params)

        qc_psi = qforte.QuantumComputer(self._nqb) # build | sig_N > according ADAPT-VQE analytical grad section
        qc_psi.apply_circuit(Utot)
        qc_sig = qforte.QuantumComputer(self._nqb) # build | psi_N > according ADAPT-VQE analytical grad section
        psi_i = copy.deepcopy(qc_psi.get_coeff_vec())
        qc_sig.set_coeff_vec(copy.deepcopy(psi_i)) # not sure if copy is faster or reapplication of state
        qc_sig.apply_operator(self._qb_ham)

        mu = M-1

        # find <sing_N | K_N | psi_N>
        if use_entire_pool:
            Kmu_prev = self._pool[mu][1].jw_transform()
            Kmu_prev.mult_coeffs(self._pool[mu][0])
        else:
            Kmu_prev = self._pool[self._tops[mu]][1].jw_transform()
            Kmu_prev.mult_coeffs(self._pool[self._tops[mu]][0])

        qc_psi.apply_operator(Kmu_prev)
        grads[mu] = 2.0 * np.real(np.vdot(qc_sig.get_coeff_vec(), qc_psi.get_coeff_vec()))

        #reset Kmu_prev |psi_i> -> |psi_i>
        qc_psi.set_coeff_vec(copy.deepcopy(psi_i))

        for mu in reversed(range(M-1)):

            # mu => N-1 => M-2
            # mu+1 => N => M-1
            # Kmu => KN-1
            # Kmu_prev => KN

            if use_entire_pool:
                tamp = pool_amps[mu+1]
            elif params is None:
                tamp = self._tamps[mu+1]
            else:
                tamp = params[mu+1]

            if use_entire_pool:
                Kmu = self._pool[mu][1].jw_transform()
                Kmu.mult_coeffs(self._pool[mu][0])
            else:
                Kmu = self._pool[self._tops[mu]][1].jw_transform()
                Kmu.mult_coeffs(self._pool[self._tops[mu]][0])

            Umu, pmu = trotterize(Kmu_prev, factor=-tamp, trotter_number=self._trotter_number)

            if (pmu != 1.0 + 0.0j):
                raise ValueError("Encountered phase change, phase not equal to (1.0 + 0.0i)")

            qc_sig.apply_circuit(Umu)
            qc_psi.apply_circuit(Umu)
            psi_i = copy.deepcopy(qc_psi.get_coeff_vec())

            qc_psi.apply_operator(Kmu)
            grads[mu] = 2.0 * np.real(np.vdot(qc_sig.get_coeff_vec(), qc_psi.get_coeff_vec()))

            #reset Kmu |psi_i> -> |psi_i>
            qc_psi.set_coeff_vec(copy.deepcopy(psi_i))
            Kmu_prev = Kmu

        np.testing.assert_allclose(np.imag(grads), np.zeros_like(grads), atol=1e-7)

        return grads

    def measure_gradient3(self):

        if self._fast==False:
            raise ValueError("self._fast must be True for gradient measurement.")

        # Initialize amplitudes
        M = len(self._pool)
        pool_amps = np.zeros(M)
        for tamp, top in zip(self._tamps, self._tops):
            pool_amps[top] = tamp

        grads = np.zeros(M)
        Utot = self.build_Uvqc()

        qc_psi = qforte.QuantumComputer(self._nqb) # build | sig_N > according to ADAPT-VQE analytical grad section
        qc_psi.apply_circuit(Utot)
        psi_i = copy.deepcopy(qc_psi.get_coeff_vec())

        qc_sig = qforte.QuantumComputer(self._nqb) # build | psi_N > according to ADAPT-VQE analytical grad section
        # TODO: Check if it's faster to recompute psi_i or copy it.
        qc_sig.set_coeff_vec(copy.deepcopy(psi_i))
        qc_sig.apply_operator(self._qb_ham)

        mu = M-1

        for mu in range(M):
            Kmu = self._pool[mu][1].jw_transform()
            Kmu.mult_coeffs(self._pool[mu][0])
            qc_psi.apply_operator(Kmu)
            grads[mu] = 2.0 * np.real(np.vdot(qc_sig.get_coeff_vec(), qc_psi.get_coeff_vec()))
            qc_psi.set_coeff_vec(copy.deepcopy(psi_i))

        np.testing.assert_allclose(np.imag(grads), np.zeros_like(grads), atol=1e-7)

        return grads

    def gradient_ary_feval(self, params):
        grads = self.measure_gradient(params)

        if(self._noise_factor > 1e-14):
            grads = [np.random.normal(np.real(grad_m), self._noise_factor) for grad_m in grads]

        self._curr_grad_norm = np.linalg.norm(grads)
        self._grad_vec_evals += 1
        self._grad_m_evals += len(self._tamps)

        return np.asarray(grads)

    def report_iteration(self, x):

        self._k_counter += 1

        if(self._k_counter == 1):
            # print(f'     {self._k_counter:7}        {self._curr_energy:+12.10f}       -----------      {self._grad_vec_evals:4}         {self._curr_grad_norm:+12.10f}')
            print('\n    k iteration         Energy               dE           Ngvec ev      Ngm ev*         ||g||')
            print('--------------------------------------------------------------------------------------------------')
            if (self._print_summary_file):
                f = open("summary.dat", "w+", buffering=1)
                f.write('\n#    k iteration         Energy               dE           Ngvec ev      Ngm ev*         ||g||')
                f.write('\n#--------------------------------------------------------------------------------------------------')
                f.close()

        # else:
        dE = self._curr_energy - self._prev_energy
        print(f'     {self._k_counter:7}        {self._curr_energy:+12.10f}      {dE:+12.10f}      {self._grad_vec_evals:4}        {self._grad_m_evals:6}       {self._curr_grad_norm:+12.10f}')

        if (self._print_summary_file):
            f = open("summary.dat", "a", buffering=1)
            f.write(f'\n       {self._k_counter:7}        {self._curr_energy:+12.12f}      {dE:+12.12f}      {self._grad_vec_evals:4}        {self._grad_m_evals:6}       {self._curr_grad_norm:+12.12f}')
            f.close()

        self._prev_energy = self._curr_energy

    def verify_required_UCCVQE_attributes(self):
        if self._use_analytic_grad is None:
            raise NotImplementedError('Concrete UCCVQE class must define self._use_analytic_grad attribute.')

        if self._pool_type is None:
            raise NotImplementedError('Concrete UCCVQE class must define self._pool_type attribute.')

        if self._pool_obj is None:
            raise NotImplementedError('Concrete UCCVQE class must define self._pool_obj attribute.')
