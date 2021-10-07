#include <stdlib.h>
#include "df.h"

int64_t df_square(int64_t val) {
    return(val * val);
}

void df_square_vec(df_list_s64_t *val, df_list_s64_t *ret0) {
    if (!val || !ret0 || val-> len == 0) return;
    ret0->ptr = malloc(sizeof(int64_t) * val->len);
    if (!ret0->ptr) return;
    ret0->len = val->len;
    for (int32_t i = 0; i < val->len; i++) {
 	ret0->ptr[i] = val->ptr[i] * val->ptr[i];
    }
}

int64_t df_mult(int64_t a, int64_t b) {
    return a * b;
}

void df_mult_vec(df_list_s64_t *a, df_list_s64_t *b, df_list_s64_t *ret0) {
    if (a->len != b->len || a->len == 0) return;
    ret0->ptr = malloc(sizeof(int64_t) * a->len);
    if (!ret0->ptr) return;
    ret0->len = a->len;
    for (int32_t i = 0; i < a->len; i++) {
 	ret0->ptr[i] = a->ptr[i] * b->ptr[i];
    }
}
