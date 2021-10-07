#include <stdlib.h>
#include "df.h"

__attribute__((weak, export_name("canonical_abi_realloc")))
void *canonical_abi_realloc(
void *ptr,
size_t orig_size,
size_t org_align,
size_t new_size
) {
  void *ret = realloc(ptr, new_size);
  if (!ret)
  abort();
  return ret;
}

__attribute__((weak, export_name("canonical_abi_free")))
void canonical_abi_free(
void *ptr,
size_t size,
size_t align
) {
  free(ptr);
}
void df_list_s64_free(df_list_s64_t *ptr) {
  canonical_abi_free(ptr->ptr, ptr->len * 8, 8);
}
static int64_t RET_AREA[2];
__attribute__((export_name("square")))
int64_t __wasm_export_df_square(int64_t arg) {
  int64_t ret = df_square(arg);
  return ret;
}
__attribute__((export_name("square_vec")))
int32_t __wasm_export_df_square_vec(int32_t arg, int32_t arg0) {
  df_list_s64_t arg1 = (df_list_s64_t) { (int64_t*)(arg), (size_t)(arg0) };
  df_list_s64_t ret;
  df_square_vec(&arg1, &ret);
  int32_t ptr = (int32_t) &RET_AREA;
  *((int32_t*)(ptr + 8)) = (int32_t) (ret).len;
  *((int32_t*)(ptr + 0)) = (int32_t) (ret).ptr;
  return ptr;
}
__attribute__((export_name("mult")))
int64_t __wasm_export_df_mult(int64_t arg, int64_t arg0) {
  int64_t ret = df_mult(arg, arg0);
  return ret;
}
__attribute__((export_name("mult_vec")))
int32_t __wasm_export_df_mult_vec(int32_t arg, int32_t arg0, int32_t arg1, int32_t arg2) {
  df_list_s64_t arg3 = (df_list_s64_t) { (int64_t*)(arg), (size_t)(arg0) };
  df_list_s64_t arg4 = (df_list_s64_t) { (int64_t*)(arg1), (size_t)(arg2) };
  df_list_s64_t ret;
  df_mult_vec(&arg3, &arg4, &ret);
  int32_t ptr = (int32_t) &RET_AREA;
  *((int32_t*)(ptr + 8)) = (int32_t) (ret).len;
  *((int32_t*)(ptr + 0)) = (int32_t) (ret).ptr;
  return ptr;
}
