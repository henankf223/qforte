import unittest
from qforte import qforte
from qforte.qkd.mrsqk import MRSQK
from qforte.qkd.srqk import SRQK
from qforte.system.molecular_info import Molecule

class QKDTests(unittest.TestCase):
    def test_H4_fast_qkd(self):
        print('\n')
        # The FCI energy for H4 at 1.5 Angstrom in a sto-6g basis
        E_fci = -2.0126741263939656

        # The He hamilitonian
        circ_vec = [
        qforte.QuantumCircuit(),
         qforte.build_circuit('Z_0'),
         qforte.build_circuit('Y_0 Z_1 Z_2 Z_3 Y_4'),
         qforte.build_circuit('X_0 Z_1 Z_2 Z_3 X_4'),
         qforte.build_circuit('Z_1'),
         qforte.build_circuit('Y_1 Z_2 Z_3 Z_4 Y_5'),
         qforte.build_circuit('X_1 Z_2 Z_3 Z_4 X_5'),
         qforte.build_circuit('Z_2'),
         qforte.build_circuit('Y_2 Z_3 Z_4 Z_5 Y_6'),
         qforte.build_circuit('X_2 Z_3 Z_4 Z_5 X_6'),
         qforte.build_circuit('Z_3'),
         qforte.build_circuit('Y_3 Z_4 Z_5 Z_6 Y_7'),
         qforte.build_circuit('X_3 Z_4 Z_5 Z_6 X_7'),
         qforte.build_circuit('Z_4'),
         qforte.build_circuit('Z_5'),
         qforte.build_circuit('Z_6'),
         qforte.build_circuit('Z_7'),
         qforte.build_circuit('Z_0 Z_1'),
         qforte.build_circuit('Y_0 Z_2 Z_3 Y_4'),
         qforte.build_circuit('X_0 Z_2 Z_3 X_4'),
         qforte.build_circuit('Y_0 X_1 X_2 Y_3'),
         qforte.build_circuit('X_0 X_1 Y_2 Y_3'),
         qforte.build_circuit('Y_0 Y_1 X_2 X_3'),
         qforte.build_circuit('X_0 Y_1 Y_2 X_3'),
         qforte.build_circuit('Y_0 X_1 X_3 Z_4 Z_5 Y_6'),
         qforte.build_circuit('X_0 X_1 X_3 Z_4 Z_5 X_6'),
         qforte.build_circuit('Y_0 Y_1 Y_3 Z_4 Z_5 Y_6'),
         qforte.build_circuit('X_0 Y_1 Y_3 Z_4 Z_5 X_6'),
         qforte.build_circuit('Z_0 Y_1 Z_2 Z_3 Z_4 Y_5'),
         qforte.build_circuit('Z_0 X_1 Z_2 Z_3 Z_4 X_5'),
         qforte.build_circuit('Y_0 X_1 X_4 Y_5'),
         qforte.build_circuit('X_0 X_1 Y_4 Y_5'),
         qforte.build_circuit('Y_0 Y_1 X_4 X_5'),
         qforte.build_circuit('X_0 Y_1 Y_4 X_5'),
         qforte.build_circuit('Y_0 X_1 X_2 Z_3 Z_4 Z_5 Z_6 Y_7'),
         qforte.build_circuit('X_0 X_1 Y_2 Z_3 Z_4 Z_5 Z_6 Y_7'),
         qforte.build_circuit('Y_0 Y_1 X_2 Z_3 Z_4 Z_5 Z_6 X_7'),
         qforte.build_circuit('X_0 Y_1 Y_2 Z_3 Z_4 Z_5 Z_6 X_7'),
         qforte.build_circuit('Y_0 X_1 X_6 Y_7'),
         qforte.build_circuit('X_0 X_1 Y_6 Y_7'),
         qforte.build_circuit('Y_0 Y_1 X_6 X_7'),
         qforte.build_circuit('X_0 Y_1 Y_6 X_7'),
         qforte.build_circuit('Z_0 Z_2'),
         qforte.build_circuit('Z_0 Y_2 Z_3 Z_4 Z_5 Y_6'),
         qforte.build_circuit('Z_0 X_2 Z_3 Z_4 Z_5 X_6'),
         qforte.build_circuit('Y_0 Z_1 Z_3 Y_4'),
         qforte.build_circuit('X_0 Z_1 Z_3 X_4'),
         qforte.build_circuit('Y_0 Z_1 X_2 X_4 Z_5 Y_6'),
         qforte.build_circuit('X_0 Z_1 X_2 X_4 Z_5 X_6'),
         qforte.build_circuit('X_0 Z_1 X_2 Y_4 Z_5 Y_6'),
         qforte.build_circuit('Y_0 Z_1 Y_2 X_4 Z_5 X_6'),
         qforte.build_circuit('Y_0 Z_1 Y_2 Y_4 Z_5 Y_6'),
         qforte.build_circuit('X_0 Z_1 Y_2 Y_4 Z_5 X_6'),
         qforte.build_circuit('Z_0 Z_3'),
         qforte.build_circuit('Y_0 Z_1 Z_2 Y_4'),
         qforte.build_circuit('X_0 Z_1 Z_2 X_4'),
         qforte.build_circuit('Y_0 Z_1 Y_2 Y_3 Z_4 Y_5'),
         qforte.build_circuit('X_0 Z_1 X_2 Y_3 Z_4 Y_5'),
         qforte.build_circuit('Y_0 Z_1 Y_2 X_3 Z_4 X_5'),
         qforte.build_circuit('X_0 Z_1 X_2 X_3 Z_4 X_5'),
         qforte.build_circuit('Y_0 Z_1 Z_2 X_3 X_5 Y_6'),
         qforte.build_circuit('X_0 Z_1 Z_2 X_3 X_5 X_6'),
         qforte.build_circuit('Y_0 Z_1 Z_2 Y_3 Y_5 Y_6'),
         qforte.build_circuit('X_0 Z_1 Z_2 Y_3 Y_5 X_6'),
         qforte.build_circuit('Z_0 Y_3 Z_4 Z_5 Z_6 Y_7'),
         qforte.build_circuit('Z_0 X_3 Z_4 Z_5 Z_6 X_7'),
         qforte.build_circuit('Y_0 Z_1 Z_2 X_3 X_4 Z_5 Z_6 Y_7'),
         qforte.build_circuit('X_0 Z_1 Z_2 X_3 Y_4 Z_5 Z_6 Y_7'),
         qforte.build_circuit('Y_0 Z_1 Z_2 Y_3 X_4 Z_5 Z_6 X_7'),
         qforte.build_circuit('X_0 Z_1 Z_2 Y_3 Y_4 Z_5 Z_6 X_7'),
         qforte.build_circuit('Z_0 Z_4'),
         qforte.build_circuit('Z_0 Z_5'),
         qforte.build_circuit('Y_0 Z_1 Z_2 Z_3 Y_4 Z_5'),
         qforte.build_circuit('X_0 Z_1 Z_2 Z_3 X_4 Z_5'),
         qforte.build_circuit('Y_0 Z_1 Y_2 Y_5 Z_6 Y_7'),
         qforte.build_circuit('X_0 Z_1 X_2 Y_5 Z_6 Y_7'),
         qforte.build_circuit('Y_0 Z_1 Y_2 X_5 Z_6 X_7'),
         qforte.build_circuit('X_0 Z_1 X_2 X_5 Z_6 X_7'),
         qforte.build_circuit('Y_0 Z_1 Z_2 Z_3 Z_4 X_5 X_6 Y_7'),
         qforte.build_circuit('X_0 Z_1 Z_2 Z_3 Z_4 X_5 Y_6 Y_7'),
         qforte.build_circuit('Y_0 Z_1 Z_2 Z_3 Z_4 Y_5 X_6 X_7'),
         qforte.build_circuit('X_0 Z_1 Z_2 Z_3 Z_4 Y_5 Y_6 X_7'),
         qforte.build_circuit('Z_0 Z_6'),
         qforte.build_circuit('Y_0 Z_1 Z_2 Z_3 Y_4 Z_6'),
         qforte.build_circuit('X_0 Z_1 Z_2 Z_3 X_4 Z_6'),
         qforte.build_circuit('Z_0 Z_7'),
         qforte.build_circuit('Y_0 Z_1 Z_2 Z_3 Y_4 Z_7'),
         qforte.build_circuit('X_0 Z_1 Z_2 Z_3 X_4 Z_7'),
         qforte.build_circuit('Z_1 Z_2'),
         qforte.build_circuit('Y_1 Z_3 Z_4 Y_5'),
         qforte.build_circuit('X_1 Z_3 Z_4 X_5'),
         qforte.build_circuit('Y_1 X_2 X_3 Y_4'),
         qforte.build_circuit('X_1 X_2 Y_3 Y_4'),
         qforte.build_circuit('Y_1 Y_2 X_3 X_4'),
         qforte.build_circuit('X_1 Y_2 Y_3 X_4'),
         qforte.build_circuit('Y_1 X_2 X_4 Z_5 Z_6 Y_7'),
         qforte.build_circuit('X_1 X_2 X_4 Z_5 Z_6 X_7'),
         qforte.build_circuit('Y_1 Y_2 Y_4 Z_5 Z_6 Y_7'),
         qforte.build_circuit('X_1 Y_2 Y_4 Z_5 Z_6 X_7'),
         qforte.build_circuit('Z_1 Y_2 Z_3 Z_4 Z_5 Y_6'),
         qforte.build_circuit('Z_1 X_2 Z_3 Z_4 Z_5 X_6'),
         qforte.build_circuit('Y_1 X_2 X_5 Y_6'),
         qforte.build_circuit('X_1 X_2 Y_5 Y_6'),
         qforte.build_circuit('Y_1 Y_2 X_5 X_6'),
         qforte.build_circuit('X_1 Y_2 Y_5 X_6'),
         qforte.build_circuit('Z_1 Z_3'),
         qforte.build_circuit('Z_1 Y_3 Z_4 Z_5 Z_6 Y_7'),
         qforte.build_circuit('Z_1 X_3 Z_4 Z_5 Z_6 X_7'),
         qforte.build_circuit('Y_1 Z_2 Z_4 Y_5'),
         qforte.build_circuit('X_1 Z_2 Z_4 X_5'),
         qforte.build_circuit('Y_1 Z_2 X_3 X_5 Z_6 Y_7'),
         qforte.build_circuit('X_1 Z_2 X_3 X_5 Z_6 X_7'),
         qforte.build_circuit('X_1 Z_2 X_3 Y_5 Z_6 Y_7'),
         qforte.build_circuit('Y_1 Z_2 Y_3 X_5 Z_6 X_7'),
         qforte.build_circuit('Y_1 Z_2 Y_3 Y_5 Z_6 Y_7'),
         qforte.build_circuit('X_1 Z_2 Y_3 Y_5 Z_6 X_7'),
         qforte.build_circuit('Z_1 Z_4'),
         qforte.build_circuit('Y_1 Z_2 Z_3 Y_5'),
         qforte.build_circuit('X_1 Z_2 Z_3 X_5'),
         qforte.build_circuit('Y_1 Z_2 Y_3 Y_4 Z_5 Y_6'),
         qforte.build_circuit('X_1 Z_2 X_3 Y_4 Z_5 Y_6'),
         qforte.build_circuit('Y_1 Z_2 Y_3 X_4 Z_5 X_6'),
         qforte.build_circuit('X_1 Z_2 X_3 X_4 Z_5 X_6'),
         qforte.build_circuit('Y_1 Z_2 Z_3 X_4 X_6 Y_7'),
         qforte.build_circuit('X_1 Z_2 Z_3 X_4 X_6 X_7'),
         qforte.build_circuit('Y_1 Z_2 Z_3 Y_4 Y_6 Y_7'),
         qforte.build_circuit('X_1 Z_2 Z_3 Y_4 Y_6 X_7'),
         qforte.build_circuit('Z_1 Z_5'),
         qforte.build_circuit('Z_1 Z_6'),
         qforte.build_circuit('Y_1 Z_2 Z_3 Z_4 Y_5 Z_6'),
         qforte.build_circuit('X_1 Z_2 Z_3 Z_4 X_5 Z_6'),
         qforte.build_circuit('Z_1 Z_7'),
         qforte.build_circuit('Y_1 Z_2 Z_3 Z_4 Y_5 Z_7'),
         qforte.build_circuit('X_1 Z_2 Z_3 Z_4 X_5 Z_7'),
         qforte.build_circuit('Z_2 Z_3'),
         qforte.build_circuit('Y_2 Z_4 Z_5 Y_6'),
         qforte.build_circuit('X_2 Z_4 Z_5 X_6'),
         qforte.build_circuit('Y_2 X_3 X_4 Y_5'),
         qforte.build_circuit('X_2 X_3 Y_4 Y_5'),
         qforte.build_circuit('Y_2 Y_3 X_4 X_5'),
         qforte.build_circuit('X_2 Y_3 Y_4 X_5'),
         qforte.build_circuit('Z_2 Y_3 Z_4 Z_5 Z_6 Y_7'),
         qforte.build_circuit('Z_2 X_3 Z_4 Z_5 Z_6 X_7'),
         qforte.build_circuit('Y_2 X_3 X_6 Y_7'),
         qforte.build_circuit('X_2 X_3 Y_6 Y_7'),
         qforte.build_circuit('Y_2 Y_3 X_6 X_7'),
         qforte.build_circuit('X_2 Y_3 Y_6 X_7'),
         qforte.build_circuit('Z_2 Z_4'),
         qforte.build_circuit('Y_2 Z_3 Z_5 Y_6'),
         qforte.build_circuit('X_2 Z_3 Z_5 X_6'),
         qforte.build_circuit('Z_2 Z_5'),
         qforte.build_circuit('Y_2 Z_3 Z_4 Y_6'),
         qforte.build_circuit('X_2 Z_3 Z_4 X_6'),
         qforte.build_circuit('Y_2 Z_3 Y_4 Y_5 Z_6 Y_7'),
         qforte.build_circuit('X_2 Z_3 X_4 Y_5 Z_6 Y_7'),
         qforte.build_circuit('Y_2 Z_3 Y_4 X_5 Z_6 X_7'),
         qforte.build_circuit('X_2 Z_3 X_4 X_5 Z_6 X_7'),
         qforte.build_circuit('Z_2 Z_6'),
         qforte.build_circuit('Z_2 Z_7'),
         qforte.build_circuit('Y_2 Z_3 Z_4 Z_5 Y_6 Z_7'),
         qforte.build_circuit('X_2 Z_3 Z_4 Z_5 X_6 Z_7'),
         qforte.build_circuit('Z_3 Z_4'),
         qforte.build_circuit('Y_3 Z_5 Z_6 Y_7'),
         qforte.build_circuit('X_3 Z_5 Z_6 X_7'),
         qforte.build_circuit('Y_3 X_4 X_5 Y_6'),
         qforte.build_circuit('X_3 X_4 Y_5 Y_6'),
         qforte.build_circuit('Y_3 Y_4 X_5 X_6'),
         qforte.build_circuit('X_3 Y_4 Y_5 X_6'),
         qforte.build_circuit('Z_3 Z_5'),
         qforte.build_circuit('Y_3 Z_4 Z_6 Y_7'),
         qforte.build_circuit('X_3 Z_4 Z_6 X_7'),
         qforte.build_circuit('Z_3 Z_6'),
         qforte.build_circuit('Y_3 Z_4 Z_5 Y_7'),
         qforte.build_circuit('X_3 Z_4 Z_5 X_7'),
         qforte.build_circuit('Z_3 Z_7'),
         qforte.build_circuit('Z_4 Z_5'),
         qforte.build_circuit('Y_4 X_5 X_6 Y_7'),
         qforte.build_circuit('X_4 X_5 Y_6 Y_7'),
         qforte.build_circuit('Y_4 Y_5 X_6 X_7'),
         qforte.build_circuit('X_4 Y_5 Y_6 X_7'),
         qforte.build_circuit('Z_4 Z_6'),
         qforte.build_circuit('Z_4 Z_7'),
         qforte.build_circuit('Z_5 Z_6'),
         qforte.build_circuit('Z_5 Z_7'),
         qforte.build_circuit('Z_6 Z_7')]

        coef_vec = [
        -0.9398866173443505,
        0.12129073807829349,
        0.00641125283150221,
        0.00641125283150221,
        0.12129073807829353,
        0.0064112528315022135,
        0.0064112528315022135,
        0.07308734612725618,
        -0.010595295586558178,
        -0.010595295586558178,
        0.0730873461272563,
        -0.010595295586558171,
        -0.010595295586558171,
        -0.004903180263267734,
        -0.0049031802632676785,
        -0.0972417632017775,
        -0.09724176320177753,
        0.10115751743776852,
        0.016853161923367253,
        0.016853161923367253,
        0.03977035285263866,
        -0.03977035285263866,
        -0.03977035285263866,
        0.03977035285263866,
        0.00905981792020611,
        0.00905981792020611,
        0.00905981792020611,
        0.00905981792020611,
        0.016853161923367253,
        0.016853161923367253,
        0.028827330860814942,
        -0.028827330860814942,
        -0.028827330860814942,
        0.028827330860814942,
        -0.00905981792020611,
        0.00905981792020611,
        0.00905981792020611,
        -0.00905981792020611,
        0.027456714140683562,
        -0.027456714140683562,
        -0.027456714140683562,
        0.027456714140683562,
        0.05019794254014193,
        0.008400644724214635,
        0.008400644724214635,
        0.01678679876377047,
        0.01678679876377047,
        0.008370670304957601,
        0.019986723846961468,
        0.011616053542003863,
        0.011616053542003863,
        0.019986723846961468,
        0.008370670304957601,
        0.08996829539278059,
        -0.00401664635059683,
        -0.00401664635059683,
        0.020803445114367297,
        0.020803445114367297,
        0.020803445114367297,
        0.020803445114367297,
        -0.020045295426307817,
        -0.020045295426307817,
        -0.020045295426307817,
        -0.020045295426307817,
        0.01746046264442075,
        0.01746046264442075,
        0.028415965731265418,
        -0.028415965731265418,
        -0.028415965731265418,
        0.028415965731265418,
        0.062364797002734416,
        0.09119212786354935,
        -0.0029292718691351837,
        -0.0029292718691351837,
        0.040032019273269284,
        0.040032019273269284,
        0.040032019273269284,
        0.040032019273269284,
        -0.008895760438436422,
        0.008895760438436422,
        0.008895760438436422,
        -0.008895760438436422,
        0.077813400984472,
        0.008622786573744252,
        0.008622786573744252,
        0.10527011512515555,
        0.017518547012180676,
        0.017518547012180676,
        0.08996829539278059,
        -0.00401664635059683,
        -0.00401664635059683,
        0.020803445114367297,
        -0.020803445114367297,
        -0.020803445114367297,
        0.020803445114367297,
        -0.020045295426307817,
        -0.020045295426307817,
        -0.020045295426307817,
        -0.020045295426307817,
        0.01746046264442075,
        0.01746046264442075,
        0.028415965731265418,
        -0.028415965731265418,
        -0.028415965731265418,
        0.028415965731265418,
        0.05019794254014193,
        0.008400644724214635,
        0.008400644724214635,
        0.01678679876377047,
        0.01678679876377047,
        0.008370670304957601,
        0.019986723846961468,
        0.011616053542003863,
        0.011616053542003863,
        0.019986723846961468,
        0.008370670304957601,
        0.09119212786354935,
        -0.0029292718691351837,
        -0.0029292718691351837,
        0.040032019273269284,
        0.040032019273269284,
        0.040032019273269284,
        0.040032019273269284,
        0.008895760438436422,
        0.008895760438436422,
        0.008895760438436422,
        0.008895760438436422,
        0.062364797002734416,
        0.10527011512515555,
        0.017518547012180676,
        0.017518547012180676,
        0.077813400984472,
        0.008622786573744252,
        0.008622786573744252,
        0.09416046345893181,
        -0.0025909758017290006,
        -0.0025909758017290006,
        0.035233425879700006,
        -0.035233425879700006,
        -0.035233425879700006,
        0.035233425879700006,
        -0.0025909758017290006,
        -0.0025909758017290006,
        0.029476085351951252,
        -0.029476085351951252,
        -0.029476085351951252,
        0.029476085351951252,
        0.05898073895378817,
        0.018463477774636035,
        0.018463477774636035,
        0.09421416483348818,
        -0.003276374161489622,
        -0.003276374161489622,
        0.02173985193612566,
        0.02173985193612566,
        0.02173985193612566,
        0.02173985193612566,
        0.06484557443787466,
        0.0943216597898259,
        0.01867832322072119,
        0.01867832322072119,
        0.09421416483348818,
        -0.003276374161489622,
        -0.003276374161489622,
        0.02173985193612566,
        -0.02173985193612566,
        -0.02173985193612566,
        0.02173985193612566,
        0.05898073895378817,
        0.018463477774636035,
        0.018463477774636035,
        0.0943216597898259,
        0.01867832322072119,
        0.01867832322072119,
        0.06484557443787466,
        0.0970891982291751,
        0.042405629926062886,
        -0.042405629926062886,
        -0.042405629926062886,
        0.042405629926062886,
        0.05395287215237218,
        0.09635850207843506,
        0.09635850207843506,
        0.05395287215237218,
        0.11278693858600855]

        H4_qubit_hamiltonian = qforte.QuantumOperator()
        for i in range(len(circ_vec)):
            H4_qubit_hamiltonian.add_term(coef_vec[i], circ_vec[i])

        ref = [1,1,1,1,0,0,0,0]

        # make test with algorithm class
        mol = Molecule()
        mol.set_hamiltonian(H4_qubit_hamiltonian)

        MRSQK
        alg2 = MRSQK(mol, reference=ref, trotter_number=100)
        alg2.run(s=3, d=3)
        Egs2 = alg2.get_gs_energy()
        self.assertLess(abs(Egs2-E_fci), 1.0e-6)

        SRQK
        alg1 = SRQK(mol, reference=ref, trotter_number=100)
        alg1.run(s=6)
        Egs1 = alg1.get_gs_energy()
        self.assertLess(abs(Egs1-E_fci), 1.0e-4)


if __name__ == '__main__':
    unittest.main()
