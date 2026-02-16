/**
 * @file optimization.h
 * @brief Optimization algorithms interface
 */

#ifndef AM_OPTIMIZATION_H
#define AM_OPTIMIZATION_H

#include <stddef.h>
#include <stdbool.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Function types for optimization */
typedef double (*objective_func_1d)(double x, void* params);
typedef double (*objective_func_nd)(const double* x, size_t n, void* params);
typedef void (*gradient_func)(const double* x, size_t n, double* grad, void* params);
typedef void (*hessian_func)(const double* x, size_t n, double** hess, void* params);
typedef bool (*constraint_func)(const double* x, size_t n, void* params);

/* Optimization result structure */
typedef struct {
    double* solution;
    size_t dimension;
    double objective_value;
    size_t iterations;
    size_t function_evaluations;
    double* gradient_norm_history;
    double* objective_history;
    bool converged;
    char* message;
} optimization_result_t;

/* Optimization parameters */
typedef struct {
    double tolerance;
    double gradient_tolerance;
    int max_iterations;
    int max_function_evaluations;
    double step_size;
    double line_search_alpha;
    double line_search_beta;
    bool verbose;
} optimization_params_t;

/* Create and destroy optimization result */
optimization_result_t* optimization_result_create(size_t dimension);
void optimization_result_destroy(optimization_result_t* result);

/* Default parameters */
optimization_params_t optimization_get_default_params(void);

/* 1D optimization algorithms */
optimization_result_t* golden_section_search(objective_func_1d f, double a, double b,
                                             void* params,
                                             const optimization_params_t* opts);
optimization_result_t* brent_method(objective_func_1d f, double a, double b,
                                   void* params,
                                   const optimization_params_t* opts);
optimization_result_t* newton_method_1d(objective_func_1d f,
                                        objective_func_1d df,
                                        objective_func_1d ddf,
                                        double x0, void* params,
                                        const optimization_params_t* opts);

/* Unconstrained optimization algorithms */
optimization_result_t* gradient_descent(objective_func_nd f, gradient_func grad,
                                        const double* x0, size_t n,
                                        void* params,
                                        const optimization_params_t* opts);
optimization_result_t* newton_method(objective_func_nd f, gradient_func grad,
                                     hessian_func hess, const double* x0,
                                     size_t n, void* params,
                                     const optimization_params_t* opts);
optimization_result_t* conjugate_gradient(objective_func_nd f, gradient_func grad,
                                          const double* x0, size_t n,
                                          void* params,
                                          const optimization_params_t* opts);
optimization_result_t* bfgs(objective_func_nd f, gradient_func grad,
                            const double* x0, size_t n, void* params,
                            const optimization_params_t* opts);
optimization_result_t* l_bfgs(objective_func_nd f, gradient_func grad,
                              const double* x0, size_t n, int m,
                              void* params,
                              const optimization_params_t* opts);

/* Derivative-free optimization */
optimization_result_t* nelder_mead(objective_func_nd f, const double* x0,
                                   size_t n, void* params,
                                   const optimization_params_t* opts);
optimization_result_t* pattern_search(objective_func_nd f, const double* x0,
                                      size_t n, void* params,
                                      const optimization_params_t* opts);
optimization_result_t* simulated_annealing(objective_func_nd f, const double* x0,
                                           size_t n, const double* lower_bounds,
                                           const double* upper_bounds,
                                           void* params,
                                           const optimization_params_t* opts);

/* Global optimization algorithms */
optimization_result_t* differential_evolution(objective_func_nd f, size_t n,
                                              const double* lower_bounds,
                                              const double* upper_bounds,
                                              size_t pop_size, void* params,
                                              const optimization_params_t* opts);
optimization_result_t* particle_swarm(objective_func_nd f, size_t n,
                                     const double* lower_bounds,
                                     const double* upper_bounds,
                                     size_t swarm_size, void* params,
                                     const optimization_params_t* opts);
optimization_result_t* genetic_algorithm(objective_func_nd f, size_t n,
                                         const double* lower_bounds,
                                         const double* upper_bounds,
                                         size_t pop_size, void* params,
                                         const optimization_params_t* opts);

/* Constrained optimization */
optimization_result_t* penalty_method(objective_func_nd f,
                                      constraint_func* constraints,
                                      size_t num_constraints,
                                      const double* x0, size_t n,
                                      void* params,
                                      const optimization_params_t* opts);
