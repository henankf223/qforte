#ifndef _sq_operator_h_
#define _sq_operator_h_

#include <complex>
#include <string>
#include <vector>

class SQOperator {
  public:
    /// default constructor: creates an empty second quantized operator
    SQOperator() {}

    /// TODO: implement
    /// build from a string of open fermion qubit operators
    // void build_from_openferm_str(std::string op) {}

    /// add one product of anihilators and/or creators to the second quantized operator
    void add_term(std::complex<double> coeff, const std::vector<size_t>& ac_ops);

    /// add an second quantized operator to the second quantized operator
    void add_op(const SQOperator& sqo);

    /// sets the operator coefficeints
    void set_coeffs(const std::vector<std::complex<double>>& new_coeffs);

    /// return a vector of terms and thier coeficients
    const std::vector<std::pair< std::complex<double>, std::vector<size_t>>>& terms() const;

    /// return a vector of string representing this quantum operator
    std::string str() const;

  private:
    /// the list of circuits
    std::vector<std::pair< std::complex<double>, std::vector<size_t>>> terms_;
};

#endif // _sq_operator_h_
