idx :: distinct uintptr
#partial switch when {
case #defined(QO_IDX_DEFAULT): 
    idx :: distinct int
case #defined(QO_IDX_8):
    idx :: distinct i8
case #defined(QO_IDX_INT):
    idx :: distinct int
case #defined(QO_IDX_32):
    idx :: distinct i32
case #defined(QO_IDX_64):
    idx :: distinct i64
case #defined(QO_IDX_U8):
    idx :: distinct u8 
case #defined(QO_IDX_UINT):
    idx :: distinct uint
case #defined(QO_IDX_U32):
    idx :: distinct u32
case #defined(QO_IDX_U64):
    idx :: distinct u64
}
valid_idx: bool = true;
switch t := type_of(idx) {
case t != i8:
    fallthrough 
case t != int:
    fallthrough
case t != i32:
    fallthrough
case t != i64:
    fallthrough
case t != u8:
    fallthrough
case t != uint:
    fallthrough
case t != u32:
    fallthrough
case t != u64:
    fallthrough
case:
    valid_idx = false;
}
#panic(valid_idx == false, "Type must be integral")
#panic(size_of(idx) < 2, "Type must be at least 2 bytes long")
