#ifndef __BINDINGS_DF_H
#define __BINDINGS_DF_H
#ifdef __cplusplus
extern "C"
{
  #endif
  
  #include <stdint.h>
  #include <stdbool.h>
  typedef struct {
    int64_t *ptr;
    size_t len;
  } df_list_s64_t;
  void df_list_s64_free(df_list_s64_t *ptr);
  int64_t df_square(int64_t val);
  void df_square_vec(df_list_s64_t *val, df_list_s64_t *ret0);
  int64_t df_mult(int64_t a, int64_t b);
  void df_mult_vec(df_list_s64_t *a, df_list_s64_t *b, df_list_s64_t *ret0);
  #ifdef __cplusplus
}
#endif
#endif
