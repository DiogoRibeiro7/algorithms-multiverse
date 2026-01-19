/**
 * @file streaming.h
 * @brief Streaming and online algorithms interface
 */

#ifndef AM_STREAMING_H
#define AM_STREAMING_H

#include <stddef.h>
#include <stdbool.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Reservoir sampling */
typedef struct reservoir_sampler reservoir_sampler_t;

reservoir_sampler_t* reservoir_sampler_create(size_t k);
void reservoir_sampler_destroy(reservoir_sampler_t* sampler);
void reservoir_sampler_add(reservoir_sampler_t* sampler, void* item);
void** reservoir_sampler_get_sample(const reservoir_sampler_t* sampler, size_t* count);
void reservoir_sampler_reset(reservoir_sampler_t* sampler);

/* Weighted reservoir sampling */
typedef struct weighted_reservoir_sampler weighted_reservoir_sampler_t;

weighted_reservoir_sampler_t* weighted_reservoir_create(size_t k);
void weighted_reservoir_destroy(weighted_reservoir_sampler_t* sampler);
void weighted_reservoir_add(weighted_reservoir_sampler_t* sampler,
                            void* item, double weight);
void** weighted_reservoir_get_sample(const weighted_reservoir_sampler_t* sampler,
                                     size_t* count);

/* Count-Min Sketch */
typedef struct count_min_sketch count_min_sketch_t;

count_min_sketch_t* cms_create(size_t width, size_t depth, uint32_t seed);
void cms_destroy(count_min_sketch_t* cms);
void cms_add(count_min_sketch_t* cms, const void* item, size_t item_size, int64_t count);
int64_t cms_query(const count_min_sketch_t* cms, const void* item, size_t item_size);
count_min_sketch_t* cms_merge(const count_min_sketch_t* cms1,
                              const count_min_sketch_t* cms2);
void cms_reset(count_min_sketch_t* cms);
double cms_error_bound(const count_min_sketch_t* cms);

/* HyperLogLog */
typedef struct hyperloglog hyperloglog_t;

hyperloglog_t* hll_create(size_t precision);
void hll_destroy(hyperloglog_t* hll);
void hll_add(hyperloglog_t* hll, const void* item, size_t item_size);
uint64_t hll_cardinality(const hyperloglog_t* hll);
hyperloglog_t* hll_merge(const hyperloglog_t* hll1, const hyperloglog_t* hll2);
void hll_reset(hyperloglog_t* hll);
double hll_error_rate(const hyperloglog_t* hll);

/* Bloom Filter */
typedef struct bloom_filter bloom_filter_t;

bloom_filter_t* bloom_create(size_t expected_items, double false_positive_rate);
void bloom_destroy(bloom_filter_t* filter);
void bloom_add(bloom_filter_t* filter, const void* item, size_t item_size);
bool bloom_contains(const bloom_filter_t* filter, const void* item, size_t item_size);
bloom_filter_t* bloom_merge(const bloom_filter_t* filter1,
                            const bloom_filter_t* filter2);
void bloom_reset(bloom_filter_t* filter);
double bloom_current_false_positive_rate(const bloom_filter_t* filter);
size_t bloom_count_estimate(const bloom_filter_t* filter);

/* Cuckoo Filter */
typedef struct cuckoo_filter cuckoo_filter_t;

cuckoo_filter_t* cuckoo_create(size_t capacity);
void cuckoo_destroy(cuckoo_filter_t* filter);
bool cuckoo_add(cuckoo_filter_t* filter, const void* item, size_t item_size);
bool cuckoo_contains(const cuckoo_filter_t* filter, const void* item, size_t item_size);
bool cuckoo_delete(cuckoo_filter_t* filter, const void* item, size_t item_size);
double cuckoo_load_factor(const cuckoo_filter_t* filter);

/* Streaming statistics */
typedef struct streaming_stats streaming_stats_t;

streaming_stats_t* streaming_stats_create(void);
void streaming_stats_destroy(streaming_stats_t* stats);
void streaming_stats_add(streaming_stats_t* stats, double value);
double streaming_stats_mean(const streaming_stats_t* stats);
double streaming_stats_variance(const streaming_stats_t* stats);
double streaming_stats_std_dev(const streaming_stats_t* stats);
double streaming_stats_min(const streaming_stats_t* stats);
double streaming_stats_max(const streaming_stats_t* stats);
size_t streaming_stats_count(const streaming_stats_t* stats);
void streaming_stats_reset(streaming_stats_t* stats);

/* Sliding window statistics */
typedef struct sliding_window sliding_window_t;

sliding_window_t* sliding_window_create(size_t window_size);
void sliding_window_destroy(sliding_window_t* window);
void sliding_window_add(sliding_window_t* window, double value);
double sliding_window_mean(const sliding_window_t* window);
double sliding_window_variance(const sliding_window_t* window);
double sliding_window_min(const sliding_window_t* window);
double sliding_window_max(const sliding_window_t* window);
double sliding_window_median(sliding_window_t* window);
size_t sliding_window_count(const sliding_window_t* window);