optimization_result_t* barrier_method(objective_func_nd f,
                                      constraint_func* constraints,
                                      size_t num_constraints,
                                      const double* x0, size_t n,
                                      void* params,
                                      const optimization_params_t* opts);
optimization_result_t* augmented_lagrangian(objective_func_nd f, gradient_func grad,
                                            constraint_func* eq_constraints,
                                            size_t num_eq,
                                            constraint_func* ineq_constraints,
                                            size_t num_ineq,
                                            const double* x0, size_t n,
                                            void* params,
                                            const optimization_params_t* opts);

/* Linear programming */
typedef struct {
    double* c;      /* Objective coefficients */
    double** A;     /* Constraint matrix */
    double* b;      /* Right-hand side */
    size_t n_vars;  /* Number of variables */
    size_t n_constraints;  /* Number of constraints */
} linear_program_t;

optimization_result_t* simplex_method(const linear_program_t* lp);
optimization_result_t* interior_point_lp(const linear_program_t* lp);
optimization_result_t* revised_simplex(const linear_program_t* lp);

/* Quadratic programming */
typedef struct {
    double** Q;     /* Quadratic term matrix */
    double* c;      /* Linear term */
    double** A;     /* Constraint matrix */
    double* b;      /* Right-hand side */
    size_t n_vars;
    size_t n_constraints;
} quadratic_program_t;

optimization_result_t* quadratic_programming(const quadratic_program_t* qp);
optimization_result_t* active_set_qp(const quadratic_program_t* qp);

/* Integer programming */
optimization_result_t* branch_and_bound(objective_func_nd f,
                                        const double* lower_bounds,
                                        const double* upper_bounds,
                                        const bool* integer_vars,
                                        size_t n, void* params,
                                        const optimization_params_t* opts);
optimization_result_t* cutting_plane(const linear_program_t* lp,
                                     const bool* integer_vars);

/* Multi-objective optimization */
typedef struct {
    double** solutions;  /* Pareto front solutions */
    double** objectives;  /* Objective values */
    size_t num_solutions;
    size_t n_vars;
    size_t n_objectives;
} pareto_front_t;

pareto_front_t* nsga2(objective_func_nd* objectives, size_t n_objectives,
                      size_t n_vars, const double* lower_bounds,
                      const double* upper_bounds, size_t pop_size,
                      void* params, const optimization_params_t* opts);
void pareto_front_destroy(pareto_front_t* front);

/* Trust region methods */
optimization_result_t* trust_region_newton(objective_func_nd f, gradient_func grad,
                                           hessian_func hess, const double* x0,
                                           size_t n, void* params,
                                           const optimization_params_t* opts);
optimization_result_t* dogleg(objective_func_nd f, gradient_func grad,
                             hessian_func hess, const double* x0,
                             size_t n, void* params,
                             const optimization_params_t* opts);

/* Line search algorithms */
double backtracking_line_search(objective_func_nd f, gradient_func grad,
                                const double* x, const double* direction,
                                size_t n, double alpha, double c1, void* params);
double wolfe_line_search(objective_func_nd f, gradient_func grad,
                         const double* x, const double* direction,
                         size_t n, double c1, double c2, void* params);

/* Stochastic optimization */
optimization_result_t* stochastic_gradient_descent(objective_func_nd f,
                                                   gradient_func stoch_grad,
                                                   const double* x0, size_t n,
                                                   double learning_rate,
                                                   size_t batch_size,
                                                   void* params,
                                                   const optimization_params_t* opts);
optimization_result_t* adam_optimizer(objective_func_nd f, gradient_func stoch_grad,
                                     const double* x0, size_t n,
                                     double learning_rate, double beta1,
                                     double beta2, size_t batch_size,
                                     void* params,
                                     const optimization_params_t* opts);

/* Utility functions */
double* numerical_gradient(objective_func_nd f, const double* x, size_t n,
                           double epsilon, void* params);
double** numerical_hessian(objective_func_nd f, const double* x, size_t n,
                          double epsilon, void* params);
bool check_gradient(objective_func_nd f, gradient_func grad,
                    const double* x, size_t n, double tolerance, void* params);

#ifdef __cplusplus
}
#endif

#endif /* AM_OPTIMIZATION_H */