/* T-Digest for quantile estimation */
typedef struct tdigest tdigest_t;

tdigest_t* tdigest_create(double compression);
void tdigest_destroy(tdigest_t* digest);
void tdigest_add(tdigest_t* digest, double value, double weight);
double tdigest_quantile(const tdigest_t* digest, double q);
double tdigest_cdf(const tdigest_t* digest, double value);
tdigest_t* tdigest_merge(const tdigest_t* digest1, const tdigest_t* digest2);
size_t tdigest_size(const tdigest_t* digest);

/* Frequent items algorithms */
typedef struct {
    void** items;
    int64_t* counts;
    size_t num_items;
} frequent_items_t;

/* Misra-Gries algorithm */
typedef struct misra_gries misra_gries_t;

misra_gries_t* misra_gries_create(size_t k);
void misra_gries_destroy(misra_gries_t* mg);
void misra_gries_add(misra_gries_t* mg, const void* item, size_t item_size);
frequent_items_t* misra_gries_query(const misra_gries_t* mg, double threshold);
void frequent_items_destroy(frequent_items_t* items);

/* Space-Saving algorithm */
typedef struct space_saving space_saving_t;

space_saving_t* space_saving_create(size_t k);
void space_saving_destroy(space_saving_t* ss);
void space_saving_add(space_saving_t* ss, const void* item, size_t item_size);
frequent_items_t* space_saving_top_k(const space_saving_t* ss);

/* Lossy Counting */
typedef struct lossy_counting lossy_counting_t;

lossy_counting_t* lossy_counting_create(double epsilon);
void lossy_counting_destroy(lossy_counting_t* lc);
void lossy_counting_add(lossy_counting_t* lc, const void* item, size_t item_size);
frequent_items_t* lossy_counting_query(const lossy_counting_t* lc, double support);

/* Online learning algorithms */
typedef struct online_learner online_learner_t;

/* Perceptron */
online_learner_t* perceptron_create(size_t num_features);
void perceptron_update(online_learner_t* learner, const double* features, int label);
int perceptron_predict(const online_learner_t* learner, const double* features);

/* Passive-Aggressive */
online_learner_t* passive_aggressive_create(size_t num_features, double C);
void passive_aggressive_update(online_learner_t* learner,
                              const double* features, int label);
int passive_aggressive_predict(const online_learner_t* learner,
                              const double* features);

/* Online gradient descent */
online_learner_t* online_gd_create(size_t num_features, double learning_rate);
void online_gd_update(online_learner_t* learner, const double* features,
                     double target);
double online_gd_predict(const online_learner_t* learner, const double* features);

void online_learner_destroy(online_learner_t* learner);
double online_learner_get_accuracy(const online_learner_t* learner);

/* Streaming clustering */
typedef struct streaming_kmeans streaming_kmeans_t;

streaming_kmeans_t* streaming_kmeans_create(size_t k, size_t dim);
void streaming_kmeans_destroy(streaming_kmeans_t* kmeans);
void streaming_kmeans_add(streaming_kmeans_t* kmeans, const double* point);
int streaming_kmeans_predict(const streaming_kmeans_t* kmeans, const double* point);
double** streaming_kmeans_get_centers(const streaming_kmeans_t* kmeans);

/* BIRCH clustering */
typedef struct birch birch_t;

birch_t* birch_create(size_t branching_factor, double threshold, size_t dim);
void birch_destroy(birch_t* birch);
void birch_add(birch_t* birch, const double* point);
int birch_predict(const birch_t* birch, const double* point);
size_t birch_num_clusters(const birch_t* birch);

/* Stream sampling utilities */
void* stream_sample_single(void* stream, size_t n,
                           void* (*next_item)(void* stream));
void** stream_sample_multiple(void* stream, size_t n, size_t k,
                              void* (*next_item)(void* stream));

/* Morris counter (approximate counting) */
typedef struct morris_counter morris_counter_t;

morris_counter_t* morris_counter_create(void);
void morris_counter_destroy(morris_counter_t* counter);
void morris_counter_increment(morris_counter_t* counter);
uint64_t morris_counter_estimate(const morris_counter_t* counter);
morris_counter_t* morris_counter_merge(const morris_counter_t* c1,
                                       const morris_counter_t* c2);

/* FM-Sketch for distinct counting */
typedef struct fm_sketch fm_sketch_t;

fm_sketch_t* fm_sketch_create(size_t num_bitmaps);
void fm_sketch_destroy(fm_sketch_t* sketch);
void fm_sketch_add(fm_sketch_t* sketch, const void* item, size_t item_size);
uint64_t fm_sketch_estimate(const fm_sketch_t* sketch);
fm_sketch_t* fm_sketch_merge(const fm_sketch_t* s1, const fm_sketch_t* s2);

#ifdef __cplusplus
}
#endif

#endif /* AM_STREAMING_H */